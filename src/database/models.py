"""
Database models for blog-poster application
Using SQLAlchemy with PostgreSQL and pgvector
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from datetime import datetime

Base = declarative_base()


class Article(Base):
    """Article model for storing generated content"""
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    
    # Content fields
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    content_markdown = Column(Text, nullable=False)
    content_html = Column(Text)
    excerpt = Column(Text)
    
    # SEO fields
    meta_title = Column(String(160))
    meta_description = Column(String(320))
    primary_keyword = Column(String(100))
    secondary_keywords = Column(JSON)
    seo_score = Column(Float)
    
    # WordPress fields
    wp_post_id = Column(Integer)
    wp_url = Column(String(500))
    wp_status = Column(String(50))
    wp_categories = Column(JSON)
    wp_tags = Column(JSON)
    
    # Analytics
    word_count = Column(Integer)
    reading_time = Column(Integer)
    internal_links = Column(Integer, default=0)
    external_links = Column(Integer, default=0)
    
    # Pipeline reference
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'))
    pipeline = relationship("Pipeline", back_populates="article")
    
    # Status and timestamps
    status = Column(String(50), default='draft', index=True)
    published_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Vector embedding for semantic search (1536 dimensions for OpenAI embeddings)
    embedding = Column(Vector(1536))
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content_markdown': self.content_markdown,
            'content_html': self.content_html,
            'excerpt': self.excerpt,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'primary_keyword': self.primary_keyword,
            'secondary_keywords': self.secondary_keywords,
            'seo_score': self.seo_score,
            'wp_post_id': self.wp_post_id,
            'wp_url': self.wp_url,
            'wp_status': self.wp_status,
            'word_count': self.word_count,
            'reading_time': self.reading_time,
            'status': self.status,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', status='{self.status}')>"


class Pipeline(Base):
    """Pipeline execution tracking"""
    __tablename__ = 'pipelines'
    
    id = Column(Integer, primary_key=True)
    pipeline_id = Column(String(100), unique=True, index=True)  # For backward compatibility
    
    # Execution details
    status = Column(String(50), default='pending', index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    execution_time_seconds = Column(Float)
    
    # Configuration and results
    input_config = Column(JSON, nullable=False)
    competitor_data = Column(JSON)
    topic_recommendation = Column(JSON)
    fact_check_report = Column(JSON)
    wordpress_result = Column(JSON)
    
    # Cost tracking
    total_cost = Column(Float, default=0.0)
    llm_tokens_used = Column(Integer, default=0)
    api_calls_made = Column(Integer, default=0)
    
    # Error handling
    errors = Column(JSON)
    warnings = Column(JSON)
    retry_count = Column(Integer, default=0)
    
    # Relationships
    article = relationship("Article", back_populates="pipeline", uselist=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'pipeline_id': self.pipeline_id,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'execution_time_seconds': self.execution_time_seconds,
            'total_cost': self.total_cost,
            'llm_tokens_used': self.llm_tokens_used,
            'api_calls_made': self.api_calls_made,
            'errors': self.errors,
            'warnings': self.warnings,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<Pipeline(id={self.id}, status='{self.status}', cost={self.total_cost})>"


class ApiKey(Base):
    """Encrypted API key storage"""
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True)
    
    # Key identification
    service = Column(String(100), nullable=False, unique=True, index=True)
    encrypted_key = Column(Text, nullable=False)
    key_preview = Column(String(20))  # First/last 4 chars for display
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime)
    usage_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime)
    
    def __repr__(self):
        return f"<ApiKey(service='{self.service}', active={self.is_active})>"


class CompetitorArticle(Base):
    """Track competitor articles for analysis"""
    __tablename__ = 'competitor_articles'
    
    id = Column(Integer, primary_key=True)
    
    # Source information
    competitor_domain = Column(String(255), nullable=False, index=True)
    url = Column(String(500), unique=True, nullable=False)
    
    # Article details
    title = Column(String(500))
    published_date = Column(DateTime)
    author = Column(String(255))
    
    # Content analysis
    content_snippet = Column(Text)  # First 500 chars for preview
    word_count = Column(Integer)
    main_topics = Column(JSON)
    keywords = Column(JSON)
    
    # Performance metrics
    social_shares = Column(Integer)
    estimated_traffic = Column(Integer)
    
    # Tracking
    discovered_at = Column(DateTime, server_default=func.now())
    analyzed_at = Column(DateTime)
    
    # Vector embedding for similarity comparison
    embedding = Column(Vector(1536))
    
    def __repr__(self):
        return f"<CompetitorArticle(domain='{self.competitor_domain}', title='{self.title}')>"


# Create indexes for better query performance
Index('idx_articles_status_created', Article.status, Article.created_at.desc())
Index('idx_pipelines_status_created', Pipeline.status, Pipeline.created_at.desc())
Index('idx_competitor_domain_discovered', CompetitorArticle.competitor_domain, CompetitorArticle.discovered_at.desc())