"""
Pipeline models for the blog generation system
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from src.models.article_models import (
    Article,
    TopicRecommendation,
    CompetitorInsights,
    FactCheckReport,
    WordPressResult
)


class PipelineStatus(str, Enum):
    """Status of the pipeline execution"""
    PENDING = "pending"
    RUNNING = "running"
    MONITORING = "monitoring_competitors"
    ANALYZING = "analyzing_topics"
    GENERATING = "generating_article"
    FACT_CHECKING = "fact_checking"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelineResult(BaseModel):
    """Result from a complete pipeline execution"""
    pipeline_id: str
    status: PipelineStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    
    # Components
    competitor_insights: Optional[CompetitorInsights] = None
    topic_recommendation: Optional[TopicRecommendation] = None
    article: Optional[Article] = None
    fact_check_report: Optional[FactCheckReport] = None
    wordpress_result: Optional[WordPressResult] = None
    
    # Metrics
    total_cost: float = 0.0
    llm_tokens_used: int = 0
    api_calls_made: int = 0
    
    # Errors and warnings
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)