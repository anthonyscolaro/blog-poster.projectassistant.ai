# Blog-Poster API Reference

## Base URL
```
http://localhost:8088
```

## Authentication
Currently, the API does not require authentication for local development. In production, implement API key authentication.

## Response Format
All API responses follow this structure:
```json
{
  "status": "success|error",
  "data": {},
  "errors": [],
  "warnings": []
}
```

---

## 🚀 Pipeline Management

### Run Full Pipeline
Execute the complete multi-agent blog generation pipeline.

**Endpoint:** `POST /pipeline/run`

**Request Body:**
```json
{
  "topic": "string (optional)",
  "primary_keyword": "string (optional)",
  "secondary_keywords": ["string"],
  "min_words": 1500,
  "max_words": 2500,
  "brand_voice": "professional, empathetic, and informative",
  "target_audience": "Service dog handlers and business owners",
  "publish_status": "draft|publish",
  "wordpress_categories": [1, 2],
  "wordpress_tags": [3, 4],
  "use_competitor_insights": true,
  "perform_fact_checking": true,
  "auto_publish": false,
  "max_cost_per_article": 0.50,
  "max_retries": 3,
  "retry_delay": 5
}
```

**Response:**
```json
{
  "status": "completed",
  "execution_time": 45.2,
  "total_cost": 0.35,
  "article": {
    "title": "string",
    "word_count": 1850,
    "seo_score": 92.5,
    "slug": "article-slug"
  },
  "fact_check": {
    "accuracy_score": 0.95,
    "verified_claims": 12,
    "incorrect_claims": 1,
    "total_claims": 13
  },
  "wordpress": {
    "post_id": 123,
    "edit_link": "https://site.com/wp-admin/post.php?post=123",
    "view_link": "https://site.com/article-slug/"
  },
  "errors": [],
  "warnings": []
}
```

### Get Pipeline Status
Check if a pipeline is currently running.

**Endpoint:** `GET /pipeline/status`

**Response:**
```json
{
  "running": true,
  "status": "generating_article",
  "message": "Pipeline is currently in generating_article stage"
}
```

### Get Pipeline History
Retrieve recent pipeline executions.

**Endpoint:** `GET /pipeline/history?limit=10`

**Response:**
```json
{
  "executions": [
    {
      "status": "completed",
      "started_at": "2024-01-15T10:00:00Z",
      "completed_at": "2024-01-15T10:01:30Z",
      "execution_time": 90.5,
      "total_cost": 0.42,
      "errors": []
    }
  ],
  "total": 10
}
```

### Get Pipeline Costs
Get cost summary for pipeline executions.

**Endpoint:** `GET /pipeline/costs`

**Response:**
```json
{
  "total_cost": 12.50,
  "average_cost": 0.35,
  "executions": 35
}
```

---

## 📝 Article Generation

### Generate Article
Generate a single SEO-optimized article.

**Endpoint:** `POST /article/generate`

**Request Body:**
```json
{
  "topic": "How to Train a Service Dog for PTSD Support",
  "primary_keyword": "PTSD service dog",
  "secondary_keywords": ["service dog training", "PTSD support", "ADA requirements"],
  "min_words": 1500,
  "max_words": 2500,
  "use_competitor_insights": true
}
```

