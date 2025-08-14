# Architecture Standardization Plan

**Project**: Blog-Poster  
**Date**: August 13, 2025  
**Objective**: Achieve consistent architecture across all environments  
**Timeline**: 3 weeks  
**Priority**: P1 (High)

## 🎯 Standardization Goals

1. **Environment Parity**: Identical service architecture across dev/staging/production
2. **Service Simplification**: Reduce operational complexity
3. **Deployment Consistency**: Single deployment pattern for all environments
4. **Performance Optimization**: Consistent performance characteristics
5. **Cost Efficiency**: Optimize for both development and production costs

## 🏗️ Target Architecture: Supabase-Centric

### Rationale for Supabase Selection

After analyzing the three architectural approaches in the current codebase, **Supabase-centric architecture** is recommended because:

1. **Most Complete Implementation**: Development environment already uses Supabase stack
2. **Integrated Ecosystem**: Auth, database, storage, real-time in one platform
3. **pgvector Native Support**: Built-in vector search capabilities
4. **Operational Simplicity**: Managed services reduce DevOps overhead
5. **Development Velocity**: Rapid prototyping and iteration capabilities

### Standardized Service Architecture

```mermaid
graph TB
    subgraph "All Environments"
        A[Blog-Poster API] --> B[Supabase Database]
        A --> C[Supabase Auth]
        A --> D[Redis Cache]
        A --> E[WordPress Site]
        
        B --> F[pgvector Extension]
        B --> G[Application Tables]
        
        C --> H[JWT Tokens]
        C --> I[User Management]
        
        D --> J[Session Cache]
        D --> K[Queue Management]
    end
    
    subgraph "Environment-Specific"
        L[Development: Local Supabase]
        M[Staging: Supabase Cloud]
        N[Production: Supabase Cloud]
    end
```

### Service Component Matrix

| Component | Development | Staging | Production |
|-----------|-------------|---------|------------|
| **API Server** | Docker Local | DO App Platform | DO App Platform |
| **Database** | Supabase Local | Supabase Cloud | Supabase Cloud |
| **Vector Search** | pgvector | pgvector | pgvector |
| **Auth** | Supabase Auth | Supabase Auth | Supabase Auth |
| **Cache** | Redis Local | Redis Cloud | Redis Cloud |
| **Storage** | Supabase Storage | Supabase Storage | Supabase Storage |
| **WordPress** | Local Instance | Staging Site | Production Site |

## 📋 Implementation Plan

### Phase 1: Foundation Setup (Week 1)

#### 1.1 Supabase Project Structure
```bash
#!/bin/bash
# setup-supabase-projects.sh

echo "🏗️ Setting up Supabase project structure..."

# Install Supabase CLI
npm install -g supabase

# Initialize Supabase configuration
supabase init

# Create project structure
mkdir -p supabase/{migrations,seed,functions}

# Set up local development
supabase start

echo "✅ Supabase foundation ready"
```

