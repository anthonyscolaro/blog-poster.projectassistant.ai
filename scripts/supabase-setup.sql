-- Supabase Database Setup for Blog Poster
-- Run this in the Supabase SQL Editor

-- pgvector extension should already be enabled
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Additional useful extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Create articles table with vector column for embeddings
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    document_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT,
    embedding vector(1536), -- OpenAI ada-002 dimension
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for vector similarity search
CREATE INDEX IF NOT EXISTS articles_embedding_idx ON articles 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create text search index
CREATE INDEX IF NOT EXISTS articles_content_idx ON articles 
USING gin(to_tsvector('english', content));

-- Create metadata index
CREATE INDEX IF NOT EXISTS articles_metadata_idx ON articles 
USING gin(metadata);

-- Create competitor content table
CREATE TABLE IF NOT EXISTS competitor_content (
    id SERIAL PRIMARY KEY,
    document_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT,
    competitor_name TEXT,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for competitor content
CREATE INDEX IF NOT EXISTS competitor_embedding_idx ON competitor_content 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create research documents table
CREATE TABLE IF NOT EXISTS research_docs (
    id SERIAL PRIMARY KEY,
    document_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for research docs
CREATE INDEX IF NOT EXISTS research_embedding_idx ON research_docs 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Function to search similar documents
CREATE OR REPLACE FUNCTION search_similar_documents(
    query_embedding vector(1536),
    match_count int DEFAULT 5,
    threshold float DEFAULT 0.7
)
RETURNS TABLE (
    document_id TEXT,
    title TEXT,
    content TEXT,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.document_id,
        a.title,
        a.content,
        1 - (a.embedding <=> query_embedding) as similarity
    FROM articles a
    WHERE 1 - (a.embedding <=> query_embedding) > threshold
    ORDER BY a.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Verify setup
SELECT 'pgvector extension enabled' as status 
WHERE EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector');

SELECT 'Tables created successfully' as status 
WHERE EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'articles');