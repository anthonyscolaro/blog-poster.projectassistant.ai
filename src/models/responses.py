"""
Standard API response models for consistent frontend integration
"""
from typing import Generic, TypeVar, Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

# Generic type for response data
T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    Standard API response wrapper for all endpoints
    Matches frontend expectations
    """
    data: T
    message: str = "Success"
    success: bool = True
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """
    Standard error response format
    """
    message: str
    success: bool = False
    errors: List[str]
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated response for list endpoints
    """
    data: List[T]
    message: str = "Success"
    success: bool = True
    pagination: Dict[str, Any] = Field(default_factory=dict)
    total: int
    page: int = 1
    per_page: int = 20
    total_pages: int = 1
    
    def __init__(self, **data):
        super().__init__(**data)
        # Calculate total pages
        if self.total and self.per_page:
            self.total_pages = (self.total + self.per_page - 1) // self.per_page
        
        # Build pagination metadata
        self.pagination = {
            "total": self.total,
            "page": self.page,
            "per_page": self.per_page,
            "total_pages": self.total_pages,
            "has_next": self.page < self.total_pages,
            "has_prev": self.page > 1
        }


# Frontend-compatible model mappings with field aliases
class PipelineStatusResponse(BaseModel):
    """
    Pipeline status model with frontend-compatible field names
    """
    id: str = Field(alias="pipeline_id")
    name: str = ""
    status: str
    progress: float = 0.0
    current_agent: str = Field(alias="currentAgent", default="")
    start_time: datetime = Field(alias="startTime")
    end_time: Optional[datetime] = Field(alias="endTime", default=None)
    error: Optional[str] = None
    cost: float = 0.0
    
    class Config:
        populate_by_name = True  # Accept both field names
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ArticleResponse(BaseModel):
    """
    Article model with frontend-compatible field names
    """
    id: str
    title: str
    content: str
    status: str  # 'draft' | 'published' | 'pending'
    word_count: int = Field(alias="wordCount")
    seo_score: float = Field(alias="seoScore")
    published_at: Optional[datetime] = Field(alias="publishedAt", default=None)
    tags: List[str] = Field(default_factory=list)
    meta: Dict[str, Any] = Field(default_factory=dict)
    cost: float = 0.0
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class AgentStatusResponse(BaseModel):
    """
    Agent health status for monitoring
    """
    id: str
    name: str
    status: str  # 'healthy' | 'warning' | 'error' | 'offline'
    last_check: datetime = Field(alias="lastCheck")
    response_time: float = Field(alias="responseTime")
    error_rate: float = Field(alias="errorRate", default=0.0)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SystemMetricsResponse(BaseModel):
    """
    System-wide metrics for dashboard
    """
    total_articles: int = Field(alias="totalArticles")
    success_rate: float = Field(alias="successRate")
    avg_processing_time: float = Field(alias="avgProcessingTime")
    active_pipelines: int = Field(alias="activePipelines")
    monthly_spend: float = Field(alias="monthlySpend")
    api_usage: Dict[str, int] = Field(alias="apiUsage", default_factory=dict)
    
    class Config:
        populate_by_name = True


class OrganizationResponse(BaseModel):
    """
    Organization model for multi-tenancy
    """
    id: str
    name: str
    slug: str
    plan: str  # 'free' | 'starter' | 'professional' | 'enterprise'
    subscription_status: str = Field(alias="subscriptionStatus")
    trial_ends_at: Optional[datetime] = Field(alias="trialEndsAt", default=None)
    articles_limit: int = Field(alias="articlesLimit")
    articles_used: int = Field(alias="articlesUsed")
    monthly_budget: float = Field(alias="monthlyBudget")
    current_month_cost: float = Field(alias="currentMonthCost")
    
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class UserProfileResponse(BaseModel):
    """
    User profile with organization context
    """
    id: str
    email: str
    full_name: Optional[str] = Field(alias="fullName", default=None)
    organization_id: str = Field(alias="organizationId")
    role: str  # 'owner' | 'admin' | 'editor' | 'member' | 'viewer'
    avatar_url: Optional[str] = Field(alias="avatarUrl", default=None)
    onboarding_completed: bool = Field(alias="onboardingCompleted", default=False)
    two_factor_enabled: bool = Field(alias="twoFactorEnabled", default=False)
    
    class Config:
        populate_by_name = True


# Helper function to create standard responses
def create_response(data: Any, message: str = "Success") -> ApiResponse:
    """
    Helper to create a standard API response
    """
    return ApiResponse(data=data, message=message)


def create_error_response(
    message: str,
    errors: List[str] = None,
    error_code: str = None
) -> ErrorResponse:
    """
    Helper to create a standard error response
    """
    return ErrorResponse(
        message=message,
        errors=errors or [message],
        error_code=error_code
    )


def create_paginated_response(
    data: List[Any],
    total: int,
    page: int = 1,
    per_page: int = 20,
    message: str = "Success"
) -> PaginatedResponse:
    """
    Helper to create a paginated response
    """
    return PaginatedResponse(
        data=data,
        total=total,
        page=page,
        per_page=per_page,
        message=message
    )