#### 1.2 Database Schema Standardization
```sql
-- supabase/migrations/001_initial_schema.sql
-- Standardized database schema for all environments

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Articles table with vector embeddings
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    content_markdown TEXT NOT NULL,
    content_html TEXT,
    excerpt TEXT,
    
    -- SEO fields
    meta_title VARCHAR(160),
    meta_description VARCHAR(320),
    primary_keyword VARCHAR(100),
    secondary_keywords JSONB DEFAULT '[]',
    seo_score FLOAT,
    
    -- WordPress integration
    wp_post_id INTEGER,
    wp_url VARCHAR(500),
    wp_status VARCHAR(50),
    wp_categories JSONB DEFAULT '[]',
    wp_tags JSONB DEFAULT '[]',
    
    -- Analytics
    word_count INTEGER,
    reading_time INTEGER,
    internal_links INTEGER DEFAULT 0,
    external_links INTEGER DEFAULT 0,
    
    -- Pipeline tracking
    pipeline_id UUID REFERENCES pipelines(id),
    
    -- Status and timestamps
    status VARCHAR(50) DEFAULT 'draft',
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Vector embedding for semantic search
    embedding VECTOR(1536)
);

-- Pipelines table for workflow tracking
CREATE TABLE pipelines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pipeline_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Execution details
    status VARCHAR(50) DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    execution_time_seconds FLOAT,
    
    -- Configuration and results
    input_config JSONB NOT NULL,
    competitor_data JSONB,
    topic_recommendation JSONB,
    fact_check_report JSONB,
    wordpress_result JSONB,
    
    -- Cost tracking
    total_cost FLOAT DEFAULT 0.0,
    llm_tokens_used INTEGER DEFAULT 0,
    api_calls_made INTEGER DEFAULT 0,
    
    -- Error handling
    errors JSONB,
    warnings JSONB,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- API keys table (encrypted)
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service VARCHAR(100) UNIQUE NOT NULL,
    encrypted_key TEXT NOT NULL,
    key_preview VARCHAR(20),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_used_at TIMESTAMPTZ,
    usage_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

-- Competitor articles table
CREATE TABLE competitor_articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Source information
    competitor_domain VARCHAR(255) NOT NULL,
    url VARCHAR(500) UNIQUE NOT NULL,
    
    -- Article details
    title VARCHAR(500),
    published_date TIMESTAMPTZ,
    author VARCHAR(255),
    
    -- Content analysis
    content_snippet TEXT,
    word_count INTEGER,
    main_topics JSONB DEFAULT '[]',
    keywords JSONB DEFAULT '[]',
    
    -- Performance metrics
    social_shares INTEGER,
    estimated_traffic INTEGER,
    
    -- Tracking
    discovered_at TIMESTAMPTZ DEFAULT NOW(),
    analyzed_at TIMESTAMPTZ,
    
    -- Vector embedding for similarity comparison
    embedding VECTOR(1536)
);

-- Indexes for performance
CREATE INDEX idx_articles_status_created ON articles(status, created_at DESC);
CREATE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_articles_embedding ON articles USING ivfflat (embedding vector_cosine_ops);

CREATE INDEX idx_pipelines_status_created ON pipelines(status, created_at DESC);
CREATE INDEX idx_pipelines_pipeline_id ON pipelines(pipeline_id);

CREATE INDEX idx_competitor_domain_discovered ON competitor_articles(competitor_domain, discovered_at DESC);
CREATE INDEX idx_competitor_embedding ON competitor_articles USING ivfflat (embedding vector_cosine_ops);

-- Row Level Security (RLS) for Supabase
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE pipelines ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitor_articles ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (to be refined based on auth requirements)
CREATE POLICY "Enable read access for all users" ON articles FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users only" ON articles FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Enable read access for all users" ON pipelines FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users only" ON pipelines FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_articles_updated_at BEFORE UPDATE ON articles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pipelines_updated_at BEFORE UPDATE ON pipelines
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

#### 1.3 Configuration Standardization
```python
# src/core/config.py
"""Standardized configuration for all environments"""

import os
from typing import Optional, Literal
from pydantic_settings import BaseSettings

Environment = Literal["development", "staging", "production"]

class BaseConfig(BaseSettings):
    """Base configuration shared across all environments"""
    
    # Application
    app_name: str = "blog-poster"
    version: str = "1.0.0"
    
    # Environment
    environment: Environment = "development"
    debug: bool = False
    
    # Database (Supabase)
    database_url: str
    supabase_url: str 
    supabase_anon_key: str
    supabase_service_key: str
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Vector Search
    vector_dimensions: int = 1536
    
    # WordPress
    wordpress_url: str
    wp_username: str
    wp_app_password: str
    wp_verify_ssl: bool = True
    
    # AI APIs (retrieved from secrets manager)
    # These will be loaded dynamically, not from environment
    
    # Costs
    max_cost_per_article: float = 0.50
    max_monthly_cost: float = 100.00
    
    # Feature flags
    enable_competitor_monitoring: bool = True
    enable_topic_analysis: bool = True
    enable_fact_checking: bool = True
    enable_auto_publish: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class DevelopmentConfig(BaseConfig):
    """Development environment configuration"""
    environment: Environment = "development"
    debug: bool = True
    
    # Local Supabase
    database_url: str = "postgresql://postgres:postgres@localhost:54322/postgres"
    supabase_url: str = "http://localhost:54321"
    supabase_anon_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0"
    supabase_service_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
    
    # Local WordPress
    wordpress_url: str = "http://localhost:8084"
    wp_verify_ssl: bool = False
    
    # Development features
    enable_auto_publish: bool = False  # Never auto-publish in dev

