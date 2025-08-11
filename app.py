"""
FastAPI tool shim that orchestrates Claude 3.5 Sonnet with:
- Verifiable slot completion via <tool .../> tags
- Internal link resolver
- SEO lint checker
- Strong Pydantic contracts for inputs/outputs

This file is self-contained for a demo. Replace stubbed services (fact checker, links, vector search) with real implementations.

Run:
  uvicorn app:app --reload --port 8088

Env (example):
  ANTHROPIC_API_KEY=...
  VECTOR_BACKEND=qdrant|convex|memory
  QDRANT_URL=http://localhost:6333
"""
from __future__ import annotations

import os
import re
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl, Field, validator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------
# Pydantic Contracts
# ------------------------------

class InternalLinkCandidate(BaseModel):
    url: HttpUrl
    title: str
    embedding_id: Optional[str] = None
    brief_summary: Optional[str] = None

class TopicRec(BaseModel):
    topic_slug: str
    primary_kw: str
    secondary_kws: List[str] = []
    title_variants: List[str] = []
    rationale: Optional[str] = None
    supporting_urls: List[HttpUrl] = []
    score_breakdown: Dict[str, float] = {}
    risk_flags: List[str] = []

class BrandStyle(BaseModel):
    voice: str = "clear, empathetic"
    audience: str = "general public"
    tone: str = "confident"
    reading_grade_target: int = 8
    banned_phrases: List[str] = []

class SiteInfo(BaseModel):
    site_url: HttpUrl
    canonical_base: HttpUrl
    category_map: Dict[str, int]
    internal_link_candidates: List[InternalLinkCandidate] = []

class SerpItem(BaseModel):
    url: HttpUrl
    title: str
    h1: Optional[str] = None
    h2s: List[str] = []
    meta_desc: Optional[str] = None

class CompetitorChunk(BaseModel):
    url: HttpUrl
    text: str
    chunk_id: str

class Evidence(BaseModel):
    facts: List[str] = []
    statutes: List[str] = []  # e.g., "28 CFR §36.302(c)"
    dates: List[str] = []     # human-readable dates or ISO
    sources: List[HttpUrl] = []
    serp_snapshot: List[SerpItem] = []
    competitor_chunks: List[CompetitorChunk] = []

class Constraints(BaseModel):
    min_words: int = 1500
    max_words: int = 2500
    image_policy: str = "stock_or_generated_ok"
    require_disclaimer: bool = True
    disallow_competitor_links: bool = True

class InputsEnvelope(BaseModel):
    topic_rec: TopicRec
    brand_style: BrandStyle
    site_info: SiteInfo
    evidence: Evidence
    constraints: Constraints

class ArticleDraft(BaseModel):
    title: str
    slug: str
    category: str
    tags: List[str]
    meta_title: str
    meta_desc: str
    canonical: HttpUrl
    schema_jsonld: Dict[str, Any]
    hero_image_prompt: str
    internal_link_targets: List[HttpUrl]
    citations: List[HttpUrl]
    markdown: str

# Tool call parsing
class ToolCall(BaseModel):
    name: str
    args: Dict[str, Any] = {}

class ToolResult(BaseModel):
    name: str
    payload: Dict[str, Any]

# ------------------------------
# Simple tool tag parser
# ------------------------------
TOOL_TAG_RE = re.compile(r"<tool\s+name=\"([^\"]+)\"([^>]*)/>")
ARG_RE = re.compile(r"(\w+)=\"([^\"]*)\"")


def parse_tool_calls(text: str) -> List[ToolCall]:
    calls: List[ToolCall] = []
    for m in TOOL_TAG_RE.finditer(text or ""):
        name = m.group(1)
        raw = m.group(2)
        args = {k: v for k, v in ARG_RE.findall(raw)}
        # decode JSON-ish args if present
        for k, v in list(args.items()):
            if v and (v.startswith("{") or v.startswith("[")):
                try:
                    args[k] = json.loads(v)
                except Exception:
                    pass
        calls.append(ToolCall(name=name, args=args))
    return calls


# ------------------------------
# Stubbed Services (replace with real)
# ------------------------------

