name: "Data Persistence Layer - Production Database Implementation"
description: |

## Purpose
Transform the blog-poster application from file-based storage to a production-ready database system with proper models, migrations, and data integrity.

## Core Principles
1. **Data Integrity**: ACID compliance for critical operations
2. **Scalability**: Handle thousands of articles and pipeline runs
3. **Performance**: Optimized queries and proper indexing
4. **Maintainability**: Clear schema migrations and documentation

---

## Goal
Replace all file-based storage (JSON files, in-memory state) with PostgreSQL database models and implement proper data persistence patterns.

## Why
- **Current Issues**: Articles lost on restart, no query capabilities, no concurrent access
- **Production Need**: Multi-user support, data analytics, backup/restore
- **Scale Requirements**: Support millions of articles, search across all content
- **Compliance**: Audit trails for content generation and publishing

## What
PostgreSQL database with SQLAlchemy ORM models for:
- Articles (drafts, published, archived)
- Pipeline executions and history
- Competitor monitoring data
- User management and authentication
- API keys and configuration
- Cost tracking and analytics

### Success Criteria
- [ ] All data persisted to PostgreSQL
- [ ] Zero data loss on application restart
- [ ] Database migrations with Alembic
- [ ] Connection pooling configured
- [ ] Backup and restore procedures
- [ ] Query performance < 100ms for common operations
- [ ] Full-text search on articles
- [ ] Data retention policies implemented

## All Needed Context

### Current State Analysis
```yaml
Current Storage:
  Articles:
    location: data/articles/*.json
    issues: 
      - No concurrent access control
      - No versioning
      - Lost on container rebuild
      
  Pipeline History:
    location: In-memory list
    issues:
      - Lost on restart
      - No persistence
      - Limited to last 100 entries
      
  Configuration:
    location: .env files
    issues:
      - No audit trail
      - No multi-tenant support
      - Secrets in plain text
```

### Database Schema Design
```sql
-- Core Tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    pipeline_id UUID REFERENCES pipelines(id),
    
    -- Content fields
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    content_markdown TEXT NOT NULL,
    content_html TEXT,
    excerpt TEXT,
    
    -- SEO fields
    meta_title VARCHAR(160),
    meta_description VARCHAR(320),
    primary_keyword VARCHAR(100),
    secondary_keywords JSONB,
    seo_score DECIMAL(3,2),
    
    -- WordPress fields
    wp_post_id INTEGER,
    wp_url VARCHAR(500),
    wp_status VARCHAR(50),
    
    -- Analytics
    word_count INTEGER,
    reading_time INTEGER,
    internal_links INTEGER,
    external_links INTEGER,
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'draft',
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Full-text search
    search_vector tsvector,
    
    INDEXES:
    - idx_articles_slug ON slug
    - idx_articles_status ON status
    - idx_articles_created ON created_at DESC
    - idx_articles_search ON search_vector USING GIN
);

CREATE TABLE pipelines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    
    -- Execution details
    status VARCHAR(50) DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    execution_time_ms INTEGER,
    
    -- Pipeline data
    input_config JSONB NOT NULL,
    competitor_data JSONB,
    topic_recommendation JSONB,
    fact_check_report JSONB,
    wordpress_result JSONB,
    
    -- Cost tracking
    total_cost DECIMAL(10,4),
    llm_tokens_used INTEGER,
    api_calls_made INTEGER,
    
    -- Error handling
    errors JSONB,
    warnings JSONB,
    retry_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE competitors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    
    -- Monitoring config
    is_active BOOLEAN DEFAULT true,
    check_frequency_hours INTEGER DEFAULT 24,
    last_checked_at TIMESTAMP,
    
    -- Statistics
    total_articles_found INTEGER DEFAULT 0,
    new_articles_30d INTEGER DEFAULT 0,
    trending_topics JSONB,
    
    -- Metadata
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE competitor_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    competitor_id UUID REFERENCES competitors(id),
    
    url VARCHAR(500) UNIQUE NOT NULL,
    title VARCHAR(500),
    published_date DATE,
    author VARCHAR(255),
    
    -- Content analysis
    word_count INTEGER,
    main_topics JSONB,
    keywords JSONB,
    
    -- Performance metrics
    social_shares INTEGER,
    backlinks INTEGER,
    
    discovered_at TIMESTAMP DEFAULT NOW(),
    analyzed_at TIMESTAMP
);

CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    
    service VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    key_preview VARCHAR(20),
    
    is_active BOOLEAN DEFAULT true,
    last_used_at TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE TABLE cost_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pipeline_id UUID REFERENCES pipelines(id),
    
    service VARCHAR(100) NOT NULL,
    operation VARCHAR(255),
    
    cost DECIMAL(10,6) NOT NULL,
    tokens_used INTEGER,
    
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### Implementation Tasks

#### Phase 1: Database Setup
```python
# src/database/models.py
from sqlalchemy import create_engine, Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False)
    content_markdown = Column(Text, nullable=False)
    # ... rest of fields