**Response:**
```json
{
  "title": "Complete Guide to Training a PTSD Service Dog",
  "slug": "ptsd-service-dog-training-guide",
  "meta_title": "PTSD Service Dog Training: Complete Guide & ADA Requirements",
  "meta_description": "Learn how to train a service dog for PTSD support...",
  "content_markdown": "# Complete Guide...",
  "content_html": "<h1>Complete Guide...</h1>",
  "primary_keyword": "PTSD service dog",
  "secondary_keywords": ["service dog training", "PTSD support"],
  "word_count": 1875,
  "reading_level": 8.5,
  "internal_links": [
    {"text": "ADA requirements", "url": "/ada-requirements-guide"}
  ],
  "external_links": [
    {"text": "ADA.gov", "url": "https://www.ada.gov"}
  ],
  "citations": ["28 CFR §36.302(c)"],
  "featured_image_prompt": "Professional service dog helping veteran with PTSD",
  "category": "Training",
  "tags": ["PTSD", "Training", "ADA"],
  "estimated_reading_time": 8,
  "seo_score": 94.5,
  "cost_tracking": {
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "input_tokens": 4500,
    "output_tokens": 2800,
    "cost": 0.0345
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### Get Article Costs
Get cost summary for article generation.

**Endpoint:** `GET /article/costs`

**Response:**
```json
{
  "total_cost": 8.45,
  "average_cost": 0.32,
  "articles_generated": 26,
  "cost_by_model": {
    "claude-3-5-sonnet-20241022": 7.25,
    "gpt-4-turbo-preview": 1.20
  }
}
```

---

## 🔍 Competitor Monitoring

### Scan Competitors
Scan competitor websites for new content.

**Endpoint:** `POST /competitors/scan`

**Request Body:**
```json
{
  "force": false
}
```

**Response:**
```json
{
  "status": "success",
  "content_pieces": 15,
  "message": "Scanned 15 pieces of content"
}
```

### Get Competitor Insights
Get comprehensive competitor analysis.

**Endpoint:** `GET /competitors/insights`

**Response:**
```json
{
  "trending_topics": [
    {
      "topic": "Service dog vest requirements",
      "trend_score": 85.5,
      "momentum": "rising",
      "competitor_count": 5
    }
  ],
  "content_gaps": [
    {
      "topic": "Service dogs for autism",
      "gap_type": "underserved",
      "opportunity_score": 92.0,
      "difficulty_score": 3.5,
      "rationale": "High search volume, low competition",
      "competitors_covering": 2
    }
  ],
  "recommended_topics": [
    "Service dog training timeline",
    "Cost of service dog training",
    "Service dog handler rights"
  ],
  "analyzed_at": "2024-01-15T10:00:00Z"
}
```

### Get Trending Topics
Get current trending topics from competitors.

**Endpoint:** `GET /competitors/trends`

**Response:**
```json
{
  "trends": [
    {
      "topic": "ESA vs Service Dog",
      "trend_score": 88.5,
      "momentum": "stable",
      "mentions": 12,
      "timeframe": "7_days"
    }
  ],
  "generated_at": "2024-01-15T10:00:00Z"
}
```

### Get Content Gaps
Identify content gaps compared to competitors.

**Endpoint:** `GET /competitors/gaps`

**Response:**
```json
{
  "gaps": [
    {
      "topic": "Service dog grooming standards",
      "gap_type": "missing",
      "opportunity_score": 78.5,
      "difficulty_score": 2.5,
      "rationale": "Competitors have limited coverage",
      "search_volume": 1200,
      "competition": "low"
    }
  ],
  "total_gaps": 8,
  "generated_at": "2024-01-15T10:00:00Z"
}
```

---

## 💡 Topic Analysis

### Analyze Topics
Perform comprehensive topic analysis.

**Endpoint:** `POST /topics/analyze`

**Request Body:**
```json
{
  "keywords": ["service dog", "PTSD", "training"],
  "competitor_urls": ["https://competitor1.com", "https://competitor2.com"],
  "existing_titles": ["Your existing article 1", "Your existing article 2"],
  "max_recommendations": 10
}
```

**Response:**
```json
{
  "keywords_analyzed": 3,
  "content_gaps_found": 5,
  "topics_recommended": 10,
  "recommendations": [
    {
      "title": "How Long Does It Take to Train a PTSD Service Dog?",
      "slug": "ptsd-service-dog-training-timeline",
      "primary_keyword": "PTSD service dog training time",
      "secondary_keywords": ["service dog timeline", "training duration"],
      "content_type": "guide",
      "target_word_count": 2000,
      "priority_score": 95.5,
      "rationale": "High search volume with low competition",
      "outline": [
        "Introduction to PTSD service dogs",
        "Training phases and timeline",
        "Factors affecting training duration"
      ]
    }
  ],
  "market_insights": {
    "trending_up": ["PTSD service dogs", "veteran service dogs"],
    "saturated": ["ESA vs service dog"],
    "opportunities": ["Service dog training costs", "Handler training"]
  },
  "analyzed_at": "2024-01-15T10:00:00Z"
}
```

### Get Topic Recommendations
Get quick topic recommendations.

**Endpoint:** `GET /topics/recommendations?count=5&focus=PTSD`

**Response:**
```json
{
  "recommendations": [
    {
      "title": "PTSD Service Dog Tasks: Complete List",
      "slug": "ptsd-service-dog-tasks",
      "primary_keyword": "PTSD service dog tasks",
      "content_type": "listicle",
      "priority_score": 88.5,
      "target_word_count": 1800
    }
  ],
  "count": 5,
  "focus": "PTSD"
}
```

### Identify Content Gaps
Find content gaps based on keywords.

**Endpoint:** `GET /topics/gaps`

**Request Body:**
```json
{
  "keywords": ["service dog", "restaurant", "rights"],
  "existing_titles": ["Service Dogs in Public Places"]
}
```

**Response:**
```json
{
  "gaps": [
    {
      "topic": "Service dog restaurant etiquette",
      "gap_type": "partial_coverage",
      "opportunity_score": 82.5,
      "difficulty_score": 3.0,
      "rationale": "Existing content lacks specific restaurant guidance",
      "competitors_covering": 3
    }
  ],
  "total_gaps": 4
}
```

---

## 🔎 Vector Search

### Index Document
Add a document to the vector search index.

**Endpoint:** `POST /vector/index`

**Request Body:**
```json
{
  "content": "Full article content here...",
  "document_id": "article-123",
  "title": "Service Dog Training Guide",
  "url": "/articles/service-dog-training",
  "collection": "blog_articles"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Document article-123 indexed successfully",
  "collection": "blog_articles"
}
```

### Search Documents
Search for similar documents using semantic search.

**Endpoint:** `POST /vector/search`

**Request Body:**
```json
{
  "query": "How to train a service dog for anxiety",
  "limit": 5,
  "collection": "blog_articles"
}
```

**Response:**
```json
{
  "query": "How to train a service dog for anxiety",
  "results": [
    {
      "title": "Anxiety Service Dog Training Guide",
      "content": "Training a service dog for anxiety requires...",
      "url": "/articles/anxiety-service-dog",
      "score": 0.945
    }
  ],
  "count": 5
}
```

### Check Duplicate
Check if content is a duplicate of existing content.

**Endpoint:** `POST /vector/check-duplicate`

**Request Body:**
```json
{
  "content": "Article content to check for duplicates...",
  "threshold": 0.9,
  "collection": "blog_articles"
}
```

**Response:**
```json
{
  "is_duplicate": true,
  "similar_document": {
    "title": "Similar Article Title",
    "url": "/articles/similar-article",
    "similarity": 0.92
  }
}
```

### Get Internal Links
Get internal link recommendations for content.

**Endpoint:** `GET /vector/internal-links`

**Query Parameters:**
- `content`: Content to find links for
- `limit`: Maximum number of links (default: 5)

**Response:**
```json
{
  "links": [
    {
      "title": "Related Article Title",
      "url": "/articles/related-article",
      "relevance_score": 0.88,
      "excerpt": "This article discusses..."
    }
  ],
  "count": 5
}
```

### Get Collection Stats
Get statistics for a vector collection.

**Endpoint:** `GET /vector/stats?collection=blog_articles`

**Response:**
```json
{
  "collection": "blog_articles",
  "points_count": 1250,
  "vectors_count": 1250,
  "indexed_vectors_count": 1250,
  "status": "green",
  "config": {
    "vector_size": 1536,
    "distance": "Cosine"
  }
}
```

### Delete Document
Remove a document from the vector index.

**Endpoint:** `DELETE /vector/document/{document_id}?collection=blog_articles`

**Response:**
```json
{
  "success": true,
  "message": "Document article-123 deleted"
}
```

---

## 📰 WordPress Publishing

### Publish to WordPress
Create or update a WordPress post.

**Endpoint:** `POST /publish/wp`

**Request Body:**
```json
{
  "title": "Article Title",
  "content": "<p>Article HTML content...</p>",
  "status": "draft",
  "slug": "article-slug",
  "categories": [1, 2],
  "tags": [3, 4],
  "meta_title": "SEO Title",
  "meta_description": "SEO meta description..."
}
```

**Response:**
```json
{
  "success": true,
  "post_id": 123,
  "edit_link": "https://site.com/wp-admin/post.php?post=123",
  "view_link": "https://site.com/article-slug/",
  "message": "Post created successfully"
}
```

### Test WordPress Connection
Verify WordPress connectivity and authentication.

**Endpoint:** `GET /wordpress/test`

**Response:**
```json
{
  "connected": true,
  "wordpress_url": "https://site.com",
  "auth_method": "application_passwords",
  "is_local": false,
  "categories": [
    {"id": 1, "name": "Training"},
    {"id": 2, "name": "Legal"}
  ],
  "tags": [
    {"id": 3, "name": "ADA"},
    {"id": 4, "name": "PTSD"}
  ]
}
```

---

## 🛠️ Utility Endpoints

### Health Check
Check if the service is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok",
  "time": "2024-01-15T10:00:00Z",
  "version": "1.0.0",
  "services": {
    "api": "healthy",
    "qdrant": "healthy",
    "redis": "healthy",
    "postgres": "healthy"
  }
}
```