class FactCheckerService:
    """Replace with real retrieval (SERP + vectors) and citation filters."""

    async def search(self, q: str, jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        # Demo payload: return authoritative ADA sources when query hints ADA
        results = {
            "facts": [
                "The ADA does not require service dog registration or certification.",
                "Businesses may ask only two questions to determine if the dog is a service animal." 
            ],
            "statutes": ["28 CFR §36.302(c)", "28 CFR §35.136"],
            "dates": ["2010-07-23"],
            "sources": [
                "https://www.ada.gov/resources/service-animals-2010-requirements/",
                "https://www.ecfr.gov/current/title-28/part-36/section-36.302",
                "https://www.ada.gov/resources/service-animals-faqs/"
            ],
        }
        return results


class InternalLinkService:
    """Resolve internal links from provided candidates. In production, back this with vectors."""

    async def resolve(self, section_summary: str, candidates: List[InternalLinkCandidate], limit: int = 3) -> List[Dict[str, Any]]:
        # naive scoring by token overlap; replace with ANN/vector search
        tokens = set(section_summary.lower().split())
        scored = []
        for c in candidates:
            score = sum(1 for t in tokens if t in (c.title or '').lower())
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = [
            {"url": str(c.url), "title": c.title}
            for score, c in scored[:limit] if score > 0
        ]
        return top


class SeoLintService:
    """Basic lints. Expand as needed."""

    async def lint(self, frontmatter: Dict[str, Any], markdown: str) -> List[str]:
        errs: List[str] = []
        title = frontmatter.get("meta_title", "")
        meta = frontmatter.get("meta_desc", "")
        if not (45 <= len(title) <= 60):
            errs.append(f"meta_title length {len(title)} out of 45–60")
        if not (140 <= len(meta) <= 160):
            errs.append(f"meta_desc length {len(meta)} out of 140–160")
        # H1 count
        h1s = re.findall(r"^#\s+.+$", markdown, flags=re.MULTILINE)
        if len(h1s) != 1:
            errs.append(f"expected exactly 1 H1, found {len(h1s)}")
        # Image alt check: ![alt](url)
        for m in re.finditer(r"!\[(.*?)\]\((.*?)\)", markdown):
            if not m.group(1).strip():
                errs.append("image missing alt text")
        # Canonical present
        if not frontmatter.get("canonical"):
            errs.append("canonical missing")
        return errs


fact_checker = FactCheckerService()
linker = InternalLinkService()
seo_lint = SeoLintService()

# ------------------------------
# Anthropic (Claude) client wrapper
# ------------------------------
try:
    import anthropic  # type: ignore
except ImportError:  # allow file to run without SDK installed
    anthropic = None


class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        # Only create client if we have a valid API key (not placeholder)
        if anthropic and self.api_key and not self.api_key.startswith("your-"):
            self.client = anthropic.Client(api_key=self.api_key)
        else:
            self.client = None

    async def complete(self, system_prompt: str, user_json: Dict[str, Any]) -> str:
        if not self.client:
            # Demo: return a fake tool call to show the shim working
            return '<tool name="fact_check.search" q="service dog ADA two questions DOJ" jurisdiction="US"/>'
        msg = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": json.dumps(user_json, default=str)}],
        )
        return msg.content[0].text  # type: ignore

    async def continue_with_tool_result(self, history: List[Dict[str, str]], tool_result: ToolResult) -> str:
        if not self.client:
            # Demo: after tool result, pretend Claude returns a finished Markdown doc
            return (
                "---\n"
                "title: Example\nslug: example\ncategory: ADA Compliance\n"
                "tags: [service dogs]\nmeta_title: Example Title That Fits\n"
                "meta_desc: This is a meta description with the right length for SEO checks.\n"
                "canonical: https://example.com/example\n"
                "schema_jsonld: {}\nhero_image_prompt: Service dog in restaurant\n"
                "internal_link_targets: []\n"
                "citations: [https://www.ada.gov/resources/service-animals-2010-requirements/]\n---\n\n"
                "# Example\n\nBody...\n"
            )
        # When using real SDK, append tool result as a user message the model expects
        msg = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=5000,
            messages=history + [
                {"role": "user", "content": json.dumps({"tool_result": tool_result.model_dump()}, default=str)}
            ],
        )
        return msg.content[0].text  # type: ignore


claude = ClaudeClient()

# ------------------------------
# FastAPI App
# ------------------------------
app = FastAPI(title="Blog Poster Dashboard")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates and static files for dashboard
templates = Jinja2Templates(directory="templates")

# Add markdown filter for rendering content
import markdown
def markdown_filter(text):
    """Convert markdown to HTML"""
    return markdown.markdown(text, extensions=['codehilite', 'fenced_code'])

templates.env.filters['markdown'] = markdown_filter

# Create directories if they don't exist
import os
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

try:
    # Include the WordPress publishing router providing /publish/wp
    from fast_api_tool_shim_pydantic_schemas_for_article_generation_agent_updated import (
        router as publish_router,
    )
    app.include_router(publish_router)
except Exception:
    pass

# Include configuration profile management API
try:
    from src.config.config_api import router as config_router
    app.include_router(config_router)
except Exception:
    # Router is optional; the app can run without it if dependencies are missing
    publish_router = None  # type: ignore


@app.get("/health")
async def health() -> Dict[str, Any]:
    """Simple health endpoint for container checks."""
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


class RunResponse(BaseModel):
    status: str
    output: Optional[str] = None
    tool_calls: List[ToolCall] = []
    tool_results: List[ToolResult] = []
    errors: List[str] = []


@app.post("/agent/run", response_model=RunResponse)
async def run_agent(payload: InputsEnvelope):
    """Generate a complete SEO-optimized article using the Article Generation Agent"""
    try:
        # Get or create article generation agent
        from agents import ArticleGenerationAgent, SEORequirements
        
        agent = ArticleGenerationAgent()
        
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


# ------------------------------
# Optional: simple endpoint to lint a draft post-hoc
# ------------------------------
class LintRequest(BaseModel):
    frontmatter: Dict[str, Any]
    markdown: str

