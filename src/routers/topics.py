"""
Topic analysis endpoints
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException

from agents.topic_analysis_agent import TopicAnalysisAgent, TopicRecommendation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/topics", tags=["topics"])

# Global topic agent
topic_agent = None

def get_topic_agent():
    """Get or create topic analysis agent"""
    global topic_agent
    if topic_agent is None:
        topic_agent = TopicAnalysisAgent()
    return topic_agent


@router.post("/analyze")
async def analyze_topics(
    keywords: List[str] = [],
    competitor_urls: List[str] = [],
    existing_titles: List[str] = [],
    max_recommendations: int = 10
):
    """
    Analyze topics and identify content opportunities
    
    Args:
        keywords: Keywords to analyze
        competitor_urls: Competitor URLs to analyze (optional)
        existing_titles: Your existing content titles to avoid duplication
        max_recommendations: Maximum topic recommendations
    """
    agent = get_topic_agent()
    
    try:
        # Get competitor content if URLs provided
        competitor_content = []
        if competitor_urls:
            # Would scrape competitor URLs here
            for url in competitor_urls[:5]:
                competitor_content.append({"title": f"Competitor article from {url}", "url": url})
        
        # Perform analysis
        report = await agent.analyze_topics(
            competitor_content=competitor_content if competitor_content else None,
            target_keywords=keywords if keywords else None,
            existing_content=existing_titles,
            max_recommendations=max_recommendations
        )
        
        return {
            "keywords_analyzed": report.keywords_analyzed,
            "content_gaps_found": report.content_gaps_found,
            "topics_recommended": report.topics_recommended,
            "recommendations": [
                {
                    "title": rec.title,
                    "slug": rec.slug,
                    "primary_keyword": rec.primary_keyword,
                    "secondary_keywords": rec.secondary_keywords,
                    "content_type": rec.content_type,
                    "target_word_count": rec.target_word_count,
                    "priority_score": rec.priority_score,
                    "rationale": rec.rationale,
                    "outline": rec.content_outline
                }
                for rec in report.recommendations
            ],
            "market_insights": report.market_insights,
            "analyzed_at": report.analyzed_at.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Topic analysis failed: {e}")
        raise HTTPException(500, f"Topic analysis failed: {str(e)}")


@router.get("/recommendations")
async def get_quick_topic_recommendations(
    count: int = 5,
    focus: Optional[str] = None
):
    """
    Get quick topic recommendations without full analysis
    
    Args:
        count: Number of recommendations (default 5)
        focus: Optional focus area (e.g., "PTSD", "training", "laws")
    """
    agent = get_topic_agent()
    
    try:
        recommendations = await agent.get_quick_recommendations(count=count, focus=focus)
        
        return {
            "recommendations": [
                {
                    "title": rec.title,
                    "slug": rec.slug,
                    "primary_keyword": rec.primary_keyword,
                    "content_type": rec.content_type,
                    "priority_score": rec.priority_score,
                    "target_word_count": rec.target_word_count
                }
                for rec in recommendations
            ],
            "count": len(recommendations),
            "focus": focus
        }
        
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        raise HTTPException(500, f"Failed to get recommendations: {str(e)}")


@router.get("/gaps")
async def identify_content_gaps(
    keywords: List[str] = [],
    existing_titles: List[str] = []
):
    """
    Identify content gaps based on keywords and existing content
    """
    agent = get_topic_agent()
    
    try:
        # Analyze for gaps
        report = await agent.analyze_topics(
            target_keywords=keywords if keywords else agent.SEED_KEYWORDS[:10],
            existing_content=existing_titles,
            max_recommendations=5
        )
        
        return {
            "gaps": [
                {
                    "topic": gap.topic,
                    "gap_type": gap.gap_type,
                    "opportunity_score": gap.opportunity_score,
                    "difficulty_score": gap.difficulty_score,
                    "rationale": gap.rationale,
                    "competitors_covering": gap.competitors_covering
                }
                for gap in report.content_gaps
            ],
            "total_gaps": len(report.content_gaps)
        }
        
    except Exception as e:
        logger.error(f"Failed to identify gaps: {e}")
        raise HTTPException(500, f"Failed to identify content gaps: {str(e)}")