### SEO Lint
Validate content for SEO compliance.

**Endpoint:** `POST /seo/lint`

**Request Body:**
```json
{
  "frontmatter": {
    "meta_title": "Service Dog Training Guide - Complete 2024 Guide",
    "meta_desc": "Learn how to train a service dog with our comprehensive guide covering ADA requirements, training techniques, and certification.",
    "canonical": "https://site.com/service-dog-training"
  },
  "markdown": "# Service Dog Training Guide\n\n## Introduction\n..."
}
```

**Response:**
```json
{
  "violations": [
    "meta_title length 62 out of 45-60",
    "image missing alt text",
    "H2 count below recommended minimum of 3"
  ]
}
```

### Legacy Agent Run
Run the original agent implementation (for compatibility).

**Endpoint:** `POST /agent/run`

**Request Body:**
```json
{
  "topic_rec": {
    "topic_slug": "ptsd-service-dog",
    "primary_kw": "PTSD service dog",
    "secondary_kws": ["service dog training", "PTSD support"],
    "title_variants": ["PTSD Service Dog Guide"],
    "rationale": "High search volume topic",
    "supporting_urls": ["https://ada.gov"],
    "score_breakdown": {"relevance": 95, "difficulty": 35},
    "risk_flags": []
  },
  "brand_style": {
    "voice": "clear, empathetic",
    "audience": "general public",
    "tone": "confident",
    "reading_grade_target": 8,
    "banned_phrases": []
  },
  "site_info": {
    "site_url": "https://site.com",
    "canonical_base": "https://site.com",
    "category_map": {"Training": 1, "Legal": 2},
    "internal_link_candidates": []
  },
  "evidence": {
    "facts": ["ADA does not require registration"],
    "statutes": ["28 CFR §36.302(c)"],
    "dates": ["2010-07-23"],
    "sources": ["https://ada.gov"],
    "serp_snapshot": [],
    "competitor_chunks": []
  },
  "constraints": {
    "min_words": 1500,
    "max_words": 2500,
    "image_policy": "stock_or_generated_ok",
    "require_disclaimer": true,
    "disallow_competitor_links": true
  }
}
```

