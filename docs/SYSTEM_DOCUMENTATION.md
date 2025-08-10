# Blog-Poster System Documentation

## 🏗️ System Overview

Blog-Poster is a sophisticated **Multi-Agent AI Content Generation System** designed for automated SEO-optimized blog content creation and publishing. The system orchestrates five specialized AI agents working in sequence to produce high-quality, legally accurate content about service dogs and ADA compliance.

### Key Features
- **Fully Automated Pipeline** - From competitor analysis to WordPress publishing
- **Vector Search Integration** - Semantic search for content deduplication and internal linking
- **Legal Fact Checking** - Ensures ADA compliance accuracy with proper citations
- **SEO Optimization** - Built-in SEO scoring and optimization
- **Cost Management** - Per-article and monthly budget tracking
- **Docker-First Architecture** - Complete containerized deployment

## 📊 Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestration Manager                    │
│                    (orchestration_manager.py)                │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐ ┌───────▼──────┐ ┌──────▼───────┐
│  Competitor  │ │    Topic     │ │   Article    │
│ Monitoring   │ │  Analysis    │ │ Generation   │
│    Agent     │ │    Agent     │ │    Agent     │
└──────────────┘ └──────────────┘ └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                                  │
┌───────▼──────┐                  ┌───────▼──────┐
│Legal Fact    │                  │  WordPress   │
│Checker Agent │                  │  Publisher   │
└──────────────┘                  └──────────────┘
```

### Data Flow

1. **Competitor Monitoring** → Tracks industry content using Jina AI
2. **Topic Analysis** → Identifies SEO opportunities and content gaps
3. **Article Generation** → Creates content with Claude 3.5 Sonnet
4. **Legal Fact Checking** → Verifies ADA compliance and citations
5. **WordPress Publishing** → Deploys content via WPGraphQL

## 🤖 Multi-Agent System

### 1. Competitor Monitoring Agent
**File**: `agents/competitor_monitoring_agent.py`

**Purpose**: Tracks competitor content and identifies trends

**Key Functions**:
- `scan_competitors()` - Scrapes competitor websites for new content
- `analyze_trends()` - Identifies trending topics and patterns
- `identify_content_gaps()` - Finds opportunities competitors are missing
- `generate_insights()` - Creates comprehensive competitive analysis

**Data Models**:
- `CompetitorContent` - Individual content piece metadata
- `TrendingTopic` - Topic with trend score and momentum
- `ContentGap` - Identified opportunity with difficulty score
- `CompetitorInsights` - Complete analysis package

### 2. Topic Analysis Agent
**File**: `agents/topic_analysis_agent.py`

**Purpose**: Analyzes topics for SEO opportunities

**Key Functions**:
- `analyze_topics()` - Deep analysis of keyword opportunities
- `get_quick_recommendations()` - Fast topic suggestions
- `identify_gaps()` - Content gap identification
- `score_opportunity()` - Calculate topic priority scores

**Data Models**:
- `TopicRecommendation` - Complete topic recommendation with outline
- `TopicAnalysisReport` - Full analysis report with insights
- `ContentGap` - Gap opportunity with metrics

### 3. Article Generation Agent
**File**: `agents/article_generation_agent.py`

**Purpose**: Generates SEO-optimized articles using LLMs

**Key Functions**:
- `generate_article()` - Main article generation pipeline
- `_generate_outline()` - Creates article structure
- `_generate_content()` - Produces full article content
- `_generate_metadata()` - Creates SEO metadata
- `_calculate_costs()` - Tracks API usage costs

**Data Models**:
- `GeneratedArticle` - Complete article with all metadata
- `SEORequirements` - Article generation constraints
- `CostTracking` - LLM API cost tracking

**LLM Support**:
- Claude 3.5 Sonnet (primary)
- Claude 3 Opus
- GPT-4 Turbo
- GPT-3.5 Turbo

### 4. Legal Fact Checker Agent
**File**: `agents/legal_fact_checker_agent.py`

**Purpose**: Verifies legal accuracy and ADA compliance

**Key Functions**:
- `fact_check_article()` - Comprehensive fact checking
- `verify_ada_claims()` - Validates ADA-specific statements
- `check_citations()` - Verifies legal citations
- `suggest_corrections()` - Provides correction recommendations

**Data Models**:
- `LegalFactCheckReport` - Complete fact check results
- `ClaimVerification` - Individual claim verification
- `CitationCheck` - Citation validation result

**Verification Sources**:
- ADA.gov official resources
- 28 CFR Part 36 regulations
- DOJ guidance documents
- State-specific service dog laws

### 5. WordPress Publishing Agent
**File**: `wordpress_publisher.py`

**Purpose**: Publishes content to WordPress

**Key Functions**:
- `test_connection()` - Verifies WordPress connectivity
- `create_post()` - Creates new WordPress post
- `update_post()` - Updates existing post
- `get_categories()` - Retrieves category list
- `get_tags()` - Retrieves tag list

**Authentication Methods**:
- JWT tokens (WPGraphQL JWT Authentication)
- Application Passwords (REST API)

## 🔍 Vector Search Integration

**File**: `vector_search.py`

### Purpose
Provides semantic search capabilities for content similarity, duplicate detection, and internal linking recommendations.

### Key Features
- **Document Indexing** - Chunks and embeds articles automatically
- **Semantic Search** - Find similar content using AI embeddings
- **Duplicate Detection** - Check for similar existing content
- **Internal Linking** - Automatically recommend relevant internal links
- **Collection Management** - Separate collections for different content types

### Collections
- `blog_articles` - Published blog content
- `competitor_content` - Competitor articles
- `research_docs` - Research documents

### Technical Details
- **Vector Database**: Qdrant (port 6333)
- **Embeddings**: OpenAI text-embedding-ada-002 (1536 dimensions)
- **Distance Metric**: Cosine similarity
- **Chunking**: 500 chars with 100 char overlap

### Key Functions
- `index_document()` - Index new content
- `search()` - Semantic similarity search
- `check_duplicate()` - Duplicate detection
- `get_internal_links()` - Link recommendations
- `find_similar_documents()` - Similar content discovery

## 🌐 API Endpoints

### Pipeline Management

#### `POST /pipeline/run`
Execute the complete multi-agent pipeline
```json
{
  "topic": "Service Dog Training for PTSD",
  "primary_keyword": "PTSD service dog",
  "use_competitor_insights": true,
  "perform_fact_checking": true,
  "auto_publish": false
}
```

#### `GET /pipeline/status`
Get current pipeline execution status

#### `GET /pipeline/history`
Get recent pipeline execution history

### Article Generation

#### `POST /article/generate`
Generate a single article
```json
{
  "topic": "Service Dog Rights in Restaurants",
  "primary_keyword": "service dog restaurants",
  "secondary_keywords": ["ADA", "public accommodation"],
  "min_words": 1500,
  "max_words": 2500
}
```

#### `GET /article/costs`
Get cost summary for article generation

### Competitor Monitoring

#### `POST /competitors/scan`
Scan competitor websites for new content

#### `GET /competitors/insights`
Get comprehensive competitor analysis

#### `GET /competitors/trends`
Get current trending topics

### Topic Analysis

#### `POST /topics/analyze`
Analyze topics for SEO opportunities
```json
{
  "keywords": ["service dog", "PTSD", "training"],
  "competitor_urls": ["https://competitor.com"],
  "max_recommendations": 10
}
```

#### `GET /topics/recommendations`
Get quick topic recommendations

### Vector Search

#### `POST /vector/index`
Index a document in vector search
```json
{
  "content": "Article content...",
  "document_id": "article-001",
  "title": "Article Title",
  "collection": "blog_articles"
}
```

#### `POST /vector/search`
Search for similar documents
```json
{
  "query": "service dog training techniques",
  "limit": 5,
  "collection": "blog_articles"
}
```

#### `POST /vector/check-duplicate`
Check if content is duplicate
```json
{
  "content": "Content to check...",
  "threshold": 0.9,
  "collection": "blog_articles"
}
```

### WordPress Publishing

#### `POST /publish/wp`
Publish article to WordPress
```json
{
  "title": "Article Title",
  "content": "Article content...",
  "status": "draft",
  "meta_title": "SEO Title",
  "meta_description": "SEO Description"
}
```

#### `GET /wordpress/test`
Test WordPress connection

### Utility Endpoints

#### `GET /health`
Service health check

#### `POST /seo/lint`
Validate SEO compliance
```json
{
  "frontmatter": {"meta_title": "Title", "meta_desc": "Description"},
  "markdown": "# Article content..."
}
```

## 🐳 Docker Services

### Service Configuration

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| API | blog-api | 8088 | FastAPI application |
| Qdrant | blog-qdrant | 6333 | Vector database |
| PostgreSQL | blog-vectors | 5433 | pgvector for embeddings |
| Redis | blog-redis | 6384 | Queue and caching |

### Docker Compose Structure
```yaml
services:
  api:
    - FastAPI with hot reload
    - Depends on all other services
    - Health checks enabled
    
  qdrant:
    - Vector search database
    - Persistent storage volume
    
  vectors:
    - PostgreSQL with pgvector
    - Backup vector storage
    
  redis:
    - Job queue and caching
    - Append-only persistence
