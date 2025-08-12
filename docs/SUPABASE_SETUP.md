# Supabase Setup Guide

## Overview

This project uses Supabase for both local development and production, providing:
- PostgreSQL database with pgvector extension for vector similarity search
- Authentication (Supabase Auth)
- Realtime subscriptions
- File storage
- REST APIs via PostgREST

## Why Supabase Instead of Qdrant?

We migrated from Qdrant to Supabase's PostgreSQL with pgvector to:
1. **Consolidate infrastructure** - Single database for both relational and vector data
2. **Dev/prod parity** - Same stack locally and in production
3. **Better integration** - Native SQL alongside vector operations
4. **Cost efficiency** - One service instead of multiple
5. **Feature richness** - Auth, storage, realtime all included

## Local Development Setup

### 1. Start Supabase Stack

```bash
# Copy environment template
cp .env.supabase.example .env.local

# Start all services
docker compose up -d

# Check services are running
docker compose ps
```

### 2. Access Services

- **Supabase Studio**: http://localhost:3100
- **API Gateway**: http://localhost:8000
- **REST API**: http://localhost:8000/rest/v1
- **Auth**: http://localhost:8000/auth/v1
- **Application**: http://localhost:8088

### 3. Initialize Database

The pgvector extension and tables are automatically created on first startup via `scripts/init-pgvector.sql`.

To manually run migrations:
```bash
python scripts/migrate_to_pgvector.py
```

## Production Setup

### 1. Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Create new project
3. **Important**: Choose standard PostgreSQL (not OrioleDB) for pgvector support
4. Save your credentials

### 2. Enable pgvector

In Supabase Dashboard:
1. Go to Database → Extensions
2. Search for "vector"
3. Enable the extension

Or via SQL Editor:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 3. Run Database Migrations

In the SQL Editor, run the contents of `scripts/init-pgvector.sql`

### 4. Update Environment Variables

```bash
# .env.staging or .env.prod
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
```

## Vector Search Operations

### Storing Embeddings

```python
from src.services.vector_search import VectorSearchManager

manager = VectorSearchManager()

# Index a document
await manager.index_document(
    content="Your article content",
    document_id="article-001",
    title="Article Title",
    url="/articles/article-001"
)
```

### Searching Similar Documents

```python
# Find similar content
results = await manager.search(
    query="service dog requirements",
    limit=5
)

# Check for duplicates
duplicate = await manager.check_duplicate(
    content="New article content",
    threshold=0.9  # 90% similarity
)
```

## Database Schema

### Articles Table
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    document_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT,
    embedding vector(1536),  -- OpenAI ada-002 dimensions
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Indexes for Performance
- **Vector similarity**: IVFFlat index for fast similarity search
- **Full-text search**: GIN index on content
- **Metadata queries**: GIN index on JSONB

## Troubleshooting

### Container Issues

```bash
# View logs
docker compose logs supabase-db
docker compose logs api

# Restart services
docker compose restart

# Clean slate
docker compose down -v
docker compose up -d
```

### Database Connection Issues

1. Check DATABASE_URL format:
   ```
   postgresql://postgres:password@localhost:5434/postgres
   ```

2. Verify pgvector is enabled:
   ```sql
   SELECT * FROM pg_extension WHERE extname = 'vector';
   ```

3. Test connection:
   ```bash
   psql $DATABASE_URL -c "SELECT version();"
   ```

### Vector Search Issues

1. Ensure embeddings are being generated:
   ```python
   # Check OpenAI API key is set
   echo $OPENAI_API_KEY
   ```

2. Verify index exists:
   ```sql
   SELECT indexname FROM pg_indexes 
   WHERE tablename = 'articles';
   ```

3. Check embedding dimensions match:
   ```sql
   SELECT vector_dims(embedding) 
   FROM articles LIMIT 1;
   -- Should return 1536 for OpenAI ada-002
   ```

## Migration from Qdrant

If you have existing data in Qdrant:

1. Export data from Qdrant
2. Run migration script:
   ```bash
   python scripts/migrate_to_pgvector.py
   ```
3. Verify data integrity
4. Update application configuration
5. Remove Qdrant container

## Performance Optimization

### Vector Index Tuning

```sql
-- Adjust lists parameter based on dataset size
-- More lists = better recall, slower build
-- Fewer lists = faster build, lower recall
CREATE INDEX ON articles 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- Adjust based on data size
```

### Query Optimization

```sql
-- Use appropriate operators
-- <=> : Euclidean distance
-- <#> : Negative inner product
-- <-> : Cosine distance (most common for embeddings)
SELECT * FROM articles
ORDER BY embedding <-> '[...]'::vector
LIMIT 5;
```

## Monitoring

### Check Database Size
```sql
SELECT pg_database_size('postgres') / 1024 / 1024 as size_mb;
```

### Monitor Index Performance
```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) as size
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexname::regclass) DESC;
```

### Vector Search Statistics
```sql
SELECT 
    COUNT(*) as total_documents,
    COUNT(embedding) as documents_with_embeddings,
    AVG(vector_dims(embedding)) as avg_dimensions
FROM articles;
```