**Response:**
```json
{
  "status": "success",
  "output": "# Article Title\n\nArticle content...",
  "tool_calls": [],
  "tool_results": [],
  "errors": []
}
```

---

## 🔐 Error Handling

All endpoints return consistent error responses:

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Invalid request parameters",
  "errors": [
    "primary_keyword is required",
    "min_words must be at least 500"
  ]
}
```

### 401 Unauthorized
```json
{
  "status": "error",
  "message": "Authentication required",
  "errors": ["Invalid or missing API key"]
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Resource not found",
  "errors": ["Document with ID 'article-999' not found"]
}
```

### 429 Too Many Requests
```json
{
  "status": "error",
  "message": "Rate limit exceeded",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Internal server error",
  "errors": ["Failed to connect to vector database"],
  "request_id": "req_123456"
}
```

---

## 📊 Rate Limiting

Default rate limits (configurable):
- **Global**: 100 requests per minute
- **Article Generation**: 10 per hour
- **Pipeline Runs**: 5 per hour
- **Vector Search**: 1000 per hour

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248000
```

---

## 🔄 Webhooks

Configure webhooks for pipeline events:

### Webhook Events
- `pipeline.started` - Pipeline execution started
- `pipeline.completed` - Pipeline completed successfully
- `pipeline.failed` - Pipeline failed
- `article.generated` - Article generation completed
- `article.published` - Article published to WordPress