```

## 🔧 Environment Configuration

### Required Variables
```env
# AI Providers (at least one required)
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...

# Web Scraping
JINA_API_KEY=jina_...

# WordPress
WORDPRESS_URL=https://site.com
WP_USERNAME=admin
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Vector Search
QDRANT_URL=http://localhost:6333
```

### Optional Variables
```env
# SSL Settings
WP_VERIFY_SSL=false  # For local development

# Cost Management
MAX_COST_PER_ARTICLE=0.50
MAX_MONTHLY_COST=100.00

# Model Selection
DEFAULT_LLM_PROVIDER=anthropic
MODEL_OVERRIDE=claude-3-5-sonnet-20241022
```

## 💰 Cost Management

### Per-Article Tracking
- Input/output token counting
- Model-specific pricing
- Real-time cost calculation
- Budget enforcement

### Pricing (per 1M tokens)
| Model | Input | Output |
|-------|-------|--------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Opus | $15.00 | $75.00 |
| GPT-4 Turbo | $10.00 | $30.00 |
| GPT-3.5 Turbo | $0.50 | $1.50 |

### Budget Controls
- Per-article limits
- Monthly caps
- 80% threshold alerts
- Automatic cutoff

## 🚀 Deployment

### Local Development
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f api

# Stop services
docker compose down
```

