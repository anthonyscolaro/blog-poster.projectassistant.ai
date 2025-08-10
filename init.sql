-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Competitor content tracking
CREATE TABLE IF NOT EXISTS competitor_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    competitor_domain VARCHAR(255) NOT NULL,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    content TEXT,
    published_date TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT NOW(),
    word_count INTEGER,
    engagement_data JSONB,
    content_hash VARCHAR(64),
    simhash VARCHAR(64),
    source_of_truth VARCHAR(50),
    CONSTRAINT chk_source CHECK (source_of_truth IN ('jina', 'bright_data', 'native_api'))
);

CREATE INDEX idx_competitor_date ON competitor_content(competitor_domain, published_date DESC);
CREATE INDEX idx_content_hash ON competitor_content(content_hash);
CREATE INDEX idx_simhash ON competitor_content(simhash);

-- Topic analysis results
CREATE TABLE IF NOT EXISTS topic_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_date TIMESTAMP DEFAULT NOW(),
    topic VARCHAR(500) NOT NULL,
    keywords TEXT[],
    opportunity_score FLOAT,
    competitor_coverage FLOAT,
    search_volume INTEGER,
    status VARCHAR(50) DEFAULT 'identified',
    CONSTRAINT chk_status CHECK (status IN ('identified', 'generated', 'published', 'rejected'))
);

CREATE INDEX idx_topic_score ON topic_analysis(opportunity_score DESC);
CREATE INDEX idx_topic_status ON topic_analysis(status);

-- Generated articles
CREATE TABLE IF NOT EXISTS generated_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id UUID REFERENCES topic_analysis(id),
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    meta_description TEXT,
    word_count INTEGER,
    seo_score FLOAT,
    generation_model VARCHAR(100),
    generation_cost DECIMAL(10,4),
    jurisdiction VARCHAR(50) NOT NULL,
    legal_fact_checked BOOLEAN DEFAULT FALSE,
    fact_check_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    wordpress_post_id INTEGER,
    status VARCHAR(50) DEFAULT 'draft',
    CONSTRAINT chk_status CHECK (status IN ('draft', 'pending', 'published', 'failed')),
    CONSTRAINT chk_publish_requires_factcheck CHECK (status != 'published' OR legal_fact_checked = TRUE)
);

CREATE INDEX idx_article_status ON generated_articles(status);
CREATE INDEX idx_article_created ON generated_articles(created_at DESC);
CREATE INDEX idx_article_jurisdiction ON generated_articles(jurisdiction);

-- Legal claims and citations
CREATE TABLE IF NOT EXISTS legal_claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES generated_articles(id) ON DELETE CASCADE,
    claim_text TEXT NOT NULL,
    law_referenced VARCHAR(50),
    jurisdiction VARCHAR(50),
    verified BOOLEAN DEFAULT FALSE,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_claim_article ON legal_claims(article_id);
CREATE INDEX idx_claim_law ON legal_claims(law_referenced);

-- Citation tracking
CREATE TABLE IF NOT EXISTS citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID REFERENCES legal_claims(id) ON DELETE CASCADE,
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50),
    url TEXT NOT NULL,
    title TEXT,
    quote TEXT,
    is_authoritative BOOLEAN DEFAULT FALSE,
    date_accessed TIMESTAMP DEFAULT NOW(),
    CONSTRAINT chk_source_type CHECK (source_type IN ('government', 'law', 'court_case', 'academic', 'nonprofit'))
);

CREATE INDEX idx_citation_claim ON citations(claim_id);
CREATE INDEX idx_citation_source_type ON citations(source_type);

-- Article embeddings for semantic search
CREATE TABLE IF NOT EXISTS article_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_slug VARCHAR(500) UNIQUE NOT NULL,
    title TEXT,
    embedding vector(384),  -- all-MiniLM-L6-v2 dimensions
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_embedding ON article_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Performance metrics
CREATE TABLE IF NOT EXISTS article_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES generated_articles(id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    page_views INTEGER DEFAULT 0,
    unique_visitors INTEGER DEFAULT 0,
    avg_time_on_page FLOAT,
    bounce_rate FLOAT,
    search_impressions INTEGER,
    search_clicks INTEGER,
    search_position FLOAT,
    UNIQUE(article_id, metric_date)
);

CREATE INDEX idx_metrics_article_date ON article_metrics(article_id, metric_date DESC);

-- Crawl compliance tracking
CREATE TABLE IF NOT EXISTS crawl_compliance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain VARCHAR(255) UNIQUE NOT NULL,
    robots_txt TEXT,
    robots_txt_parsed JSONB,
    tos_url TEXT,
    tos_compliant BOOLEAN DEFAULT TRUE,
    crawl_delay FLOAT DEFAULT 1.0,
    max_pages_per_run INTEGER DEFAULT 10,
    last_checked TIMESTAMP DEFAULT NOW(),
    notes TEXT
);

CREATE INDEX idx_compliance_domain ON crawl_compliance(domain);

-- Job tracking for orchestration
CREATE TABLE IF NOT EXISTS job_tracking (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    metadata JSONB,
    CONSTRAINT chk_job_type CHECK (job_type IN ('monitor', 'analyze', 'generate', 'publish', 'full_cycle')),
    CONSTRAINT chk_job_status CHECK (status IN ('pending', 'running', 'completed', 'failed'))
);

CREATE INDEX idx_job_status ON job_tracking(status, job_type);
CREATE INDEX idx_job_started ON job_tracking(started_at DESC);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bloguser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bloguser;