# src/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=40)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Phase 2: Migration System
```bash
# Setup Alembic
alembic init migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

#### Phase 3: Repository Pattern
```python
# src/repositories/article_repository.py
class ArticleRepository:
    def __init__(self, db_session):
        self.db = db_session
    
    def create(self, article_data: dict) -> Article:
        article = Article(**article_data)
        self.db.add(article)
        self.db.commit()
        return article
    
    def find_by_slug(self, slug: str) -> Optional[Article]:
        return self.db.query(Article).filter_by(slug=slug).first()
    
    def search(self, query: str, limit: int = 10):
        return self.db.query(Article).filter(
            Article.search_vector.match(query)
        ).limit(limit).all()
```

#### Phase 4: Data Migration
```python
# scripts/migrate_json_to_db.py
import json
import glob
from pathlib import Path

def migrate_articles():
    """Migrate existing JSON articles to database"""
    article_files = glob.glob('data/articles/*.json')
    
    with get_db() as db:
        repo = ArticleRepository(db)
        
        for file_path in article_files:
            with open(file_path) as f:
                data = json.load(f)
                repo.create(data)
```

### Testing Requirements
```python
# tests/test_database.py
def test_article_crud():
    """Test article creation, read, update, delete"""
    
def test_pipeline_tracking():
    """Test pipeline execution tracking"""
    
def test_concurrent_access():
    """Test multiple concurrent database operations"""
    
def test_transaction_rollback():
    """Test transaction rollback on error"""
```

### Performance Optimization
```yaml
Indexes:
  - articles.slug (unique)
  - articles.created_at DESC
  - articles.status
  - pipelines.status, created_at DESC
  - Full-text search on content

Connection Pool:
  - Min: 5 connections
  - Max: 20 connections
  - Overflow: 20 connections
  
Query Optimization:
  - Use eager loading for relationships
  - Implement query result caching
  - Batch inserts for bulk operations
```

### Deployment Considerations
```yaml
Digital Ocean Managed Database:
  - PostgreSQL 15+
  - 2GB RAM minimum
  - Automated backups
  - Read replicas for scaling
  
Environment Variables:
  DATABASE_URL: postgresql://user:pass@host:5432/blogposter
  DATABASE_POOL_SIZE: 20
  DATABASE_MAX_OVERFLOW: 40
  
Migration Strategy:
  1. Deploy database schema
  2. Run data migration script
  3. Switch application to use database
  4. Verify all operations
  5. Archive JSON files
```

### Monitoring & Maintenance
```yaml
Metrics to Track:
  - Query performance (p50, p95, p99)
  - Connection pool utilization
  - Database size growth
  - Slow query log
  
Maintenance Tasks:
  - Daily backups
  - Weekly VACUUM ANALYZE
  - Monthly index optimization
  - Quarterly data archival
```

---

## Implementation Priority
1. **Week 1**: Database models and basic CRUD
2. **Week 2**: Migration system and data import
3. **Week 3**: Repository pattern and testing
4. **Week 4**: Performance optimization and monitoring

## Success Metrics
- Zero data loss incidents
- Query response time < 100ms (p95)
- 99.9% database uptime
- Successful daily backups
- Support for 10,000+ articles