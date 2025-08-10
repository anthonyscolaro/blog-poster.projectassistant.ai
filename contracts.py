"""
Shared Pydantic data contracts for blog automation agents
"""
from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import List, Optional, Dict, Literal, Any
from datetime import datetime
import hashlib


class CompetitorContent(BaseModel):
    """Normalized competitor content from various sources"""
    id: str
    url: HttpUrl
    domain: str
    fetched_at: datetime
    type: Literal["blog", "news", "social"]
    title: str
    text_md: str
    lang: str = "en"
    engagement: Dict[str, int] = Field(default_factory=dict)
    checksum: str
    source_of_truth: Literal["jina", "brightdata", "other"]
    
    @field_validator('checksum', mode='before')
    def generate_checksum(cls, v, values):
        if not v and 'text_md' in values:
            return hashlib.sha256(values['text_md'].encode()).hexdigest()[:16]
        return v


class TopicRec(BaseModel):
    """Topic recommendation from analysis agent"""
    topic_slug: str
    title_variants: List[str]
    primary_kw: str
    secondary_kws: List[str]
    rationale: str
    supporting_urls: List[HttpUrl]
    score_breakdown: Dict[str, float]
    risk_flags: List[str] = Field(default_factory=list)
    
    @field_validator('topic_slug')
    def validate_slug(cls, v):
        import re
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v


class ArticleDraft(BaseModel):
    """Generated article ready for publishing"""
    title: str = Field(max_length=60)
    slug: str
    category: str
    tags: List[str] = Field(max_items=10)
    meta_title: str = Field(max_length=60)
    meta_desc: str = Field(min_length=120, max_length=160)
    canonical: HttpUrl
    schema_jsonld: Dict[str, Any]
    hero_image_prompt: str
    internal_link_targets: List[HttpUrl]
    markdown: str = Field(min_length=1000)
    citations: List[HttpUrl] = Field(min_items=2)
    jurisdiction: Optional[str] = None
    
    @field_validator('slug')
    def validate_slug(cls, v):
        import re
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v


class FactCheckResult(BaseModel):
    """Legal fact checking result"""
    verified: bool
    confidence_score: float = Field(ge=0, le=1)
    issues_found: List[str] = Field(default_factory=list)
    required_disclaimers: List[str] = Field(default_factory=list)
    jurisdiction_tags: List[str] = Field(default_factory=list)
    verified_citations: List[HttpUrl] = Field(default_factory=list)


class PublishingConfig(BaseModel):
    """WordPress publishing configuration"""
    status: Literal["draft", "pending", "publish", "future"] = "draft"
    scheduled_gmt: Optional[datetime] = None
    featured_image_path: Optional[str] = None
    external_id: str
    force_update: bool = False
    enable_seo_fields: bool = True
    enable_post_automation: bool = True


class PublishingResult(BaseModel):
    """WordPress publishing result"""
    post_id: int
    post_url: HttpUrl
    operation: Literal["created", "updated", "skipped"]
    media_uploaded: bool = False
    seo_fields_set: bool = False
    categories_set: List[int] = Field(default_factory=list)
    tags_set: List[str] = Field(default_factory=list)
    sitemap_pinged: bool = False
    indexnow_submitted: bool = False
    cache_invalidated: bool = False


class MonitoringSchedule(BaseModel):
    """Agent execution schedule"""
    competitor_monitoring: str = "0 */6 * * *"  # Every 6 hours
    topic_analysis: str = "0 8 * * *"  # Daily at 8am
    article_generation: str = "0 9 * * MON,WED,FRI"  # MWF at 9am
    publishing: str = "0 10 * * MON,WED,FRI"  # MWF at 10am


class CostTracking(BaseModel):
    """API cost tracking"""
    article_id: str
    timestamp: datetime
    agent: str
    api_provider: str
    tokens_used: int
    cost_usd: float
    monthly_total: float = 0.0
    
    @field_validator('cost_usd')
    def validate_cost(cls, v):
        if v > 15.0:
            raise ValueError(f'Article cost ${v} exceeds $15 limit')
        return v


class AgentMetrics(BaseModel):
    """Agent performance metrics"""
    agent_name: str
    execution_time_seconds: float
    success: bool
    error_message: Optional[str] = None
    input_size_bytes: int
    output_size_bytes: int
    api_calls_made: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)