class LintResponse(BaseModel):
    violations: List[str]

@app.post("/seo/lint", response_model=LintResponse)
async def lint_endpoint(req: LintRequest):
    v = await seo_lint.lint(req.frontmatter, req.markdown)
    return LintResponse(violations=v)


# ------------------------------
# WordPress Publishing Endpoints
# ------------------------------

from src.services.wordpress_publisher import WordPressPublisher

@app.post("/publish/wp")
async def publish_to_wordpress(
    title: str,
    content: str,
    status: Literal["draft", "publish"] = "draft",
    slug: Optional[str] = None,
    categories: Optional[List[int]] = None,
    tags: Optional[List[int]] = None,
    meta_title: Optional[str] = None,
    meta_description: Optional[str] = None
):
    """
    Publish an article to WordPress
    
    Args:
        title: Article title
        content: Article content (HTML or Markdown)
        status: Post status (draft or publish)
        slug: URL slug
        categories: List of category IDs
        tags: List of tag IDs
        meta_title: SEO meta title
        meta_description: SEO meta description
    """
    # Get active configuration profile
    try:
        from src.config.config_profiles import get_profile_manager
        manager = get_profile_manager()
        active_profile = manager.get_active_profile()
        
        if active_profile and active_profile.wordpress:
            # Use configuration from active profile
            publisher = WordPressPublisher(
                wp_url=active_profile.wordpress.url,
                username=active_profile.wordpress.username,
                password=active_profile.wordpress.password,
                auth_method=active_profile.wordpress.auth_method,
                verify_ssl=active_profile.wordpress.verify_ssl
            )
        else:
            # Fallback to environment variables
            publisher = WordPressPublisher()
    except Exception as e:
        logger.warning(f"Could not load active profile, using environment variables: {e}")
        publisher = WordPressPublisher()
    
    # Test connection first
    connected = await publisher.test_connection()
    if not connected:
        return {
            "success": False,
            "error": "Failed to connect to WordPress. Check credentials and URL."
        }
    
    # Prepare meta fields if SEO data provided
    meta = {}
    if meta_title:
        meta["meta_title"] = meta_title
    if meta_description:
        meta["meta_description"] = meta_description
    
    # Create the post
    result = await publisher.create_post(
        title=title,
        content=content,
        status=status,
        slug=slug,
        categories=categories,
        tags=tags,
        meta=meta if meta else None
    )
    
    if result["success"]:
        logger.info(f"Successfully published post {result['post_id']}: {result['edit_link']}")
    else:
        logger.error(f"Failed to publish post: {result.get('error')}")
    
    return result

@app.get("/wordpress/test")
async def test_wordpress_connection():
    """Test WordPress connection and authentication"""
    publisher = WordPressPublisher()
    connected = await publisher.test_connection()
    
    if connected:
        # Get categories and tags for reference
        categories = await publisher.get_categories()
        tags = await publisher.get_tags()
        
        return {
            "connected": True,
            "wordpress_url": publisher.wordpress_url,
            "auth_method": publisher.auth_method,
            "is_local": publisher.is_local,
            "categories": [{"id": cat["id"], "name": cat["name"]} for cat in categories[:5]],
            "tags": [{"id": tag["id"], "name": tag["name"]} for tag in tags[:5]]
        }
    else:
        return {
            "connected": False,
            "error": "Failed to connect to WordPress",
            "wordpress_url": publisher.wordpress_url,
            "auth_method": publisher.auth_method
        }

# ------------------------------
# Article Generation Endpoints
# ------------------------------
from agents import (
    CompetitorMonitoringAgent, CompetitorInsights,
    ArticleGenerationAgent, GeneratedArticle, SEORequirements
)
from typing import List

# Global agent instances
article_agent = None

def get_article_agent():
    """Get or create article generation agent"""
    global article_agent
    if article_agent is None:
        article_agent = ArticleGenerationAgent()
    return article_agent

@app.post("/article/generate")
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

@app.get("/article/costs")
async def get_article_costs():
    """Get cost summary for article generation"""
    agent = get_article_agent()
    return agent.get_cost_summary()


# ------------------------------
# Competitor Monitoring Endpoints  
# ------------------------------

# Global agent instance (in production, use dependency injection)
competitor_agent = None

def get_competitor_agent():
    """Get or create competitor monitoring agent"""
    global competitor_agent
    if competitor_agent is None:
        competitor_agent = CompetitorMonitoringAgent()
    return competitor_agent

@app.post("/competitors/scan")
async def scan_competitors(force: bool = False):
    """
    Scan competitor websites for new content
    
    Args:
        force: Force scan even if recently scanned
    """
    agent = get_competitor_agent()
    try:
        content = await agent.scan_competitors(force=force)
        return {
            "status": "success",
            "content_pieces": len(content),
            "message": f"Scanned {len(content)} pieces of content"
        }
    except Exception as e:
        logger.error(f"Competitor scan failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/competitors/insights")
