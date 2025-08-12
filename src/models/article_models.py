"""
Article generation models for blog poster
Compatible with both file-based and database-backed systems
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ArticleRequest(BaseModel):
    """Request to generate an article"""
    topic: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    target_word_count: int = 2000
    auto_publish: bool = False
    custom_instructions: Optional[str] = None


class Article(BaseModel):
    """Generated article content"""
    title: str
    slug: str
    content_markdown: str
    content_html: Optional[str] = None
    excerpt: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    primary_keyword: Optional[str] = None
    secondary_keywords: List[str] = Field(default_factory=list)
    seo_score: float = 0.0
    word_count: int = 0
    reading_time: int = 0
    internal_links_count: int = 0
    external_links_count: int = 0


class TopicRecommendation(BaseModel):
    """Topic recommendation from analysis"""
    topic: str
    primary_keyword: str
    secondary_keywords: List[str] = Field(default_factory=list)
    search_volume: Optional[int] = None
    competition_level: Optional[str] = None
    content_type: str = "article"


class CompetitorInsights(BaseModel):
    """Insights from competitor analysis"""
    competitors_analyzed: int
    trending_topics: List[str] = Field(default_factory=list)
    content_gaps: List[str] = Field(default_factory=list)
    recommended_keywords: List[str] = Field(default_factory=list)


class FactCheckReport(BaseModel):
    """Fact checking report"""
    is_approved: bool
    accuracy_score: float
    issues_found: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    legal_citations_verified: bool = True
    # Compatibility fields
    overall_accuracy_score: Optional[float] = None
    verified_claims: int = 0
    incorrect_claims: int = 0
    total_claims: int = 0
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.overall_accuracy_score is None:
            self.overall_accuracy_score = self.accuracy_score


class WordPressResult(BaseModel):
    """WordPress publishing result"""
    success: bool
    post_id: Optional[int] = None
    post_url: Optional[str] = None
    edit_url: Optional[str] = None
    error: Optional[str] = None