class StagingConfig(BaseConfig):
    """Staging environment configuration"""
    environment: Environment = "staging"
    debug: bool = False
    
    # Staging Supabase project
    # These will be set via environment variables
    wordpress_url: str = "https://staging-wp.servicedogus.org"
    
    # Staging features
    enable_auto_publish: bool = False  # Manual approval in staging

class ProductionConfig(BaseConfig):
    """Production environment configuration"""
    environment: Environment = "production"
    debug: bool = False
    
    # Production Supabase project
    # All sensitive values from secrets manager
    wordpress_url: str = "https://servicedogus.com"
    
    # Production features
    enable_auto_publish: bool = True  # Can auto-publish in production

def get_config() -> BaseConfig:
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "development":
        return DevelopmentConfig()
    elif env == "staging":
        return StagingConfig()
    elif env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()  # Default fallback

# Global config instance
config = get_config()
```

### Phase 2: Service Migration (Week 2)

#### 2.1 Docker Compose Standardization
```yaml
# docker-compose.yml (Development)
version: '3.8'

services:
  api:
    build: .
    container_name: blog-poster-api
    ports:
      - "8088:8088"
    environment:
      ENVIRONMENT: development
      DATABASE_URL: postgresql://postgres:postgres@supabase-db:5432/postgres
      SUPABASE_URL: http://supabase-kong:8000
      SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY}
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
      REDIS_URL: redis://redis:6379
      WORDPRESS_URL: http://host.docker.internal:8084
    volumes:
      - ./:/app
    depends_on:
      supabase-db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8088/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Supabase stack (unchanged from current implementation)
  supabase-db:
    image: supabase/postgres:15.1.0.117
    container_name: supabase-db
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: postgres
    ports:
      - "54322:5432"
    volumes:
      - supabase-db-data:/var/lib/postgresql/data
      - ./supabase/migrations:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 10

  supabase-kong:
    image: kong:2.8.1
    container_name: supabase-kong
    restart: unless-stopped
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /var/lib/kong/kong.yml
    ports:
      - "54321:8000"
    volumes:
      - ./supabase/kong.yml:/var/lib/kong/kong.yml:ro

  redis:
    image: redis:7-alpine
    container_name: blog-poster-redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  supabase-db-data:
  redis-data:
```

```yaml
# docker-compose.staging.yml (Staging)
version: '3.8'

services:
  api:
    image: blog-poster-api:staging
    build:
      context: .
      dockerfile: Dockerfile
    container_name: blog-poster-staging
    ports:
      - "80:8088"
    environment:
      ENVIRONMENT: staging
      DATABASE_URL: ${SUPABASE_DATABASE_URL}
      SUPABASE_URL: ${SUPABASE_URL}
      SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY}
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
      REDIS_URL: ${REDIS_URL}
      WORDPRESS_URL: https://staging-wp.servicedogus.org
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8088/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # No local database services - using Supabase Cloud
  # No local Redis - using managed Redis
```

#### 2.2 Database Migration Scripts
```python
# scripts/migrate-to-supabase.py
"""Migrate existing data to standardized Supabase schema"""

import asyncio
import asyncpg
import json
from typing import Dict, List, Any
from datetime import datetime

