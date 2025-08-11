"""
Application configuration management with environment-specific settings
"""
import os
from typing import Optional, Dict, Any
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from enum import Enum


class Environment(str, Enum):
    """Application environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    """
    Application settings with validation and environment management
    """
    
    # Environment
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        env="APP_ENV"
    )
    
    # Application
    app_name: str = Field(default="Blog Poster", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # API Settings
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8088"],
        env="CORS_ORIGINS"
    )
    
    # Database
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    db_pool_size: int = Field(default=20, env="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=40, env="DB_MAX_OVERFLOW")
    db_pool_timeout: int = Field(default=30, env="DB_POOL_TIMEOUT")
    db_echo_sql: bool = Field(default=False, env="DB_ECHO_SQL")
    
    # Redis Cache
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    redis_ttl: int = Field(default=3600, env="REDIS_TTL")  # 1 hour default
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    api_encryption_key: Optional[str] = Field(default=None, env="API_ENCRYPTION_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE")
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_period: int = Field(default=60, env="RATE_LIMIT_PERIOD")  # seconds
    
    # API Keys (loaded from DB in production)
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    jina_api_key: Optional[str] = Field(default=None, env="JINA_API_KEY")
    bright_data_api_key: Optional[str] = Field(default=None, env="BRIGHT_DATA_API_KEY")
    
    # WordPress Configuration
    wordpress_url: Optional[str] = Field(default=None, env="WORDPRESS_URL")
    wp_username: Optional[str] = Field(default=None, env="WP_USERNAME")
    wp_app_password: Optional[str] = Field(default=None, env="WP_APP_PASSWORD")
    wp_verify_ssl: bool = Field(default=True, env="WP_VERIFY_SSL")
    
    # Cost Management
    max_cost_per_article: float = Field(default=0.50, env="MAX_COST_PER_ARTICLE")
    max_monthly_cost: float = Field(default=100.00, env="MAX_MONTHLY_COST")
    cost_alert_threshold: float = Field(default=0.8, env="COST_ALERT_THRESHOLD")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Backup
    backup_enabled: bool = Field(default=True, env="BACKUP_ENABLED")
    backup_retention_days: int = Field(default=30, env="BACKUP_RETENTION_DAYS")
    
    @validator("database_url", pre=True)
    def build_database_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Build database URL from components if not provided"""
        if v:
            # Convert postgresql:// to postgresql+psycopg2://
            if v.startswith("postgresql://"):
                return v.replace("postgresql://", "postgresql+psycopg2://", 1)
            return v
        
        # Build from components
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5433")
        db_name = os.getenv("DB_NAME", "blog_poster")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "postgres")
        
        return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    @validator("redis_url", pre=True)
    def build_redis_url(cls, v: Optional[str]) -> str:
        """Build Redis URL if not provided"""
        if v:
            return v
        
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = os.getenv("REDIS_PORT", "6384")
        redis_password = os.getenv("REDIS_PASSWORD", "")
        
        if redis_password:
            return f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
        return f"redis://{redis_host}:{redis_port}/0"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == Environment.PRODUCTION
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing"""
        return self.environment == Environment.TESTING
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Allow extra fields for flexibility
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    
    Returns:
        Settings: Application settings
    """
    return Settings()


# Export for convenience
settings = get_settings()