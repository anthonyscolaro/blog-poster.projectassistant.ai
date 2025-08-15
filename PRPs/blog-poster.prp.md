name: "Blog-Poster: Multi-Agent SEO Content Generation and Publishing System"
description: |

## Purpose
Build an automated blog content generation system with multi-agent orchestration for SEO-optimized article creation, fact-checking, and WordPress publishing for ServiceDogUS.

## Core Principles
1. **Autonomous Operation**: System runs independently with minimal human intervention
2. **SEO Excellence**: Every piece of content optimized for search engines
3. **Factual Accuracy**: Legal claims verified, especially ADA compliance
4. **Production Ready**: Docker-based deployment with monitoring and cost controls

---

## Goal
Create a production-ready multi-agent system that monitors competitors, identifies content opportunities, generates high-quality SEO articles, fact-checks them, and publishes to WordPress automatically.

## Why
- **Business value**: Scales content production while maintaining quality
- **SEO advantage**: Systematic approach to ranking for target keywords
- **Legal compliance**: Ensures accuracy in service dog and ADA information
- **Problems solved**: Manual content creation bottleneck, inconsistent publishing schedule

## What
A FastAPI-based orchestration system where:
- Competitor Monitoring Agent tracks industry content trends
- Topic Analysis Agent identifies high-value content opportunities
- Article Generation Agent creates SEO-optimized content
- Legal Fact Checker Agent verifies all claims
- WordPress Publishing Agent handles content deployment

### Success Criteria
- [x] FastAPI service running on port 8088 with health checks
- [x] Docker compose stack with all required services
- [x] WordPress integration via WPGraphQL and REST API
- [x] Pydantic models for type-safe data contracts
- [x] Cost tracking and budget controls
- [ ] Comprehensive test coverage
- [ ] Production deployment via Portainer
- [ ] Automated content pipeline end-to-end

## All Needed Context

### Documentation & References
```yaml
# Core Technologies
- file: app.py
  why: Main FastAPI application with endpoints
  
- file: orchestrator.py
  why: Workflow state management and retry logic
  
- file: wordpress_agent.py
  why: WordPress publishing implementation
  
- file: contracts.py
  why: Pydantic models and data validation
  
- file: docker-compose.yml
  why: Service orchestration and networking

# Configuration
- file: .env.local.example
  why: Required environment variables
  
- file: PROGRESS.md
  why: Current implementation status
```

### Current Architecture
```yaml
Services:
  API:
    port: 8088
    framework: FastAPI
    endpoints:
      - /agent/run
      - /seo/lint
      - /publish/wp
      - /health
      
  Qdrant:
    port: 6333
    purpose: Vector search for semantic similarity
    
  PostgreSQL:
    port: 5433
    extension: pgvector
    purpose: Embeddings storage
    
  Redis:
    port: 6384
    purpose: Job queue and caching

Agents:
  competitor_monitoring:
    tools: [Jina AI scraper]
    output: CompetitorData
    
  topic_analysis:
    input: CompetitorData
    output: TopicRec
    
  article_generation:
    llm: Claude 3.5 Sonnet
    input: TopicRec
    output: ArticleDraft
    
  legal_fact_checker:
    input: ArticleDraft
    output: FactCheckOutput
    
  wordpress_publishing:
    input: ArticleDraft + FactCheckOutput
    output: WordPressPost
```

### Key Implementation Details
```python
# Workflow State Management
class WorkflowState(Enum):
    PENDING = "pending"
    MONITORING = "monitoring"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    FACT_CHECKING = "fact_checking"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"

# SEO Optimization
class ArticleDraft:
    title: str              # H1, 60 chars max
    meta_title: str         # SEO title tag
    meta_desc: str          # 155 chars max
    canonical: HttpUrl      # Canonical URL
    schema_jsonld: dict     # Structured data
    internal_links: List    # Related content
    
# WordPress Integration
auth_methods = [
    "JWT Token",           # Via WPGraphQL JWT
    "Application Password", # WP native auth
    "Basic Auth"           # Fallback
]
```

## Validation Scripts

### 1. Service Health Check
```bash
#!/bin/bash
# validate_services.sh

echo "Checking service health..."

# API health
curl -f http://localhost:8088/health || exit 1

# Qdrant health
curl -f http://localhost:6333/collections || exit 1

# Redis ping
redis-cli -p 6384 ping || exit 1

echo "✅ All services healthy"
```

### 2. SEO Validation
```python
# test_seo.py
import requests

def test_seo_lint():
    response = requests.post(
        "http://localhost:8088/seo/lint",
        json={
            "title": "Service Dog Requirements Under ADA",
            "meta_desc": "Learn about ADA service dog requirements, including the two questions businesses can ask and your rights as a handler.",
            "word_count": 1500,
            "h1_count": 1,
            "h2_count": 5
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert result["valid"] == True
    assert len(result["warnings"]) == 0
```

### 3. WordPress Publishing Test
```bash
#!/bin/bash
# test_publish.sh

# Create test article
curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d '{
    "frontmatter": {
      "title": "Test Article",
      "slug": "test-article",
      "category": "ADA Compliance",
      "tags": ["test"],
      "meta_title": "Test Article - ServiceDogUS",
      "meta_desc": "This is a test article"
    },
    "markdown": "# Test Article\n\nThis is test content.",
    "status": "DRAFT"
  }'
```

## Example Usage

### Generate Article
```bash
curl -X POST http://localhost:8088/agent/run \
  -H "Content-Type: application/json" \
  -d @topic-input.json
```

### Monitor Workflow
```python
# monitor.py
import asyncio
import redis.asyncio as redis

async def monitor_workflow(workflow_id):
    r = await redis.from_url("redis://localhost:6384")
    
    while True:
        state = await r.get(f"workflow:{workflow_id}:state")
        print(f"Current state: {state}")
        
        if state in ["published", "failed"]:
            break
            
        await asyncio.sleep(5)
```

## Production Deployment Checklist

- [ ] Environment variables configured in `.env.local`
- [ ] SSL certificates for WordPress connection
- [ ] API keys for Anthropic/OpenAI
- [ ] Jina AI key for web scraping
- [ ] WordPress user with publishing permissions
- [ ] Monitoring dashboards configured
- [ ] Cost limits set (MAX_COST_PER_ARTICLE, MAX_MONTHLY_COST)
- [ ] Backup strategy for vector stores
- [ ] Rate limiting configured
- [ ] Error alerting setup

## Edge Cases & Error Handling

1. **WordPress Connection Failure**
   - Retry with exponential backoff
   - Store draft locally for manual recovery
   
2. **LLM Rate Limits**
   - Queue articles for later processing
   - Switch to fallback provider (OpenAI)
   
3. **Fact Check Failure**
   - Block publication
   - Alert human reviewer
   - Log disputed claims
   
4. **Cost Overrun**
   - Pause generation at 80% budget
   - Send alert to admin
   - Complete in-progress articles only

## Maintenance & Monitoring

```yaml
Metrics:
  - Articles published per day
  - Average generation time
  - Cost per article
  - SEO score distribution
  - Fact check pass rate
  
Alerts:
  - Service downtime > 5 minutes
  - Cost threshold exceeded
  - Fact check failures > 10%
  - WordPress auth failures
  
Logs:
  - All agent interactions
  - API requests/responses
  - Cost tracking
  - Error traces
```