class DatabaseMigrator:
    def __init__(self, source_url: str, target_url: str):
        self.source_url = source_url
        self.target_url = target_url
        
    async def migrate_all(self):
        """Migrate all data from source to target database"""
        print("🚀 Starting database migration...")
        
        # Connect to databases
        source_conn = await asyncpg.connect(self.source_url)
        target_conn = await asyncpg.connect(self.target_url)
        
        try:
            # Migrate articles
            await self.migrate_articles(source_conn, target_conn)
            
            # Migrate pipelines
            await self.migrate_pipelines(source_conn, target_conn)
            
            # Migrate competitor data
            await self.migrate_competitor_articles(source_conn, target_conn)
            
            print("✅ Migration completed successfully")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise
        finally:
            await source_conn.close()
            await target_conn.close()
    
    async def migrate_articles(self, source: asyncpg.Connection, target: asyncpg.Connection):
        """Migrate articles table"""
        print("📝 Migrating articles...")
        
        # Get articles from source
        articles = await source.fetch("SELECT * FROM articles")
        
        migrated_count = 0
        for article in articles:
            try:
                # Convert to new schema format
                await target.execute("""
                    INSERT INTO articles (
                        id, title, slug, content_markdown, content_html,
                        meta_title, meta_description, primary_keyword,
                        secondary_keywords, seo_score, wp_post_id, wp_url,
                        word_count, reading_time, status, published_at,
                        created_at, updated_at, embedding
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
                        $11, $12, $13, $14, $15, $16, $17, $18, $19
                    )
                """, 
                    article['id'],
                    article['title'],
                    article['slug'],
                    article['content_markdown'],
                    article.get('content_html'),
                    article.get('meta_title'),
                    article.get('meta_description'),
                    article.get('primary_keyword'),
                    json.dumps(article.get('secondary_keywords', [])),
                    article.get('seo_score'),
                    article.get('wp_post_id'),
                    article.get('wp_url'),
                    article.get('word_count'),
                    article.get('reading_time'),
                    article.get('status', 'draft'),
                    article.get('published_at'),
                    article.get('created_at', datetime.utcnow()),
                    article.get('updated_at', datetime.utcnow()),
                    article.get('embedding')
                )
                migrated_count += 1
                
            except Exception as e:
                print(f"⚠️ Failed to migrate article {article['id']}: {e}")
        
        print(f"✅ Migrated {migrated_count} articles")
    
    async def migrate_pipelines(self, source: asyncpg.Connection, target: asyncpg.Connection):
        """Migrate pipelines table"""
        print("⚙️ Migrating pipelines...")
        
        # Similar migration logic for pipelines
        pipelines = await source.fetch("SELECT * FROM pipelines")
        
        migrated_count = 0
        for pipeline in pipelines:
            try:
                await target.execute("""
                    INSERT INTO pipelines (
                        id, pipeline_id, status, started_at, completed_at,
                        input_config, total_cost, created_at, updated_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                    pipeline['id'],
                    pipeline['pipeline_id'],
                    pipeline.get('status', 'pending'),
                    pipeline.get('started_at'),
                    pipeline.get('completed_at'),
                    json.dumps(pipeline.get('input_config', {})),
                    pipeline.get('total_cost', 0.0),
                    pipeline.get('created_at', datetime.utcnow()),
                    pipeline.get('updated_at', datetime.utcnow())
                )
                migrated_count += 1
                
            except Exception as e:
                print(f"⚠️ Failed to migrate pipeline {pipeline['id']}: {e}")
        
        print(f"✅ Migrated {migrated_count} pipelines")
    
    async def migrate_competitor_articles(self, source: asyncpg.Connection, target: asyncpg.Connection):
        """Migrate competitor articles if they exist"""
        print("🔍 Migrating competitor articles...")
        
        try:
            competitors = await source.fetch("SELECT * FROM competitor_articles")
            migrated_count = 0
            
            for competitor in competitors:
                try:
                    await target.execute("""
                        INSERT INTO competitor_articles (
                            id, competitor_domain, url, title, content_snippet,
                            discovered_at, embedding
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                        competitor['id'],
                        competitor['competitor_domain'],
                        competitor['url'],
                        competitor.get('title'),
                        competitor.get('content_snippet'),
                        competitor.get('discovered_at', datetime.utcnow()),
                        competitor.get('embedding')
                    )
                    migrated_count += 1
                    
                except Exception as e:
                    print(f"⚠️ Failed to migrate competitor {competitor['id']}: {e}")
            
            print(f"✅ Migrated {migrated_count} competitor articles")
            
        except Exception:
            print("ℹ️ No competitor articles table found - skipping")

async def main():
    """Run migration"""
    # Configuration
    source_db = "postgresql://postgres:postgres@localhost:5433/vectors"  # Current staging
    target_db = "postgresql://postgres:postgres@localhost:54322/postgres"  # New Supabase
    
    migrator = DatabaseMigrator(source_db, target_db)
    await migrator.migrate_all()

if __name__ == "__main__":
    asyncio.run(main())
```

### Phase 3: Application Updates (Week 3)

#### 3.1 Database Connection Standardization
```python
# src/database/connection.py
"""Standardized database connection management"""

import asyncpg
from typing import Optional
from contextlib import asynccontextmanager
from src.core.config import config

class DatabaseManager:
    """Centralized database connection management"""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        
    async def initialize(self):
        """Initialize database connection pool"""
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                config.database_url,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection from pool"""
        if not self.pool:
            await self.initialize()
            
        async with self.pool.acquire() as connection:
            yield connection
    
    async def execute_query(self, query: str, *args):
        """Execute a query and return results"""
        async with self.get_connection() as conn:
            return await conn.fetch(query, *args)
    
    async def execute_command(self, command: str, *args):
        """Execute a command (INSERT, UPDATE, DELETE)"""
        async with self.get_connection() as conn:
            return await conn.execute(command, *args)

# Global database manager
db_manager = DatabaseManager()

# Startup/shutdown handlers
async def startup_database():
    """Initialize database on startup"""
    await db_manager.initialize()

async def shutdown_database():
    """Close database on shutdown"""
    await db_manager.close()
```

#### 3.2 Agent Integration Updates
```python
# src/agents/base_agent.py
"""Base agent class with standardized database integration"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.database.connection import db_manager
from src.core.config import config
from src.core.secrets import secrets_manager

class BaseAgent(ABC):
    """Base class for all agents with standardized integrations"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.config = config
        self.db = db_manager
        self.secrets = secrets_manager
        
    async def initialize(self):
        """Initialize agent with required resources"""
        # Load secrets
        await self._load_secrets()
        
        # Initialize database connection
        await self.db.initialize()
        
        # Agent-specific initialization
        await self._initialize_agent()
    
    async def _load_secrets(self):
        """Load required secrets for this agent"""
        # Base implementation - override in subclasses
        pass
    
    @abstractmethod
    async def _initialize_agent(self):
        """Agent-specific initialization logic"""
        pass
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic"""
        pass
    
    async def log_execution(self, pipeline_id: str, result: Dict[str, Any]):
        """Log agent execution to database"""
        await self.db.execute_command("""
            UPDATE pipelines 
            SET {agent_name}_result = $1, updated_at = NOW()
            WHERE pipeline_id = $2
        """.format(agent_name=self.agent_name.lower()),
            result, pipeline_id
        )

# Updated article generation agent
class ArticleGenerationAgent(BaseAgent):
    """Standardized article generation agent"""
    
    def __init__(self):
        super().__init__("article_generation")
        self.anthropic_client = None
        self.openai_client = None
    
    async def _load_secrets(self):
        """Load AI API secrets"""
        self.anthropic_key = await self.secrets.get_secret("ANTHROPIC_API_KEY")
        self.openai_key = await self.secrets.get_secret("OPENAI_API_KEY")
    
    async def _initialize_agent(self):
        """Initialize LLM clients"""
        if self.anthropic_key:
            import anthropic
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
        
        if self.openai_key:
            import openai
            openai.api_key = self.openai_key
            self.openai_client = openai
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate article with standardized database integration"""
        # Generate article (existing logic)
        article_data = await self._generate_article_content(input_data)
        
        # Save to database using standardized schema
        article_id = await self._save_article_to_db(article_data)
        
        return {
            "article_id": article_id,
            "status": "completed",
            "article_data": article_data
        }
    
    async def _save_article_to_db(self, article_data: Dict[str, Any]) -> str:
        """Save article using standardized database schema"""
        result = await self.db.execute_query("""
            INSERT INTO articles (
                title, slug, content_markdown, content_html,
                meta_title, meta_description, primary_keyword,
                secondary_keywords, word_count, status
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING id
        """,
            article_data['title'],
            article_data['slug'],
            article_data['content_markdown'],
            article_data.get('content_html'),
            article_data['meta_title'],
            article_data['meta_description'],
            article_data['primary_keyword'],
            article_data.get('secondary_keywords', []),
            article_data['word_count'],
            'draft'
        )
        
        return str(result[0]['id'])
```

## 📊 Validation & Testing Strategy

### 3.1 Environment Parity Tests
```python
# tests/test_environment_parity.py
"""Ensure all environments behave identically"""

import pytest
import asyncio
from src.core.config import get_config

@pytest.mark.parametrize("environment", ["development", "staging", "production"])
async def test_database_schema_consistency(environment):
    """Test database schema is identical across environments"""
    # Set environment
    os.environ["ENVIRONMENT"] = environment
    config = get_config()
    
    # Connect to database
    conn = await asyncpg.connect(config.database_url)
    
    # Get schema information
    tables = await conn.fetch("""
        SELECT table_name, column_name, data_type 
        FROM information_schema.columns 
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
    """)
    
    # Verify standard tables exist
    table_names = {row['table_name'] for row in tables}
    expected_tables = {'articles', 'pipelines', 'api_keys', 'competitor_articles'}
    
    assert expected_tables.issubset(table_names), f"Missing tables in {environment}"
    
    await conn.close()

@pytest.mark.parametrize("environment", ["development", "staging", "production"])
async def test_api_endpoints_consistent(environment):
    """Test API endpoints work identically across environments"""
    os.environ["ENVIRONMENT"] = environment
    
    # Test health endpoint
    async with httpx.AsyncClient() as client:
        config = get_config()
        response = await client.get(f"{config.api_base_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "environment" in data
        assert data["environment"] == environment
```

### 3.2 Migration Validation
```bash
#!/bin/bash
# validate-standardization.sh

echo "🧪 Validating architecture standardization..."

# Test 1: Verify all environments use same schema
echo "1. Testing schema consistency..."
python -m pytest tests/test_environment_parity.py::test_database_schema_consistency -v

# Test 2: Verify service connectivity
echo "2. Testing service connectivity..."
python scripts/test-service-connectivity.py

# Test 3: Verify agent functionality
echo "3. Testing agent functionality..."
python -m pytest tests/test_agents/ -v

# Test 4: Verify WordPress integration
echo "4. Testing WordPress integration..."
python -m pytest tests/test_wordpress_integration.py -v

# Test 5: Performance baseline
echo "5. Running performance tests..."
python scripts/performance-baseline.py

echo "✅ Standardization validation complete"
```

## 📈 Success Metrics

### Before Standardization
- ❌ 3 different database backends
- ❌ Inconsistent service architectures  
- ❌ Multiple configuration patterns
- ❌ Environment-specific code paths
- ❌ Complex deployment procedures

### After Standardization
- ✅ Single Supabase-based architecture
- ✅ Identical service patterns across environments
- ✅ Unified configuration management
- ✅ Environment-agnostic code
- ✅ Simplified deployment pipeline

### Key Performance Indicators
1. **Environment Parity**: 100% schema consistency
2. **Deployment Success**: 100% success rate across environments
3. **Developer Experience**: Setup time reduced from 2 hours to 15 minutes
4. **Operational Complexity**: Service count reduced from 8 to 3 (in production)
5. **Performance**: Consistent response times across environments

## 🔗 Next Steps

1. **Week 1**: Execute Phase 1 (Foundation Setup)
2. **Week 2**: Execute Phase 2 (Service Migration)  
3. **Week 3**: Execute Phase 3 (Application Updates)
4. **Week 4**: Final validation and production deployment

## 📋 Rollback Plan

If standardization causes issues:

1. **Immediate Rollback**: Revert to staging configuration
2. **Data Recovery**: Restore from pre-migration backups
3. **Service Restart**: Use existing docker-compose.staging.yml
4. **Issue Analysis**: Identify and document failures
5. **Incremental Retry**: Address issues and retry standardization

---

**This standardization plan addresses the critical architecture inconsistencies that prevent reliable production deployment. Upon completion, all environments will have identical, predictable behavior.**