### Production Deployment
1. Set production environment variables
2. Configure SSL certificates
3. Set up monitoring (Prometheus/Grafana)
4. Configure backup strategy
5. Enable rate limiting

### Health Monitoring
- `/health` endpoint for container checks
- Service-specific health checks
- Retry policies for resilience
- Graceful failure handling

## 🔒 Security Considerations

### API Security
- Environment variable isolation
- No hardcoded credentials
- SSL/TLS for production
- Rate limiting on endpoints

### WordPress Security
- Application passwords (no plain text)
- JWT token rotation
- IP whitelisting (optional)
- SSL verification

### Data Security
- Vector embeddings are anonymous
- No PII in vector database
- Secure credential storage
- Audit logging

## 📈 Performance Optimization

### Caching Strategy
- Redis for API responses
- Vector search result caching
- LLM response caching
- WordPress API caching

### Scaling Considerations
- Horizontal scaling via Docker Swarm/K8s
- Database connection pooling
- Async processing for long tasks
- Queue-based job distribution

## 🧪 Testing

### Unit Tests
- Agent-specific test suites
- Mocked LLM responses
- Vector search testing
- WordPress integration tests

### Integration Tests
- End-to-end pipeline testing
- Multi-agent coordination
- Error handling scenarios
- Cost tracking validation

### Performance Tests
- Load testing with Locust
- Vector search benchmarks
- LLM response time monitoring
- Database query optimization

## 📚 Additional Resources

### Documentation
- [API Reference](./API_REFERENCE.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Agent Development](./AGENT_DEVELOPMENT.md)
- [Troubleshooting](./TROUBLESHOOTING.md)

### External Links
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference)
- [WPGraphQL Documentation](https://www.wpgraphql.com/docs/)
- [ADA.gov Resources](https://www.ada.gov/)

## 🎯 Vector Search Success Metrics

✅ **Vector Search Successfully Connected!**

Features Implemented:
- Document Indexing - Articles automatically chunked and embedded
- Semantic Search - Find similar content using AI embeddings
- Duplicate Detection - Check for similar existing content
- Internal Linking - Automatically recommend relevant internal links
- Collection Management - Separate collections for articles, competitors, and research

Technical Achievement:
- Vector Database: Qdrant running on port 6333
- Embeddings: OpenAI text-embedding-ada-002 (1536 dimensions)
- Distance Metric: Cosine similarity
- Collections Created:
  - blog_articles - Published content
  - competitor_content - Competitor articles
  - research_docs - Research documents

The multi-agent system now has complete vector search capabilities for intelligent content management!