async def get_competitor_insights():
    """Get comprehensive competitor analysis and insights"""
    agent = get_competitor_agent()
    try:
        insights = await agent.generate_insights()
        return insights.dict()
    except Exception as e:
        logger.error(f"Failed to generate insights: {str(e)}")
        raise HTTPException(500, f"Failed to generate insights: {str(e)}")

@app.get("/competitors/trends")
async def get_trending_topics():
    """Get current trending topics from competitors"""
    agent = get_competitor_agent()
    try:
        content = await agent.scan_competitors()
        trends = agent.analyze_trends(content)
        return {
            "trends": [t.dict() for t in trends],
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get trends: {str(e)}")
        raise HTTPException(500, f"Failed to get trends: {str(e)}")

@app.get("/competitors/gaps")
async def get_content_gaps():
    """Identify content gaps compared to competitors"""
    agent = get_competitor_agent()
    try:
        content = await agent.scan_competitors()
        gaps = agent.identify_content_gaps(content)
        return {
            "gaps": [g.dict() for g in gaps],
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to identify gaps: {str(e)}")
        raise HTTPException(500, f"Failed to identify gaps: {str(e)}")


# ------------------------------
# Topic Analysis Endpoints
# ------------------------------
from agents.topic_analysis_agent import TopicAnalysisAgent, TopicRecommendation

# Global topic agent
topic_agent = None

def get_topic_agent():
    """Get or create topic analysis agent"""
    global topic_agent
    if topic_agent is None:
        topic_agent = TopicAnalysisAgent()
    return topic_agent

@app.post("/topics/analyze")
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

@app.get("/topics/recommendations")
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

@app.get("/topics/gaps")
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

# ------------------------------
# Orchestration Pipeline Endpoints
# ------------------------------
from src.services.orchestration_manager import (
    OrchestrationManager, 
    PipelineConfig, 
    PipelineResult,
    PipelineStatus
)

# Global orchestration manager
orchestration_manager = None

def get_orchestration_manager():
    """Get or create orchestration manager"""
    global orchestration_manager
    if orchestration_manager is None:
        orchestration_manager = OrchestrationManager()
    return orchestration_manager

@app.post("/pipeline/run")
async def run_full_pipeline(config: PipelineConfig):
    """
    Run the complete multi-agent blog generation pipeline
    
    This orchestrates all 5 agents in sequence:
    1. Competitor Monitoring
    2. Topic Analysis
    3. Article Generation
    4. Legal Fact Checking
    5. WordPress Publishing
    """
    manager = get_orchestration_manager()
    
    try:
        logger.info(f"Starting pipeline for topic: {config.topic or 'auto-determined'}")
        result = await manager.run_pipeline(config)
        
        # Generate a pipeline ID based on start time
        pipeline_id = f"pipeline_{result.started_at.strftime('%Y%m%d%H%M%S')}"
        
        # Convert to dict for response
        response = {
            "status": result.status,
            "execution_time": result.execution_time,
            "total_cost": result.total_cost,
            "errors": result.errors,
            "warnings": result.warnings,
            "pipeline_id": pipeline_id
        }
        
        # Add article details if generated
        if result.article:
            response["article"] = {
                "title": result.article.title,
                "word_count": result.article.word_count,
                "seo_score": result.article.seo_score,
                "slug": result.article.slug
            }
        
        # Add fact check summary if performed
        if result.fact_check_report:
            response["fact_check"] = {
                "accuracy_score": result.fact_check_report.overall_accuracy_score,
                "verified_claims": result.fact_check_report.verified_claims,
                "incorrect_claims": result.fact_check_report.incorrect_claims,
                "total_claims": result.fact_check_report.total_claims
            }
        
        # Add WordPress details if published
        if result.wordpress_result and result.wordpress_result.get("success"):
            response["wordpress"] = {
                "post_id": result.wordpress_result["post_id"],
                "edit_link": result.wordpress_result["edit_link"],
                "view_link": result.wordpress_result.get("view_link")
            }
        
        return response
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise HTTPException(500, f"Pipeline execution failed: {str(e)}")

@app.get("/pipeline/status")
async def get_pipeline_status():
    """Get current pipeline execution status"""
    manager = get_orchestration_manager()
    status = manager.get_pipeline_status()
    
    if status:
        return {
            "running": True,
            "status": status,
            "message": f"Pipeline is currently in {status} stage"
        }
    else:
        return {
            "running": False,
            "status": None,
            "message": "No pipeline currently running"
        }

@app.get("/pipeline/history")
async def get_pipeline_history(limit: int = 10):
    """Get recent pipeline execution history"""
    manager = get_orchestration_manager()
    history = manager.get_pipeline_history(limit)
    
    return {
        "executions": [
            {
                "status": h.status,
                "started_at": h.started_at.isoformat(),
                "completed_at": h.completed_at.isoformat() if h.completed_at else None,
                "execution_time": h.execution_time,
                "total_cost": h.total_cost,
                "errors": h.errors
            }
            for h in history
        ],
        "total": len(history)
    }

@app.get("/pipeline/costs")
async def get_pipeline_costs():
    """Get cost summary for pipeline executions"""
    manager = get_orchestration_manager()
    return manager.get_cost_summary()

@app.get("/pipeline/{pipeline_id}/details")
async def get_pipeline_details(pipeline_id: str):
    """Get detailed information about a specific pipeline run"""
    manager = get_orchestration_manager()
    
    # Find the pipeline in history
    for result in manager.pipeline_history:
        # Check if this pipeline matches the ID
        result_id = f"pipeline_{result.started_at.strftime('%Y%m%d%H%M%S')}"
        if result_id == pipeline_id or pipeline_id.startswith(result_id):
            return {
                "pipeline_id": pipeline_id,
                "status": result.status.value,
                "started_at": result.started_at.isoformat(),
                "completed_at": result.completed_at.isoformat() if result.completed_at else None,
                "execution_time": result.execution_time,
                "total_cost": result.total_cost,
                "primary_keyword": result.topic_recommendation.primary_keyword if result.topic_recommendation else None,
                "article": result.article.dict() if result.article else None,
                "topic_recommendation": result.topic_recommendation.dict() if result.topic_recommendation else None,
                "competitor_insights": result.competitor_insights if result.competitor_insights else None,
                "fact_check_report": result.fact_check_report.dict() if result.fact_check_report else None,
                "wordpress_result": result.wordpress_result if result.wordpress_result else None,
                "errors": result.errors,
                "warnings": result.warnings
            }
    
    # Check if it's a saved article file
    import glob
    import json as json_lib
    article_files = glob.glob(f"data/articles/*{pipeline_id}*.json")
    if article_files:
        with open(article_files[0], 'r') as f:
            article_data = json_lib.load(f)
            return {
                "pipeline_id": pipeline_id,
                "status": "completed",
                "started_at": article_data.get('generated_at'),
                "completed_at": article_data.get('generated_at'),
                "execution_time": 0,
                "total_cost": article_data.get('cost_tracking', {}).get('cost', 0),
                "primary_keyword": article_data.get('primary_keyword'),
                "article": article_data,
                "topic_recommendation": {
                    "title": article_data.get('title'),
                    "primary_keyword": article_data.get('primary_keyword'),
                    "secondary_keywords": article_data.get('secondary_keywords', [])
                },
                "competitor_insights": None,
                "fact_check_report": None,
                "wordpress_result": None,
                "errors": [],
                "warnings": []
            }
    
    raise HTTPException(404, f"Pipeline {pipeline_id} not found")

# ------------------------------
# Vector Search Endpoints
# ------------------------------
from src.services.vector_search import VectorSearchManager, SearchResult

# Global vector search manager
vector_manager = None

def get_vector_manager():
    """Get or create vector search manager"""
    global vector_manager
    if vector_manager is None:
        vector_manager = VectorSearchManager()
    return vector_manager

class IndexDocumentRequest(BaseModel):
    content: str
    document_id: str
    title: str
    url: Optional[str] = None
    collection: str = "blog_articles"

@app.post("/vector/index")
async def index_document(request: IndexDocumentRequest):
    """
    Index a document in vector search
    
    Args:
        content: Document content
        document_id: Unique document ID
        title: Document title
        url: Document URL
        collection: Collection to index in
    """
    manager = get_vector_manager()
    
    success = await manager.index_document(
        content=request.content,
        document_id=request.document_id,
        title=request.title,
        url=request.url,
        collection=request.collection
    )
    
    if success:
        return {
            "success": True,
            "message": f"Document {request.document_id} indexed successfully",
            "collection": request.collection
        }
    else:
        raise HTTPException(500, "Failed to index document")

class SearchDocumentsRequest(BaseModel):
    query: str
    limit: int = 5
    collection: str = "blog_articles"

@app.post("/vector/search")
async def search_documents(request: SearchDocumentsRequest):
    """
    Search for similar documents
    
    Args:
        query: Search query
        limit: Number of results
        collection: Collection to search
    """
    manager = get_vector_manager()
    
    results = await manager.search(
        query=request.query,
        limit=request.limit,
        collection=request.collection
    )
    
    return {
        "query": request.query,
        "results": [
            {
                "title": r.document_title,
                "content": r.content[:200] + "...",
                "url": r.document_url,
                "score": r.similarity_score
            }
            for r in results
        ],
        "count": len(results)
    }

@app.post("/vector/check-duplicate")
async def check_duplicate(
    content: str,
    threshold: float = 0.9,
    collection: str = "blog_articles"
):
    """
    Check if content is duplicate
    
    Args:
        content: Content to check
        threshold: Similarity threshold (0.9 = 90% similar)
        collection: Collection to check against
    """
    manager = get_vector_manager()
    
    duplicate = await manager.check_duplicate(
        content=content,
        threshold=threshold,
        collection=collection
    )
    
    if duplicate:
        return {
            "is_duplicate": True,
            "similar_document": {
                "title": duplicate.document_title,
                "url": duplicate.document_url,
                "similarity": duplicate.similarity_score
            }
        }
    else:
        return {
            "is_duplicate": False,
            "message": "No duplicate found"
        }

@app.get("/vector/internal-links")
async def get_internal_links(
    content: str,
    limit: int = 5
):
    """
    Get internal link recommendations based on content
    
    Args:
        content: Content to find links for
        limit: Maximum number of links
    """
    manager = get_vector_manager()
    
    links = await manager.get_internal_links(
        content=content,
        limit=limit
    )
    
    return {
        "links": links,
        "count": len(links)
    }

@app.get("/vector/stats")
async def get_vector_stats(collection: str = "blog_articles"):
    """
    Get collection statistics
    
    Args:
        collection: Collection name
    """
    manager = get_vector_manager()
    stats = manager.get_collection_stats(collection)
    
    return stats

@app.delete("/vector/document/{document_id}")
async def delete_document(
    document_id: str,
    collection: str = "blog_articles"
):
    """
    Delete a document from vector search
    
    Args:
        document_id: Document ID to delete
        collection: Collection to delete from
    """
    manager = get_vector_manager()
    
    success = await manager.delete_document(
        document_id=document_id,
        collection=collection
    )
    
    if success:
        return {
            "success": True,
            "message": f"Document {document_id} deleted"
        }
    else:
        raise HTTPException(500, "Failed to delete document")

# ------------------------------
# Dashboard Routes
# ------------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main dashboard page"""
    try:
        # Get system status
        orchestration_status = get_orchestration_manager()
        vector_manager = get_vector_manager()
        
        # Get basic stats
        pipeline_stats = await orchestration_status.get_pipeline_stats() if orchestration_status else {}
        vector_stats = vector_manager.get_collection_stats() if vector_manager else {}
        
        context = {
            "request": request,
            "title": "Blog Poster Dashboard",
            "pipeline_stats": pipeline_stats,
            "vector_stats": vector_stats,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("dashboard.html", context)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/pipeline", response_class=HTMLResponse)
async def pipeline_dashboard(request: Request):
    """Pipeline monitoring page"""
    try:
        orchestration_status = get_orchestration_manager()
        logger.info(f"Got orchestration manager: {orchestration_status is not None}")
        
        # Get pipeline history using the working API method instead of dashboard method
        pipeline_history_api = orchestration_status.get_pipeline_history(20) if orchestration_status else []
        active_pipelines = await orchestration_status.get_active_pipelines() if orchestration_status else []
        logger.info(f"Pipeline history API returned: {len(pipeline_history_api)} items")
        logger.info(f"Active pipelines: {len(active_pipelines)} items")
        
        # Convert API format to dashboard format
        pipeline_history = []
        for i, result in enumerate(pipeline_history_api):
            pipeline_id = f"pipeline_{result.started_at.strftime('%Y%m%d%H%M%S')}_{i}"
            
            # Extract the primary keyword
            primary_keyword = "Unknown"
            if result.topic_recommendation and hasattr(result.topic_recommendation, 'primary_keyword'):
                primary_keyword = result.topic_recommendation.primary_keyword
            elif result.topic_recommendation and hasattr(result.topic_recommendation, 'topic'):
                primary_keyword = result.topic_recommendation.topic
            
            # Calculate time ago
            now = datetime.now()
            diff = now - result.started_at
            if diff.days > 0:
                time_ago = f"{diff.days} days ago"
            elif diff.seconds > 3600:
                time_ago = f"{diff.seconds // 3600} hours ago"
            elif diff.seconds > 60:
                time_ago = f"{diff.seconds // 60} minutes ago"
            else:
                time_ago = "Just now"
            
            pipeline_history.append({
                "pipeline_id": pipeline_id,
                "primary_keyword": primary_keyword,
                "started_at": result.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "time_ago": time_ago,
                "duration": result.execution_time if result.execution_time else None,
                "status": result.status.value,
                "cost": result.total_cost,
                "article_generated": bool(result.article),
                "article_id": pipeline_id if result.article else None
            })
        
        context = {
            "request": request,
            "title": "Pipeline Monitor",
            "pipeline_history": pipeline_history[:20],  # Last 20 runs
            "active_pipelines": active_pipelines,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("pipeline.html", context)
    except Exception as e:
        logger.error(f"Pipeline dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/pipeline/{pipeline_id}/view", response_class=HTMLResponse)
async def view_pipeline_details(request: Request, pipeline_id: str):
    """View detailed pipeline execution results"""
    try:
        # Get pipeline details from API
        details = await get_pipeline_details(pipeline_id)
        
        # Format the data for the template
        pipeline = {
            "pipeline_id": details["pipeline_id"],
            "status": details["status"],
            "started_at": details["started_at"],
            "completed_at": details["completed_at"],
            "execution_time": details["execution_time"],
            "total_cost": details["total_cost"],
            "primary_keyword": details["primary_keyword"],
            "article_id": pipeline_id,
            "article": details.get("article"),
            "topic_recommendation": details.get("topic_recommendation"),
            "competitor_insights": details.get("competitor_insights"),
            "fact_check_report": details.get("fact_check_report"),
            "wordpress_result": details.get("wordpress_result"),
            "errors": details.get("errors", []),
            "warnings": details.get("warnings", [])
        }
        
        context = {
            "request": request,
            "title": f"Pipeline Details - {pipeline_id}",
            "pipeline": pipeline
        }
        
        return templates.TemplateResponse("pipeline-details.html", context)
    except HTTPException as e:
        if e.status_code == 404:
            return templates.TemplateResponse("error.html", {"request": request, "error": f"Pipeline {pipeline_id} not found"})
        raise
    except Exception as e:
        logger.error(f"Pipeline details error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/articles", response_class=HTMLResponse)
async def articles_dashboard(request: Request):
    """Article management page"""
    try:
        # Get recent articles from cache/database
        import glob
        import json as json_lib
        
        articles = []
        article_files = glob.glob("data/articles/*.json")
        article_files.sort(key=os.path.getmtime, reverse=True)
        
        for file_path in article_files[:50]:  # Last 50 articles
            try:
                with open(file_path, 'r') as f:
                    article_data = json_lib.load(f)
                    article_data['file_path'] = file_path
                    article_data['created_at'] = datetime.fromtimestamp(os.path.getmtime(file_path))
                    articles.append(article_data)
            except Exception:
                continue
        
        context = {
            "request": request,
            "title": "Article Management",
            "articles": articles,
            "total_articles": len(articles),
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("articles.html", context)
    except Exception as e:
        logger.error(f"Articles dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/articles/{article_id}", response_class=HTMLResponse)
async def article_detail(request: Request, article_id: str):
    """Individual article detail page"""
    try:
        # Try to find the article file
        import glob
        import json as json_lib
        
        article_data = None
        
        # Look for article by ID in filenames
        article_files = glob.glob("data/articles/*.json")
        for file_path in article_files:
            filename = os.path.basename(file_path).replace('.json', '')
            # Try exact match first, then partial match
            if article_id == filename or article_id in file_path:
                try:
                    with open(file_path, 'r') as f:
                        article_data = json_lib.load(f)
                        article_data['file_path'] = file_path
                        article_data['created_at'] = datetime.fromtimestamp(os.path.getmtime(file_path))
                        break
                except Exception:
                    continue
        
        if not article_data:
            # If not found, check if it's a current pipeline
            if article_id == "current_pipeline":
                manager = get_orchestration_manager()
                if manager and manager.current_pipeline and manager.current_pipeline.article:
                    article = manager.current_pipeline.article
                    article_data = {
                        "title": article.title,
                        "content_markdown": article.content_markdown,
                        "meta_title": article.meta_title,
                        "meta_description": article.meta_description,
                        "word_count": article.word_count,
                        "seo_score": article.seo_score,
                        "primary_keyword": article.primary_keyword,
                        "slug": article.slug,
                        "created_at": datetime.now(),
                        "status": "In Progress"
                    }
                else:
                    raise HTTPException(404, "Article not found")
            else:
                raise HTTPException(404, "Article not found")
        
        context = {
            "request": request,
            "title": f"Article: {article_data.get('title', 'Unknown')}",
            "article": article_data,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("article-detail.html", context)
    except Exception as e:
        logger.error(f"Article detail error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/health-dashboard", response_class=HTMLResponse)
async def health_dashboard(request: Request):
    """System health monitoring page"""
    try:
        # Check service health
        health_data = {
            "services": {},
            "environment": {},
            "metrics": {}
        }
        
        # Check orchestration manager
        try:
            orchestration_status = get_orchestration_manager()
            health_data["services"]["orchestration"] = "healthy" if orchestration_status else "down"
        except:
            health_data["services"]["orchestration"] = "error"
        
        # Check vector database
        try:
            vector_manager = get_vector_manager()
            collections = vector_manager.get_collection_stats() if vector_manager else {}
            health_data["services"]["qdrant"] = "healthy" if collections else "down"
            health_data["metrics"]["collections"] = collections
        except Exception as e:
            logger.error(f"Qdrant health check error: {e}")
            health_data["services"]["qdrant"] = "error"
            health_data["metrics"]["collections"] = {}
        
        # Check WordPress connection
        try:
            from src.services.wordpress_publisher import WordPressPublisher
            wp_publisher = WordPressPublisher()
            # This would need a health check method
            health_data["services"]["wordpress"] = "unknown"
        except:
            health_data["services"]["wordpress"] = "error"
        
        # Check Bright Data
        health_data["services"]["bright_data"] = "healthy" if os.getenv("BRIGHT_DATA_API_KEY") else "unknown"
        
        # Check Jina AI
        health_data["services"]["jina"] = "healthy" if os.getenv("JINA_API_KEY") else "unknown"
        
        # Environment info
        health_data["environment"] = {
            "anthropic_key": "✓" if os.getenv("ANTHROPIC_API_KEY") else "✗",
            "jina_key": "✓" if os.getenv("JINA_API_KEY") else "✗",
            "bright_data_key": "✓" if os.getenv("BRIGHT_DATA_API_KEY") else "✗",
            "wp_url": os.getenv("WORDPRESS_URL", "not set"),
            "wp_user": os.getenv("WP_USERNAME", "not set")
        }
        
        context = {
            "request": request,
            "title": "System Health",
            "health_data": health_data,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("health.html", context)
    except Exception as e:
        logger.error(f"Health dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/config", response_class=HTMLResponse)
async def config_dashboard(request: Request):
    """Configuration profiles management page"""
    try:
        context = {
            "request": request,
            "title": "Configuration Profiles",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("config-profiles.html", context)
    except Exception as e:
        logger.error(f"Config dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/instructions", response_class=HTMLResponse)
async def instructions_page(request: Request):
    """Instructions and user guide page"""
    try:
        context = {
            "request": request,
            "title": "Instructions & User Guide",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("instructions.html", context)
    except Exception as e:
        logger.error(f"Instructions page error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/features", response_class=HTMLResponse)
async def features_page(request: Request):
    """Features page showing all system capabilities"""
    try:
        context = {
            "request": request,
            "title": "Features",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return templates.TemplateResponse("features.html", context)
    except Exception as e:
        logger.error(f"Features page error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/config/legacy", response_class=HTMLResponse)
async def legacy_config_dashboard(request: Request):
    """Legacy configuration management page"""
    try:
        # Get current configuration
        config_data = {
            "wordpress": {
                "url": os.getenv("WORDPRESS_URL", ""),
                "username": os.getenv("WP_USERNAME", ""),
                "auth_method": os.getenv("WP_AUTH_METHOD", "basic"),
                "verify_ssl": os.getenv("WP_VERIFY_SSL", "true")
            },
            "content": {
                "min_words": os.getenv("ARTICLE_MIN_WORDS", "1500"),
                "max_words": os.getenv("ARTICLE_MAX_WORDS", "2500"),
                "max_cost": os.getenv("MAX_COST_PER_ARTICLE", "15.00"),
                "monthly_budget": os.getenv("MAX_MONTHLY_COST", "500.00")
            },
            "agents": {
                "competitor_monitoring": os.getenv("ENABLE_COMPETITOR_MONITORING", "true") == "true",
                "topic_analysis": os.getenv("ENABLE_TOPIC_ANALYSIS", "true") == "true",
                "fact_checking": os.getenv("ENABLE_FACT_CHECKING", "true") == "true",
                "auto_publish": os.getenv("ENABLE_AUTO_PUBLISH", "false") == "true"
            }
        }
        
        context = {
            "request": request,
            "title": "Configuration",
            "config_data": config_data,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("config.html", context)
    except Exception as e:
        logger.error(f"Config dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

# ------------------------------
# WebSocket for Real-time Logs
# ------------------------------
from src.services.pipeline_logger import pipeline_logger

@app.websocket("/ws/logs/{pipeline_id}")
async def websocket_logs(websocket: WebSocket, pipeline_id: str):
    """WebSocket endpoint for streaming pipeline logs"""
    try:
        await websocket.accept()
        logger.info(f"WebSocket connected for pipeline {pipeline_id}")
        
        # Add this connection to the pipeline logger
        pipeline_logger.add_connection(pipeline_id, websocket)
        
        # Send initial logs if any exist
        existing_logs = pipeline_logger.get_logs(pipeline_id, limit=100)
        if existing_logs:
            await websocket.send_json({
                "type": "initial",
                "logs": existing_logs
            })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for any message from client (heartbeat, etc.)
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_text("pong")
            except WebSocketDisconnect:
                logger.info(f"WebSocket client disconnected for pipeline {pipeline_id}")
                break
            except Exception as e:
                logger.error(f"WebSocket receive error for pipeline {pipeline_id}: {e}")
                break
                
    except Exception as e:
        logger.error(f"WebSocket handler error for pipeline {pipeline_id}: {e}")
        try:
            await websocket.close(code=1000)
        except:
            pass
    finally:
        # Remove connection when done
        try:
            pipeline_logger.remove_connection(pipeline_id, websocket)
        except Exception as e:
            logger.error(f"Error removing WebSocket connection: {e}")
        logger.info(f"WebSocket disconnected for pipeline {pipeline_id}")

@app.get("/logs/{pipeline_id}")
async def get_pipeline_logs(pipeline_id: str, limit: int = 100):
    """Get recent logs for a pipeline"""
    logs = pipeline_logger.get_logs(pipeline_id, limit=limit)
    return {
        "pipeline_id": pipeline_id,
        "logs": logs,
        "count": len(logs)
    }

@app.delete("/logs/{pipeline_id}")
async def clear_pipeline_logs(pipeline_id: str):
    """Clear logs for a pipeline"""
    pipeline_logger.clear_logs(pipeline_id)
    return {
        "success": True,
        "message": f"Logs cleared for pipeline {pipeline_id}"
    }

# ------------------------------
# Cleanup on shutdown
# ------------------------------
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    global competitor_agent, orchestration_manager
    if competitor_agent:
        await competitor_agent.close()
        competitor_agent = None
    if orchestration_manager:
        await orchestration_manager.close()
        orchestration_manager = None


# ------------------------------
# Dev harness
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8088, reload=True)