### Webhook Payload
```json
{
  "event": "pipeline.completed",
  "timestamp": "2024-01-15T10:00:00Z",
  "data": {
    "pipeline_id": "pipe_123",
    "status": "completed",
    "article_id": "article_456",
    "wordpress_post_id": 789
  }
}
```

---

## 🧪 Testing

### Test with cURL

Generate an article:
```bash
curl -X POST http://localhost:8088/article/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Service Dog Training Basics",
    "primary_keyword": "service dog training"
  }'
```

Search for content:
```bash
curl -X POST http://localhost:8088/vector/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ADA requirements for service dogs",
    "limit": 3
  }'
```

### Test with Python

```python
import requests

# Generate article
response = requests.post(
    "http://localhost:8088/article/generate",
    json={
        "topic": "Service Dog Public Access Rights",
        "primary_keyword": "service dog rights"
    }
)
article = response.json()
print(f"Generated: {article['title']}")

# Publish to WordPress
response = requests.post(
    "http://localhost:8088/publish/wp",
    json={
        "title": article["title"],
        "content": article["content_html"],
        "status": "draft"
    }
)
result = response.json()
print(f"Published: {result['edit_link']}")
```

---

## 📦 SDK Support

### JavaScript/TypeScript
```typescript
import { BlogPosterClient } from '@blog-poster/sdk';

const client = new BlogPosterClient({
  baseURL: 'http://localhost:8088',
  apiKey: 'your-api-key'
});

// Generate article
const article = await client.articles.generate({
  topic: 'Service Dog Training',
  primaryKeyword: 'service dog training'
});

// Run pipeline
const result = await client.pipeline.run({
  topic: 'PTSD Service Dogs',
  autoPublish: true
});
```

### Python SDK
```python
from blog_poster import BlogPosterClient

client = BlogPosterClient(
    base_url="http://localhost:8088",
    api_key="your-api-key"
)

# Generate article
article = client.articles.generate(
    topic="Service Dog Training",
    primary_keyword="service dog training"
)

# Run pipeline
result = client.pipeline.run(
    topic="PTSD Service Dogs",
    auto_publish=True
)
```

---

## 🌐 CORS Configuration

The API supports CORS for browser-based applications:

```python
# Current CORS settings (development)
allow_origins=["*"]
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]

# Production CORS settings
allow_origins=["https://your-domain.com"]
allow_credentials=True
allow_methods=["GET", "POST", "PUT", "DELETE"]
allow_headers=["Authorization", "Content-Type"]
```

---

## 📈 Monitoring

### Metrics Endpoint
**Endpoint:** `GET /metrics`

Returns Prometheus-compatible metrics:
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{endpoint="/article/generate",method="POST",status="200"} 125

# HELP article_generation_duration_seconds Article generation time
# TYPE article_generation_duration_seconds histogram
article_generation_duration_seconds_bucket{le="10.0"} 45
article_generation_duration_seconds_bucket{le="30.0"} 120
```

### Health Checks
- Liveness: `/health/live`
- Readiness: `/health/ready`
- Startup: `/health/startup`