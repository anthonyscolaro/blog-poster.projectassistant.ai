"""
Article generation and management endpoints
"""
import os
import glob
import logging
import json as json_lib
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from ..models import RunResponse, InputsEnvelope
from agents import (
    ArticleGenerationAgent, GeneratedArticle, SEORequirements,
    CompetitorMonitoringAgent
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/articles", tags=["articles"])

# Global agent instances
article_agent = None

def get_article_agent():
    """Get or create article generation agent"""
    global article_agent
    if article_agent is None:
        article_agent = ArticleGenerationAgent()
    return article_agent


def get_competitor_agent():
    """Get or create competitor monitoring agent"""
    # This function is referenced but not defined in original code
    # Adding placeholder implementation
    try:
        from ..routers.competitors import get_competitor_agent as get_comp_agent
        return get_comp_agent()
    except:
        return None


@router.post("/agent/run", response_model=RunResponse)
async def run_agent(payload: InputsEnvelope):
    """Generate a complete SEO-optimized article using the Article Generation Agent"""
    try:
        # Get or create article generation agent
        agent = get_article_agent()
        
        # Extract topic and keywords from payload
        topic_rec = payload.topic_rec
        topic = f"{topic_rec.primary_kw}: {topic_rec.rationale or 'Comprehensive Guide'}"
        
        # Create SEO requirements
        seo_reqs = SEORequirements(
            primary_keyword=topic_rec.primary_kw,
            secondary_keywords=topic_rec.secondary_kws[:5],  # Limit to 5 secondary keywords
            min_words=payload.constraints.min_words,
            max_words=payload.constraints.max_words,
            internal_links_count=3,
            external_links_count=2
        )
        
        # Get competitor insights if available
        competitor_insights = None
        if hasattr(payload, 'evidence') and payload.evidence.competitor_chunks:
            competitor_insights = {
                "competitor_topics": list(set([chunk.text[:100] for chunk in payload.evidence.competitor_chunks[:5]])),
                "serp_titles": [item.title for item in payload.evidence.serp_snapshot[:5]] if payload.evidence.serp_snapshot else []
            }
        
        # Generate the article
        logger.info(f"Generating article about: {topic}")
        article = await agent.generate_article(
            topic=topic,
            seo_requirements=seo_reqs,
            brand_voice=payload.brand_style.voice,
            target_audience=payload.brand_style.audience,
            additional_context=topic_rec.rationale,
            competitor_insights=competitor_insights
        )
        
        # Convert to expected output format
        output = f"""# {article.title}

{article.content_markdown}

---
**SEO Metadata:**
- Meta Title: {article.meta_title}
- Meta Description: {article.meta_description}
- Primary Keyword: {article.primary_keyword}
- Word Count: {article.word_count}
- SEO Score: {article.seo_score:.1f}/100
- Reading Time: {article.estimated_reading_time} minutes
- Cost: ${article.cost_tracking.cost:.4f if article.cost_tracking else 0.0}
"""
        
        return RunResponse(
            status="success",
            output=output,
            tool_calls=[],
            tool_results=[],
            errors=[]
        )
    except Exception as e:
        logger.error(f"Error generating article: {e}")
        return RunResponse(
            status="error",
            output="",
            tool_calls=[],
            tool_results=[],
            errors=[str(e)]
        )


@router.post("/generate")
async def generate_article(
    topic: str,
    primary_keyword: str,
    secondary_keywords: List[str] = [],
    min_words: int = 1500,
    max_words: int = 2500,
    use_competitor_insights: bool = True
):
    """
    Generate a complete SEO-optimized article
    
    Args:
        topic: Topic to write about
        primary_keyword: Main SEO keyword
        secondary_keywords: Additional keywords
        min_words: Minimum word count
        max_words: Maximum word count
        use_competitor_insights: Whether to use competitor analysis
    """
    agent = get_article_agent()
    
    # Create SEO requirements
    seo_reqs = SEORequirements(
        primary_keyword=primary_keyword,
        secondary_keywords=secondary_keywords[:5],
        min_words=min_words,
        max_words=max_words
    )
    
    # Get competitor insights if requested
    competitor_insights = None
    if use_competitor_insights:
        try:
            comp_agent = get_competitor_agent()
            if comp_agent:
                insights = await comp_agent.generate_insights()
                competitor_insights = {
                    "trending_topics": [t.topic for t in insights.trending_topics[:3]],
                    "content_gaps": [g.topic for g in insights.content_gaps[:3]],
                    "recommended_topics": insights.recommended_topics[:3]
                }
        except Exception as e:
            logger.warning(f"Could not get competitor insights: {e}")
    
    try:
        article = await agent.generate_article(
            topic=topic,
            seo_requirements=seo_reqs,
            brand_voice="professional, empathetic, and informative",
            target_audience="Service dog handlers and business owners",
            competitor_insights=competitor_insights
        )
        
        return article.dict()
    
    except Exception as e:
        logger.error(f"Article generation failed: {str(e)}")
        raise HTTPException(500, f"Article generation failed: {str(e)}")


@router.get("/costs")
async def get_article_costs():
    """Get cost summary for article generation"""
    agent = get_article_agent()
    return agent.get_cost_summary()


@router.delete("/{article_id}")
async def delete_article(article_id: str):
    """Delete an article file"""
    try:
        # Find the article file
        article_files = glob.glob("data/articles/*.json")
        article_path = None
        
        for file_path in article_files:
            filename = os.path.basename(file_path).replace('.json', '')
            if article_id == filename or article_id in file_path:
                article_path = file_path
                break
        
        if not article_path:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Delete the file
        os.remove(article_path)
        logger.info(f"Deleted article: {article_path}")
        
        return JSONResponse({
            "success": True,
            "message": f"Article deleted successfully"
        })
        
    except Exception as e:
        logger.error(f"Failed to delete article {article_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete article: {str(e)}")