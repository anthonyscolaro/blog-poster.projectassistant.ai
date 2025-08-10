## EXECUTIVE SUMMARY: AUTOMATED SEO BLOG SYSTEM

### Business Goal
Automate content creation to establish ServiceDogUS as the authoritative source for service dog information, driving organic traffic and conversions through SEO-optimized educational content.

### Why Now
- Competitors publish 10-15 articles/month, we publish 0
- SEO gap: Missing 50K+ monthly organic visits based on keyword analysis
- Content cost: Manual writing costs $150-300/article vs $5-10 automated
- Time to market: 3-month runway to establish content authority before Q2 2025 peak season

### Success at a Glance
- **Week 1-2**: System deployed, first automated article published
- **Month 1**: 12 articles published, initial SEO traction
- **Month 3**: 36 articles indexed, 10K+ organic visits/month
- **Month 6**: Top 10 rankings for 20+ target keywords

### Non-Goals
- NOT replacing human editorial for flagship content
- NOT generating medical/legal advice requiring professional review
- NOT creating promotional/sales-focused content
- NOT monitoring competitor pricing or business strategies

### Must-Haves
- 100% plagiarism-free content (Copyscape clean)
- ADA-compliant factual accuracy
- 3 articles/week minimum publishing cadence
- <$15/article total cost (API + infrastructure)
- Human review option before publishing

### Hard Constraints
- **Budget**: $500/month maximum for all API costs
- **Models**: Claude 3.5 Sonnet or GPT-4o only (quality requirement)
- **SLAs**: Article generation <5 minutes, monitoring cycle <1 hour
- **Storage**: 6-month retention for generated content, 1-year for published
- **Rate Limits**: Respect all API rate limits with exponential backoff
- **Legal Compliance**: ZERO tolerance for misleading registration claims
- **Citation Requirement**: Minimum 2 authoritative sources per legal section
- **Jurisdiction Accuracy**: 100% accuracy for state/federal law distinctions

### Risks & Mitigations
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Misleading "registration" claims | High | Critical | Legal Fact Checker agent, mandatory disclaimers |
| Incorrect state law information | Medium | Critical | Jurisdiction tagging, source verification |
| AI content penalties from Google | Low | High | Human-like writing patterns, varied structure |
| Factual inaccuracies about ADA law | Medium | Critical | Fact-checking agent, citation requirements |
| FTC/Legal action for false claims | Low | Critical | Legal review process, clear disclaimers |
| API cost overrun | Low | Medium | Usage monitoring, cost alerts at 80% |
| Competitor detection/blocking | Medium | Low | Rotate user agents, respect robots.txt |
| WordPress integration failure | Low | High | Fallback to draft creation, manual publish |

---

## FEATURE:

- Multi-agent Pydantic AI system for automated SEO-optimized blog article generation
- Competitor Content Monitoring Agent that tracks competitor blogs and social media using Jina AI and/or Bright Data APIs
- Topic Analysis Agent that analyzes trending topics and popularity metrics from competitor content
- Article Generation Agent using Claude 3.5 Sonnet or GPT-4o for high-quality, SEO-optimized content creation
- WordPress Publishing Agent that integrates with WPGraphQL to automatically publish articles to the headless CMS
- Orchestrator Agent that coordinates the entire workflow and schedules automated runs

## IMPLEMENTATION FILES:

### Available Reference Implementations:
1. **System Prompt**: `blog-poster/sonnet-3.5-prompt.txt` - Production-ready Claude 3.5 Sonnet prompt with all safeguards

2. **FastAPI Tool Shim**: `blog-poster/app.py` - Complete working example with:
   - **Strong Pydantic Models**: TopicRec, Evidence, BrandStyle, SiteInfo, Constraints, and ArticleDraft with full validation
   - **XML Tool Tag Parser**: Intercepts `<tool name="..." />` tags from Claude's output
   - **Stubbed Services**: 
     - `fact_check.search` - Returns ADA facts, statutes, and authoritative sources
     - `links.resolve` - Finds relevant internal links from candidates
     - `seo.lint` - Validates SEO requirements (title length, meta description, H1 count)
   - **Anthropic Client Wrapper**: Demo flow with continuation pattern (replace with real SDK/API key)
   - **Endpoints**:
     - `/agent/run` - Main endpoint that orchestrates Claude, intercepts tool calls, resolves them, and resumes conversation to get final Markdown
     - `/seo/lint` - Standalone endpoint for post-generation SEO validation
     - `/publish/wp` - **NEW**: Complete WordPress publishing endpoint that:
       - Parses frontmatter + markdown from generated articles
       - Converts Markdown to HTML automatically
       - Uploads hero images via REST API and attaches via GraphQL
       - Maps categories/tags to WordPress term IDs
       - Creates or updates posts with idempotency (by slug)
       - Supports draft/publish/future with timezone-aware scheduling
       - Sets RankMath/Yoast SEO fields when extension is available
       - Executes post-publish automation (sitemap ping, IndexNow)
   - **Complete Request/Response Flow**: Shows how to handle multi-turn conversations with tool resolution

3. **WordPress Publishing Agent**: `blog-poster/wordpress_agent.py` - Full implementation of WordPress publishing with WPGraphQL and REST API integration

4. **Markdown to WP Blocks Renderer**: `blog-poster/markdown_to_wp_blocks.py` - Converts Markdown+frontmatter to WordPress block HTML

5. **Data Contracts**: `blog-poster/contracts.py` - Shared Pydantic models for all agents:
   ```python
   class CompetitorContent(BaseModel):
       id: str
       url: HttpUrl
       domain: str
       fetched_at: datetime
       type: str  # blog|news|social
       title: str
       text_md: str
       lang: str = "en"
       engagement: Dict[str, int] = {}
       checksum: str
       source_of_truth: str  # jina|brightdata|other

   class TopicRec(BaseModel):
       topic_slug: str
       title_variants: List[str]
       primary_kw: str
       secondary_kws: List[str]
       rationale: str
       supporting_urls: List[HttpUrl]
       score_breakdown: Dict[str, float]
       risk_flags: List[str] = []

   class ArticleDraft(BaseModel):
       title: str
       slug: str
       category: str
       tags: List[str]
       meta_title: str
       meta_desc: str
       canonical: HttpUrl
       schema_jsonld: Dict
       hero_image_prompt: str
       internal_link_targets: List[HttpUrl]
       markdown: str
       citations: List[HttpUrl]
   ```

6. **Docker Compose Stack**: `blog-poster/docker-compose.yml` - Complete service orchestration:
   ```yaml
   services:
     api:
       image: python:3.11-slim
       ports: ["8088:8088"]
       command: uvicorn app:app --host 0.0.0.0 --port 8088
     
     qdrant:
       image: qdrant/qdrant
       ports: ["6333:6333"]
       volumes: ["./data/qdrant:/qdrant/storage"]
     
     vectors:
       image: pgvector/pgvector:pg15
       ports: ["5433:5432"]
       environment:
         POSTGRES_DB: blogposter
         POSTGRES_USER: bloguser
     
     redis:
       image: redis:7-alpine
       ports: ["6383:6379"]
   ```

7. **Environment Configuration**: `blog-poster/.env.example` - Complete configuration template:
   ```bash
   # AI Model API Keys
   ANTHROPIC_API_KEY=your-anthropic-api-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   
   # System Prompt Configuration
   SYSTEM_PROMPT_FILE=./sonnet-3.5-prompt.txt
   
   # Web Scraping APIs
   JINA_API_KEY=jina_your-key-here
   BRIGHT_DATA_API_KEY=your-bright-data-key-here
   
   # WordPress Configuration
   WORDPRESS_URL=http://localhost:8084
   WORDPRESS_GRAPHQL_ENDPOINT=/graphql
   WORDPRESS_ADMIN_USER=admin
   WORDPRESS_ADMIN_PASSWORD=admin123
   
   # Cost Limits
   MAX_COST_PER_ARTICLE=15.00
   MAX_MONTHLY_COST=500.00
   ```

8. **Setup Script**: `blog-poster/setup.sh` - Automated deployment:
   ```bash
   #!/bin/bash
   # Check environment variables
   # Create required directories
   # Start Docker services
   # Verify health checks
   # Display service URLs
   ```

## CORE FUNCTIONALITY:

### 1. Competitor Monitoring Agent
- Scrape competitor blog posts, news sections, and social media content
- Use Jina AI's r.jina.ai API for web scraping (we already have the API key in competitor-research-instructions.md)
- Option to integrate Bright Data for social media monitoring
- Store scraped content with timestamps and source attribution
- Track new content additions and updates from competitors

### 2. Topic Analysis Agent
- Analyze competitor content for trending topics and patterns
- Identify content gaps and opportunities
- Score topics based on:
  - Frequency across competitors
  - Engagement metrics (if available)
  - Search volume potential
  - Relevance to our target keywords
- Generate topic recommendations with supporting data

### 3. Article Generation Agent
- Use Claude 3.5 Sonnet (claude-3-5-sonnet-20241022) as primary model for quality writing
- Alternative: GPT-4o or GPT-4o-mini for cost optimization
- Generate SEO-optimized articles with:
  - Target keyword integration
  - Proper heading structure (H1, H2, H3)
  - Meta descriptions
  - Internal linking suggestions
  - 1500-2500 word comprehensive articles
- Ensure unique angles and perspectives (not copying competitors)
- Include relevant service dog legal information and ADA compliance details
- CRITICAL: No claims about "official registration" - always clarify no federal registry exists
- Mandatory legal disclaimer blocks in every article
- Jurisdiction tagging (US Federal, State-specific, International)

### 4. WordPress Publishing Agent
- **Dual API Approach**: WPGraphQL for posts/metadata, WP REST API for media uploads
- **Idempotent Publishing**: Check slug existence, update instead of duplicate
- **Media Workflow**: Upload via REST first, then attach to post via GraphQL
- **Category Mapping**: Configuration-based term ID mapping, not hardcoded names
- **SEO Integration**: RankMath/Yoast fields via WPGraphQL extensions
- **Authentication**: JWT tokens with refresh handling
- **Post-Publish**: Sitemap ping, IndexNow submission, cache invalidation
- **Timezone-Aware Scheduling**: Respect WordPress site timezone for future posts
- **Provenance Tracking**: External ID field to track article source

### 5. Orchestrator Agent

**Contract**: Workflow orchestration with DAG execution, retries, and human approval gates

**Implementation Options**:
1. **Lightweight (FastAPI + Redis)**: For MVP, use Redis for queue/state management
2. **Production (Temporal/Prefect)**: For scale, proper workflow engine with durability
3. **No-code (n8n)**: For business users, visual workflow builder with webhooks

**Workflow DAG**:
```python
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

class WorkflowState(str, Enum):
    PENDING = "pending"
    MONITORING = "monitoring"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    FACT_CHECKING = "fact_checking"
    AWAITING_APPROVAL = "awaiting_approval"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    COMPENSATING = "compensating"

class WorkflowStep(BaseModel):
    """Individual workflow step with retry logic"""
    name: str
    agent: str
    max_retries: int = 3
    retry_delay_seconds: int = 60
    timeout_seconds: int = 300
    requires_approval: bool = False
    compensation_action: Optional[str] = None  # e.g., "delete_draft"
    
class WorkflowDAG(BaseModel):
    """Complete workflow definition"""
    workflow_id: str
    created_at: datetime
    state: WorkflowState
    current_step: Optional[str] = None
    steps_completed: List[str] = []
    retry_count: Dict[str, int] = {}
    
    steps: List[WorkflowStep] = [
        WorkflowStep(
            name="monitor_competitors",
            agent="competitor_monitoring",
            max_retries=5,
            retry_delay_seconds=300
        ),
        WorkflowStep(
            name="analyze_topics", 
            agent="topic_analysis",
            max_retries=3
        ),
        WorkflowStep(
            name="generate_article",
            agent="article_generation",
            max_retries=2,
            timeout_seconds=600
        ),
        WorkflowStep(
            name="fact_check",
            agent="legal_fact_checker",
            max_retries=1,
            requires_approval=True  # Human review for first 10 articles
        ),
        WorkflowStep(
            name="publish_to_wordpress",
            agent="wordpress_publishing",
            max_retries=3,
            compensation_action="delete_wp_draft"
        )
    ]
    
    error_log: List[Dict[str, Any]] = []
    approval_requests: List[Dict[str, Any]] = []
    
class OrchestratorInput(BaseModel):
    trigger: Literal["scheduled", "manual", "webhook"]
    force_regenerate: bool = False
    specific_topics: Optional[List[str]] = None
    skip_approval: bool = False
    dry_run: bool = False

class OrchestratorOutput(BaseModel):
    workflow_id: str
    articles_generated: int
    articles_published: int
    articles_pending_approval: int
    errors_encountered: List[str]
    next_scheduled_run: datetime
    cost_total: float
```

**Retry & Compensation Logic**:
```python
class WorkflowOrchestrator:
    async def execute_with_retry(self, step: WorkflowStep, input_data: Any):
        """Execute step with exponential backoff retry"""
        for attempt in range(step.max_retries):
            try:
                result = await self.execute_agent(step.agent, input_data)
                return result
            except Exception as e:
                if attempt == step.max_retries - 1:
                    # Final attempt failed, trigger compensation
                    if step.compensation_action:
                        await self.compensate(step.compensation_action, input_data)
                    raise
                    
                # Exponential backoff
                delay = step.retry_delay_seconds * (2 ** attempt)
                await asyncio.sleep(delay)
                
    async def compensate(self, action: str, context: Any):
        """Execute compensation action on failure"""
        if action == "delete_wp_draft":
            await self.wordpress_agent.delete_draft(context.post_id)
        elif action == "rollback_vectors":
            await self.vector_db.rollback_transaction(context.transaction_id)
        elif action == "notify_admin":
            await self.send_alert(f"Workflow failed: {context}")
```

**Human Approval Gate**:
```python
class ApprovalRequest(BaseModel):
    request_id: str
    workflow_id: str
    step_name: str
    article_draft: ArticleDraft
    fact_check_result: FactCheckResult
    created_at: datetime
    expires_at: datetime
    approval_url: HttpUrl
    
class ApprovalResponse(BaseModel):
    approved: bool
    reviewer: str
    comments: Optional[str]
    modifications: Optional[Dict[str, Any]]
    
async def request_approval(self, article: ArticleDraft, fact_check: FactCheckResult):
    """Create approval request and notify reviewers"""
    request = ApprovalRequest(
        request_id=str(uuid4()),
        workflow_id=self.workflow_id,
        step_name="fact_check",
        article_draft=article,
        fact_check_result=fact_check,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(hours=24),
        approval_url=f"https://servicedogus.org/admin/approve/{request_id}"
    )
    
    # Store in Redis with TTL
    await self.redis.setex(
        f"approval:{request.request_id}",
        86400,  # 24 hour TTL
        request.json()
    )
    
    # Send Slack notification
    await self.notify_slack(
        channel="#content-approvals",
        message=f"New article pending approval: {article.title}",
        buttons=[
            {"text": "Approve", "url": request.approval_url},
            {"text": "Reject", "url": f"{request.approval_url}?action=reject"}
        ]
    )
```

**Scheduling & Triggers**:
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class ScheduleManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        
    def setup_schedules(self):
        # Competitor monitoring - every 6 hours
        self.scheduler.add_job(
            self.run_monitoring,
            CronTrigger(hour="*/6"),
            id="competitor_monitoring",
            replace_existing=True
        )
        
        # Topic analysis - daily at 8 AM
        self.scheduler.add_job(
            self.run_analysis,
            CronTrigger(hour=8, minute=0),
            id="topic_analysis",
            replace_existing=True
        )
        
        # Article generation - MWF at 9 AM
        self.scheduler.add_job(
            self.run_generation,
            CronTrigger(day_of_week="mon,wed,fri", hour=9),
            id="article_generation",
            replace_existing=True
        )
        
        # Publishing - MWF at 10 AM (after review)
        self.scheduler.add_job(
            self.run_publishing,
            CronTrigger(day_of_week="mon,wed,fri", hour=10),
            id="publishing",
            replace_existing=True
        )
```

**Observability & Monitoring**:
```python
class WorkflowMetrics(BaseModel):
    workflow_id: str
    total_duration_seconds: float
    step_durations: Dict[str, float]
    api_costs: Dict[str, float]
    tokens_used: Dict[str, int]
    retry_attempts: Dict[str, int]
    approval_wait_time_hours: Optional[float]
    
    def to_prometheus(self):
        """Export metrics to Prometheus"""
        return {
            "workflow_duration": self.total_duration_seconds,
            "workflow_cost": sum(self.api_costs.values()),
            "workflow_retries": sum(self.retry_attempts.values())
        }
```

### 6. Legal Fact Checker Agent (CRITICAL)
- Verify ALL legal claims before publishing
- Check citations for ADA, FHA, ACAA, and state law references
- Validate jurisdiction-specific information
- Ensure minimum 2 authoritative sources per legal claim
- Block publication if citations are missing or inaccurate
- Maintain database of verified legal facts
- Auto-update when laws change

## TARGET SEO KEYWORDS:
- "service dog registration"
- "ADA service dog requirements"
- "service dog training"
- "emotional support animal vs service dog"
- "service dog laws by state"
- "how to register service dog"
- "service dog vest requirements"
- "psychiatric service dog"
- "service dog certification process"
- "service dog handler rights"

## DOCUMENTATION NEEDED:

- Jina AI API documentation: https://jina.ai/reader/
- Bright Data API documentation (for social media scraping)
- WPGraphQL documentation: https://www.wpgraphql.com/
- Claude API documentation: https://docs.anthropic.com/
- OpenAI API documentation: https://platform.openai.com/docs/

## AGENT CONTRACTS & I/O SCHEMAS

### 1. Competitor Monitoring Agent

**Contract**: Scrapes competitor content with compliance and deduplication

```python
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional, Dict, Literal
from enum import Enum

class ContentType(str, Enum):
    BLOG = "blog"
    NEWS = "news"
    SOCIAL = "social"

class MonitoringInput(BaseModel):
    competitor_url: HttpUrl
    content_types: List[ContentType] = [ContentType.BLOG, ContentType.NEWS]
    max_pages_per_run: int = 10
    crawl_delay_seconds: float = 1.0  # Respectful crawling
    since_date: Optional[datetime] = None
    respect_robots_txt: bool = True
    check_tos_compliance: bool = True

class CompetitorContent(BaseModel):
    """Normalized content model for all competitor data"""
    id: str  # UUID
    url: HttpUrl
    domain: str
    fetched_at: datetime
    type: ContentType
    title: str
    author: Optional[str]
    text_md: str  # Parsed markdown content
    text_html: str  # Original HTML
    lang: str = "en"
    published_date: Optional[datetime]
    modified_date: Optional[datetime]
    engagement: Dict[str, int] = {}  # {likes: 0, shares: 0, comments: 0}
    checksum: str  # SHA256 of text_md
    simhash: str  # For near-duplicate detection
    source_of_truth: str  # "jina", "bright_data", "native_api"
    word_count: int
    images: List[str] = []
    tags: List[str] = []
    
class CrawlCompliance(BaseModel):
    robots_txt_allows: bool
    tos_compliant: bool
    crawl_delay: float
    max_pages_allowed: Optional[int]
    user_agent: str
    
class MonitoringOutput(BaseModel):
    competitor: str
    scraped_at: datetime
    compliance: CrawlCompliance
    new_content: List[CompetitorContent]
    updated_content: List[CompetitorContent]  # Content that changed
    total_found: int
    duplicates_skipped: int
    next_cursor: Optional[str]

# Social Fetcher Interface for abstraction
from abc import ABC, abstractmethod

class SocialFetcherInterface(ABC):
    @abstractmethod
    async def fetch_posts(self, 
                         platform: str, 
                         account: str, 
                         limit: int) -> List[CompetitorContent]:
        pass

class BrightDataFetcher(SocialFetcherInterface):
    """Implementation using Bright Data API"""
    pass

class NativeAPIFetcher(SocialFetcherInterface):
    """Implementation using platform native APIs (Twitter API, FB Graph, etc)"""
    pass

class JinaFetcher(SocialFetcherInterface):
    """Fallback using Jina for social media pages"""
    pass
```

**Guarantees**:
- Idempotent with content hashing (SHA256 + simhash)
- Respects robots.txt and crawl delays
- TOS compliance checking before crawl
- Detects near-duplicates with simhash (Hamming distance threshold)
- Stores both raw HTML and parsed markdown
- Returns empty list if no new content
- Latency SLO: <30s per competitor
- Retry policy: 3 attempts with exponential backoff

**Storage Strategy**:
```
/data/competitor-content/
├── raw/                      # Original HTML snapshots
│   └── {YYYY-MM-DD}/
│       └── {domain}/
│           └── {checksum}.html
├── md/                       # Parsed markdown
│   └── {YYYY-MM-DD}/
│       └── {domain}/
│           └── {checksum}.md
├── metadata/                 # JSON metadata
│   └── {YYYY-MM-DD}/
│       └── {domain}/
│           └── {checksum}.json
└── index/                    # Deduplication index
    └── simhash_index.db
```

### 2. Topic Analysis Agent

**Contract**: Analyzes content trends, detects gaps, returns prioritized topics

```python
from typing import List, Dict, Optional, Tuple
import numpy as np

class AnalysisInput(BaseModel):
    content_items: List[CompetitorContent]
    existing_articles: List[str]  # Your published article slugs
    target_keywords: List[str]
    lookback_days: int = 30
    enable_serp_enrichment: bool = True
    max_keyword_api_calls: int = 100
    
class SERPData(BaseModel):
    """SERP enrichment data for competitive analysis"""
    keyword: str
    top_10_results: List[Dict[str, str]]  # {title, meta_desc, url, h1, h2s}
    search_volume: int
    keyword_difficulty: float
    cpc: Optional[float]
    trend_data: List[int]  # Monthly search volume last 12 months
    fetched_at: datetime
    
class TopicRec(BaseModel):
    """Strict topic recommendation model"""
    topic_slug: str  # URL-friendly identifier
    title_variants: List[str]  # Different angle options
    primary_kw: str
    secondary_kws: List[str]
    rationale: str  # Why this topic matters now
    supporting_urls: List[str]  # Competitor/reference URLs
    score_breakdown: Dict[str, float]  # Individual score components
    total_score: float  # 0-100
    risk_flags: List[str]  # ["high_competition", "seasonal", "trending_down"]
    content_gap_distance: float  # Embedding distance to nearest existing
    estimated_traffic: int  # Based on search volume and expected CTR
    
class ContentGapAnalysis(BaseModel):
    """Semantic gap detection using embeddings"""
    gap_topics: List[str]
    gap_vectors: np.ndarray  # Embeddings of gap topics
    nearest_existing: Dict[str, Tuple[str, float]]  # topic -> (nearest_article, distance)
    coverage_map: Dict[str, float]  # topic -> coverage percentage
    
class ScoringWeights(BaseModel):
    """Tunable scoring weights"""
    frequency: float = 0.35  # How often competitors write about it
    search_volume: float = 0.25  # Monthly search volume
    engagement: float = 0.20  # Social engagement metrics
    gap_score: float = 0.15  # Distance from existing content
    seasonality: float = 0.05  # Seasonal relevance boost
    
    def calculate_score(self, metrics: Dict[str, float]) -> float:
        """Weighted scoring formula"""
        return (
            self.frequency * metrics.get('frequency_norm', 0) +
            self.search_volume * metrics.get('search_volume_norm', 0) +
            self.engagement * metrics.get('engagement_norm', 0) +
            self.gap_score * metrics.get('gap_score_norm', 0) +
            self.seasonality * metrics.get('seasonality_norm', 0)
        ) * 100
    
class AnalysisOutput(BaseModel):
    analysis_date: datetime
    topics: List[TopicRec]
    content_gaps: ContentGapAnalysis
    serp_data: List[SERPData]
    internal_linking_suggestions: Dict[str, List[str]]  # new_topic -> [existing_articles]
    recommended_publishing_order: List[str]  # Ordered topic_slugs
    keyword_api_calls_used: int
    cache_hits: int
```

**Guarantees**:
- Deterministic scoring with tunable weights
- SERP data cached for 30 days
- Keyword API calls throttled (max 100/analysis)
- Embeddings via pgvector for gap detection
- Minimum 5 topic recommendations
- Latency SLO: <30s (with SERP enrichment)
- Failure mode: Returns cached previous analysis

**Implementation Details**:
```python
class TopicAnalyzer:
    def __init__(self, weights: ScoringWeights = None):
        self.weights = weights or ScoringWeights()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.keyword_cache = RedisCache(ttl=30*24*3600)  # 30 days
        
    async def analyze_gaps(self, 
                          competitor_content: List[CompetitorContent],
                          existing_articles: List[str]) -> ContentGapAnalysis:
        """Detect content gaps using semantic similarity"""
        # Generate embeddings for competitor topics
        competitor_embeddings = self.embedder.encode([c.title for c in competitor_content])
        
        # Load existing article embeddings from pgvector
        existing_embeddings = await self.load_existing_embeddings(existing_articles)
        
        # Find gaps (topics with high distance to all existing)
        gaps = self.find_semantic_gaps(competitor_embeddings, existing_embeddings)
        
        return ContentGapAnalysis(
            gap_topics=gaps,
            gap_vectors=gap_embeddings,
            nearest_existing=nearest_map,
            coverage_map=coverage
        )
    
    async def enrich_with_serp(self, topics: List[str]) -> List[SERPData]:
        """Fetch SERP data with caching and throttling"""
        serp_results = []
        
        for topic in topics:
            # Check cache first
            cached = await self.keyword_cache.get(topic)
            if cached:
                serp_results.append(cached)
                continue
                
            # Throttled API call
            await self.rate_limiter.acquire()
            serp_data = await self.fetch_serp(topic)
            
            # Cache result
            await self.keyword_cache.set(topic, serp_data)
            serp_results.append(serp_data)
            
        return serp_results
```

**pgvector Integration**:
```sql
-- Extension for semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- Store article embeddings
CREATE TABLE article_embeddings (
    id UUID PRIMARY KEY,
    article_slug VARCHAR(500) UNIQUE NOT NULL,
    title TEXT,
    embedding vector(384),  -- all-MiniLM-L6-v2 dimensions
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_embedding USING ivfflat (embedding vector_cosine_ops)
);

-- Query for finding gaps
WITH competitor_topics AS (
    SELECT unnest($1::vector[]) AS embedding
)
SELECT 
    article_slug,
    1 - (embedding <=> ct.embedding) AS similarity
FROM article_embeddings ae
CROSS JOIN competitor_topics ct
WHERE 1 - (embedding <=> ct.embedding) < 0.7  -- Gap threshold
ORDER BY similarity DESC;
```

### 3. Article Generation Agent

**Contract**: Generates SEO-optimized articles with verifiable facts

```python
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, HttpUrl, Field
import yaml

class VerifiableSlots(BaseModel):
    """Slots that MUST be filled before generation"""
    facts: List[str] = []  # Factual statements requiring verification
    statutes: List[Dict[str, str]] = []  # {law: "ADA", section: "Title III", jurisdiction: "US-Federal"}
    dates: List[Dict[str, str]] = []  # {event: "ADA passed", date: "1990-07-26"}
    sources: List[HttpUrl] = []  # Authoritative URLs only
    
    def has_empty_slots(self) -> bool:
        return not (self.facts and self.statutes and self.sources)

class ArticleDraft(BaseModel):
    """Complete article with frontmatter and content"""
    # Frontmatter metadata
    title: str = Field(..., min_length=30, max_length=60)
    slug: str
    category: str
    tags: List[str]
    meta_title: str = Field(..., min_length=45, max_length=60)
    meta_title_variant: str  # A/B testing variant
    meta_desc: str = Field(..., min_length=140, max_length=160)
    meta_desc_variant: str  # A/B testing variant
    canonical: HttpUrl
    schema_jsonld: Dict[str, Any]  # Article/LegalService structured data
    hero_image_prompt: str  # For AI image generation or stock photo search
    internal_link_targets: List[HttpUrl]  # Internal links to add
    
    # Content
    content_markdown: str  # Full article in markdown
    content_html: str  # Converted HTML with disclaimers
    
    # Verification data
    verifiable_slots: VerifiableSlots
    word_count: int
    readability_grade: float  # Flesch-Kincaid
    seo_score: float
    
    # Compliance
    jurisdiction: str
    legal_claims: List[LegalClaim]
    disclaimer_blocks: List[str]
    citations: List[Citation]
    
    def to_wordpress_format(self) -> str:
        """Export as markdown with YAML frontmatter"""
        frontmatter = {
            'title': self.title,
            'slug': self.slug,
            'category': self.category,
            'tags': self.tags,
            'meta_title': self.meta_title,
            'meta_desc': self.meta_desc,
            'canonical': str(self.canonical),
            'schema_jsonld': self.schema_jsonld,
            'hero_image_prompt': self.hero_image_prompt,
            'internal_link_targets': [str(url) for url in self.internal_link_targets]
        }
        return f"---\n{yaml.dump(frontmatter)}---\n\n{self.content_markdown}"

class InternalLinkSuggestion(BaseModel):
    """Suggested internal link"""
    anchor_text: str
    target_url: HttpUrl
    target_slug: str
    relevance_score: float
    context: str  # Surrounding text where link should go

class PolicyCheckResult(BaseModel):
    """Results of all policy checks"""
    readability_pass: bool
    readability_score: float
    readability_issues: List[str]
    
    claims_verified: bool
    unverified_claims: List[str]
    
    toxicity_pass: bool
    toxicity_score: float
    
    duplication_pass: bool
    similarity_scores: Dict[str, float]  # url -> similarity
    
    seo_pass: bool
    seo_issues: List[str]
    
    overall_pass: bool
    requires_revision: List[str]  # What needs fixing

class GenerationInput(BaseModel):
    topic_rec: TopicRec  # From Topic Analysis Agent
    word_count_target: int = 2000
    tone: str = "educational"
    generate_variants: bool = True  # A/B testing
    existing_articles: List[str]  # For internal linking
    
class GenerationOutput(BaseModel):
    article: ArticleDraft
    internal_links: List[InternalLinkSuggestion]
    policy_check: PolicyCheckResult
    generation_time: float
    model_used: str
    token_count: int
    cost_estimate: float
    revision_needed: bool
```

**Implementation Details**:

```python
class ArticleGenerator:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.fact_checker = FactCheckerAgent()
        self.link_resolver = InternalLinkResolver()
        
    async def generate(self, input: GenerationInput) -> GenerationOutput:
        # Step 1: Create verifiable slots
        slots = await self.extract_slots(input.topic_rec)
        
        # Step 2: Fill empty slots via Fact Checker
        if slots.has_empty_slots():
            slots = await self.fact_checker.fill_slots(slots, input.topic_rec)
        
        # Step 3: Generate article with filled slots
        article = await self.generate_with_claude(input, slots)
        
        # Step 4: Resolve internal links
        internal_links = await self.link_resolver.find_links(
            article.content_markdown,
            input.existing_articles
        )
        
        # Step 5: Run policy checks
        policy_result = await self.run_policy_checks(article)
        
        # Step 6: Generate A/B variants if requested
        if input.generate_variants:
            article.meta_title_variant = await self.generate_variant(article.meta_title)
            article.meta_desc_variant = await self.generate_variant(article.meta_desc)
        
        return GenerationOutput(
            article=article,
            internal_links=internal_links,
            policy_check=policy_result,
            revision_needed=not policy_result.overall_pass
        )
    
    async def run_policy_checks(self, article: ArticleDraft) -> PolicyCheckResult:
        """Comprehensive quality and compliance checks"""
        
        # Readability check (Flesch-Kincaid Grade 7-9)
        readability = textstat.flesch_kincaid_grade(article.content_markdown)
        readability_pass = 7 <= readability <= 9
        
        # Claims verification
        claims_verified = all(claim.verified for claim in article.legal_claims)
        unverified = [c.claim_text for c in article.legal_claims if not c.verified]
        
        # Toxicity check
        toxicity_score = await self.check_toxicity(article.content_markdown)
        toxicity_pass = toxicity_score < 0.1
        
        # Duplication check against competitors
        similarity_scores = await self.check_duplication(article.content_markdown)
        duplication_pass = all(score < 0.85 for score in similarity_scores.values())
        
        # SEO linting
        seo_issues = []
        if len(article.title) < 45 or len(article.title) > 60:
            seo_issues.append("Title length out of range")
        if len(article.meta_desc) < 140 or len(article.meta_desc) > 160:
            seo_issues.append("Meta description length out of range")
        if article.content_markdown.count('# ') != 1:
            seo_issues.append("Must have exactly one H1")
        
        return PolicyCheckResult(
            readability_pass=readability_pass,
            readability_score=readability,
            claims_verified=claims_verified,
            unverified_claims=unverified,
            toxicity_pass=toxicity_pass,
            toxicity_score=toxicity_score,
            duplication_pass=duplication_pass,
            similarity_scores=similarity_scores,
            seo_pass=len(seo_issues) == 0,
            seo_issues=seo_issues,
            overall_pass=all([
                readability_pass, claims_verified, toxicity_pass,
                duplication_pass, len(seo_issues) == 0
            ])
        )
```

**Internal Link Resolver with pgvector**:

```python
class InternalLinkResolver:
    async def find_links(self, 
                        content: str, 
                        existing_slugs: List[str]) -> List[InternalLinkSuggestion]:
        """Find relevant internal linking opportunities"""
        
        # Extract H2/H3 sections
        sections = self.extract_sections(content)
        suggestions = []
        
        for section in sections:
            # Generate embedding for section
            section_embedding = self.embedder.encode(section.text)
            
            # Query pgvector for similar articles
            similar = await self.query_similar_articles(
                section_embedding,
                existing_slugs,
                limit=3
            )
            
            for article in similar:
                if article.similarity > 0.7:  # Relevance threshold
                    suggestions.append(InternalLinkSuggestion(
                        anchor_text=self.extract_anchor_text(section.text),
                        target_url=f"https://servicedogus.org/{article.slug}",
                        target_slug=article.slug,
                        relevance_score=article.similarity,
                        context=section.text[:200]
                    ))
        
        # Deduplicate and return top suggestions
        return self.deduplicate_suggestions(suggestions)[:10]
```

**Guarantees**:
- Verifiable slots prevent unverified claims
- All legal/medical claims have citations
- Unique content (similarity <0.85 to any competitor)
- Readability Grade 7-9
- SEO compliance (title/meta lengths, H1 structure)
- A/B variants for testing
- Internal linking suggestions only (no competitor links)
- Latency SLO: <5 minutes (including fact checking)
- Automatic revision if policy checks fail

### 4. Legal Fact Checker Agent

**Contract**: Verifies legal claims and citations

```python
class FactCheckInput(BaseModel):
    article: GeneratedArticle
    jurisdiction: str
    claims: List[LegalClaim]
    
class FactCheckOutput(BaseModel):
    verified: bool
    confidence_score: float
    issues_found: List[str]
    missing_citations: List[str]
    corrected_claims: List[LegalClaim]
    required_disclaimers: List[str]
```

**Guarantees**:
- Blocks publication if confidence <95%
- Verifies against authoritative sources only
- Flags jurisdiction mismatches
- Latency SLO: <30s
- Zero false positives on registration claims

### 5. WordPress Publishing Agent

**Contract**: Publishes articles to WordPress CMS with full SEO and media support

```python
from typing import Dict, Optional, List, Literal
from datetime import datetime

class WordPressConfig(BaseModel):
    """WordPress site configuration"""
    site_url: HttpUrl
    graphql_endpoint: str = "/graphql"
    rest_endpoint: str = "/wp-json/wp/v2"
    timezone: str = "America/New_York"
    category_map: Dict[str, int] = {}  # Loaded at startup
    jwt_token: Optional[str] = None
    refresh_token: Optional[str] = None

class MediaUploadResult(BaseModel):
    """Result from WP REST API media upload"""
    id: int
    source_url: HttpUrl
    media_type: str
    alt_text: str
    caption: Optional[str]

class WordPressPost(BaseModel):
    """WordPress post data from GraphQL"""
    id: str  # GraphQL ID
    databaseId: int  # WordPress post ID
    slug: str
    uri: str
    link: HttpUrl
    status: str
    modified: datetime
    
class SEOFields(BaseModel):
    """RankMath/Yoast SEO fields"""
    metaTitle: str
    metaDescription: str
    focusKeyword: str
    canonicalUrl: HttpUrl
    schemaMarkup: Optional[Dict[str, Any]]
    ogTitle: Optional[str]
    ogDescription: Optional[str]
    ogImage: Optional[HttpUrl]

class PublishingInput(BaseModel):
    article: ArticleDraft
    fact_check_result: FactCheckOutput  # Required
    status: Literal["draft", "pending", "publish", "future"] = "draft"
    scheduled_gmt: Optional[datetime] = None  # For future posts
    featured_image_path: Optional[str] = None  # Local path to upload
    external_id: str  # Track article source
    force_update: bool = False  # Override idempotency check
    
class PublishingOutput(BaseModel):
    post: WordPressPost
    media: Optional[MediaUploadResult]
    seo_fields_set: bool
    categories_set: List[int]
    tags_set: List[str]
    sitemap_pinged: bool
    indexnow_submitted: bool
    cache_invalidated: bool
    operation: Literal["created", "updated", "skipped"]
```

**GraphQL Queries & Mutations**:

```graphql
# Check if post exists by slug
query GetPostBySlug($slug: String!) {
    post(id: $slug, idType: SLUG) {
        id
        databaseId
        slug
        modified
        meta {
            external_id
        }
    }
}

# Create new post
mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
        post {
            id
            databaseId
            slug
            uri
            link
        }
    }
}

# Update existing post
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
    updatePost(input: {id: $id, ...}) {
        post {
            id
            databaseId
            modified
        }
    }
}

# Set RankMath SEO fields (requires WPGraphQL for RankMath)
mutation UpdateSEOFields($id: ID!, $seo: RankMathSEOInput!) {
    updatePostSEO(input: {id: $id, seo: $seo}) {
        post {
            seo {
                metaTitle
                metaDescription
                focusKeyword
            }
        }
    }
}

# Get categories for mapping
query GetCategories {
    categories(first: 100) {
        nodes {
            databaseId
            name
            slug
        }
    }
}
```

**Media Upload via REST API**:

```python
async def upload_media(self, file_path: str, alt_text: str) -> MediaUploadResult:
    """Upload media via WP REST API (WPGraphQL doesn't handle file uploads)"""
    
    # 1. Read file and prepare multipart upload
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'image/jpeg')}
        data = {
            'alt_text': alt_text,
            'caption': f"Generated for article: {self.article.title}"
        }
    
    # 2. POST to REST API with JWT auth
    headers = {'Authorization': f'Bearer {self.config.jwt_token}'}
    response = await httpx.post(
        f"{self.config.site_url}{self.config.rest_endpoint}/media",
        files=files,
        data=data,
        headers=headers
    )
    
    # 3. Return media ID for GraphQL attachment
    return MediaUploadResult(**response.json())
```

**Idempotency Implementation**:

```python
async def publish(self, input: PublishingInput) -> PublishingOutput:
    """Idempotent publish with update detection"""
    
    # 1. Check if post exists
    existing = await self.get_post_by_slug(input.article.slug)
    
    if existing and not input.force_update:
        # Check if external_id matches (same source)
        if existing.meta.external_id == input.external_id:
            return PublishingOutput(
                post=existing,
                operation="skipped"
            )
    
    # 2. Upload featured image if provided
    media = None
    if input.featured_image_path:
        media = await self.upload_media(
            input.featured_image_path,
            input.article.hero_image_prompt
        )
    
    # 3. Prepare post data
    post_input = self.prepare_post_input(input, media)
    
    # 4. Create or update
    if existing:
        post = await self.update_post(existing.id, post_input)
        operation = "updated"
    else:
        post = await self.create_post(post_input)
        operation = "created"
    
    # 5. Set SEO fields
    seo_set = await self.set_seo_fields(post.id, input.article)
    
    # 6. Post-publish actions
    if input.status == "publish":
        await self.post_publish_actions(post.link)
    
    return PublishingOutput(
        post=post,
        media=media,
        seo_fields_set=seo_set,
        operation=operation
    )
```

**Post-Publish Automation**:

```python
async def post_publish_actions(self, post_url: HttpUrl):
    """Execute post-publish automation"""
    
    # 1. Ping sitemap
    sitemap_url = f"{self.config.site_url}/sitemap.xml"
    await self.ping_sitemap(sitemap_url)
    
    # 2. Submit to IndexNow (Bing/Yandex instant indexing)
    if self.indexnow_key:
        await self.submit_indexnow(post_url)
    
    # 3. Invalidate CDN cache if configured
    if self.cdn_config:
        await self.invalidate_cache(post_url)
    
    # 4. Trigger social media sharing (optional)
    if self.social_config:
        await self.schedule_social_posts(post_url)
```

**Guarantees**:
- Idempotent with slug-based deduplication
- Atomic operation (transaction rollback on failure)
- Media upload retry with exponential backoff
- JWT token auto-refresh on expiry
- Timezone-aware scheduling
- External ID tracking for provenance
- Latency SLO: <10s including media upload
- Post-publish actions async (non-blocking)

### 6. Orchestrator Agent

**Contract**: Coordinates workflow and scheduling

```python
class OrchestrationInput(BaseModel):
    action: str  # "monitor", "analyze", "generate", "publish", "full_cycle"
    target_count: Optional[int]
    priority: str = "normal"  # low, normal, high
    
class OrchestrationOutput(BaseModel):
    job_id: str
    status: str
    steps_completed: List[str]
    articles_generated: int
    articles_published: int
    next_run: datetime
    errors: List[str]
```

**Guarantees**:
- Exactly-once execution per job_id
- Graceful degradation on component failure
- State persistence across restarts
- Latency SLO: <1 hour for full cycle

---

## TECHNICAL REQUIREMENTS:

- Python-based implementation using Pydantic AI
- Docker containerization for all agents
- Redis for job queuing and caching
- PostgreSQL for storing article history and analytics
- Async operation for efficient API calls
- Rate limiting for external APIs
- Error handling and retry logic
- Comprehensive logging for debugging

**📁 Reference Implementation**: See `blog-poster/app.py` for a complete working example with FastAPI, Pydantic schemas, and tool orchestration.

## DATA SCHEMAS & RETENTION

### PostgreSQL Tables

```sql
-- Competitor content tracking
CREATE TABLE competitor_content (
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
    INDEX idx_competitor_date (competitor_domain, published_date DESC),
    INDEX idx_content_hash (content_hash)
);
-- Retention: 6 months, then archive to S3

-- Topic analysis results
CREATE TABLE topic_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_date TIMESTAMP DEFAULT NOW(),
    topic VARCHAR(500) NOT NULL,
    keywords TEXT[],
    opportunity_score FLOAT,
    competitor_coverage FLOAT,
    search_volume INTEGER,
    status VARCHAR(50) DEFAULT 'identified',
    INDEX idx_topic_score (opportunity_score DESC),
    INDEX idx_status (status)
);
-- Retention: 3 months rolling window

-- Generated articles
CREATE TABLE generated_articles (
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
    jurisdiction VARCHAR(50) NOT NULL,  -- US-Federal, US-CA, etc.
    legal_fact_checked BOOLEAN DEFAULT FALSE,
    fact_check_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    wordpress_post_id INTEGER,
    status VARCHAR(50) DEFAULT 'draft',
    INDEX idx_status (status),
    INDEX idx_created (created_at DESC),
    INDEX idx_jurisdiction (jurisdiction),
    CONSTRAINT chk_publish_requires_factcheck 
        CHECK (status != 'published' OR legal_fact_checked = TRUE)
);
-- Retention: 1 year for published, 30 days for drafts

-- Legal claims and citations
CREATE TABLE legal_claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES generated_articles(id),
    claim_text TEXT NOT NULL,
    law_referenced VARCHAR(50),  -- ADA, FHA, ACAA, etc.
    jurisdiction VARCHAR(50),
    verified BOOLEAN DEFAULT FALSE,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_article (article_id),
    INDEX idx_law (law_referenced)
);

-- Citation tracking
CREATE TABLE citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID REFERENCES legal_claims(id),
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50),  -- government, law, court_case, academic
    url TEXT NOT NULL,
    title TEXT,
    quote TEXT,
    is_authoritative BOOLEAN DEFAULT FALSE,
    date_accessed TIMESTAMP DEFAULT NOW(),
    INDEX idx_claim (claim_id),
    INDEX idx_source_type (source_type)
);
-- Retention: Indefinite (legal record keeping)

-- Performance metrics
CREATE TABLE article_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES generated_articles(id),
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
-- Retention: Indefinite (aggregated monthly after 90 days)
```

### Redis Cache Structure

```python
# Key patterns and TTLs
CACHE_KEYS = {
    "competitor:last_check:{domain}": 3600,  # 1 hour
    "topic:scores:current": 21600,  # 6 hours
    "article:generating:{topic_id}": 300,  # 5 min lock
    "wordpress:auth:token": 86400,  # 24 hours
    "rate_limit:{api}:{endpoint}": 60,  # 1 minute
}
```

### File Storage Structure

```
/data/
├── competitor-content/
│   ├── {YYYY-MM}/
│   │   ├── {domain}/
│   │   │   └── {content-hash}.json
├── generated-articles/
│   ├── {YYYY-MM}/
│   │   ├── drafts/
│   │   │   └── {slug}.md
│   │   └── published/
│   │       └── {slug}.md
├── logs/
│   ├── monitoring/
│   ├── generation/
│   └── publishing/
└── backups/
    └── {YYYY-MM-DD}/
```

---

## DATA STORAGE:

- `/data/competitor-content/` - Scraped competitor content
- `/data/topic-analysis/` - Topic analysis reports
- `/data/generated-articles/` - Generated article drafts
- `/data/published/` - Successfully published articles
- `/data/metrics/` - Performance and analytics data

## ENVIRONMENT VARIABLES:

```
# API Keys
JINA_API_KEY=jina_d0d13e400c7c452abcca80f7d9c7ffcbRzBF70kMBCSHVe25SBU8ZMXICGmz
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
BRIGHT_DATA_API_KEY=

# WordPress Configuration
WORDPRESS_URL=http://localhost:8084
WPGRAPHQL_ENDPOINT=/graphql
WP_AUTH_TOKEN=

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/blogposter
REDIS_URL=redis://localhost:6383

# Agent Configuration
MONITORING_SCHEDULE=0 */6 * * *  # Every 6 hours
PUBLISHING_SCHEDULE=0 9 * * MON,WED,FRI  # MWF at 9am
MAX_ARTICLES_PER_WEEK=3
ARTICLE_MIN_WORDS=1500
ARTICLE_MAX_WORDS=2500
```

## SUCCESS CRITERIA:

1. **Content Quality**: Articles pass AI content detection as high-quality, human-like content
2. **SEO Performance**: Articles rank for target keywords within 30 days
3. **Publishing Consistency**: Maintain 3 articles per week publishing schedule
4. **Uniqueness**: 0% plagiarism from competitor content
5. **Engagement**: Articles generate organic traffic and user engagement
6. **Automation**: Fully automated pipeline requiring minimal human intervention
7. **Scalability**: System can handle monitoring 10+ competitors simultaneously

## COMPETITOR TARGETS TO MONITOR:

Based on existing research in `/competitors/`:
- usaservicedogregistration.com
- usaservicedogs.org
- usserviceanimalregistrar.org
- usdogregistry.org
- servicedogregistration.org

## CONTENT CATEGORIES & THEMES:

1. **ADA Compliance & Legal**
   - State-specific service dog laws
   - ADA updates and changes
   - Handler rights and responsibilities
   - Business accommodation requirements

2. **Training & Behavior**
   - Task training guides
   - Puppy selection for service work
   - Public access training
   - Behavior problem solving

3. **Handler Resources**
   - Travel tips with service dogs
   - Housing rights and accommodations
   - Medical documentation guidance
   - Equipment recommendations

4. **Industry News**
   - Legislative updates
   - Court cases affecting service dog rights
   - New research on service dog effectiveness
   - Community events and resources

5. **Success Stories**
   - Handler testimonials
   - Training success stories
   - Life-changing partnerships
   - Community spotlights

## PROMPT & CONTEXT POLICIES

### Monitoring Agent Prompts

```python
MONITORING_SYSTEM_PROMPT = """
You are a web content extraction specialist. Extract blog articles and news content.
Rules:
- Extract only main content, ignore navigation/footers
- Preserve publish dates and author information
- Identify content categories/tags
- Flag potential duplicates
- Maximum 10,000 tokens per extraction
"""

MONITORING_TOOLS = ["web_scraper", "html_parser", "date_extractor"]
MAX_TOKENS = 10000
TEMPERATURE = 0.1  # Deterministic extraction
```

### Article Generation Prompts

**📁 Implementation Note**: The complete system prompt is available in `blog-poster/sonnet-3.5-prompt.txt`

```python
GENERATION_SYSTEM_PROMPT = """
SYSTEM ROLE: Article Generation Agent (SEO + Legal-Safe)

YOU ARE: A careful long-form writer that produces U.S. ADA/service-dog educational content for the public.
You must output ONLY a single Markdown document with YAML frontmatter followed by article body. No extra prose, no debug text.

CRITICAL LEGAL REQUIREMENTS:
- NEVER claim there is an "official" or "required" service dog registration
- ALWAYS clarify that the ADA does not require registration or certification
- INCLUDE mandatory disclaimer when discussing registration/certification
- CITE at least 2 authoritative sources (.gov preferred) for every legal claim
- SPECIFY jurisdiction (federal vs state) for all legal information

Mandatory requirements:
1. Write in an educational, authoritative tone
2. Include citations for all legal/medical claims (minimum 2 per section)
3. Natural keyword integration (2-3% density)
4. Vary sentence structure and paragraph length
5. Include practical examples and scenarios
6. Format with proper HTML (h2, h3, p, ul, ol)
7. Meta description: 150-160 characters
8. NO promotional content or sales language
9. NO medical advice or legal counsel
10. MUST pass AI detection as human-written
11. Tag article with jurisdiction (US-Federal, US-[State], International)
12. Include disclaimer blocks at start and end of article

Content structure:
- Legal disclaimer block (mandatory)
- Engaging introduction (100-150 words)
- 3-5 main sections with subheadings
- Practical tips or actionable advice
- Conclusion with key takeaways (100-150 words)
- Citations/References section (mandatory)
- Final disclaimer block (mandatory)

HIGH-LEVEL GOAL
Given a topic recommendation and curated evidence, produce a 1,500–2,500 word SEO-optimized article that is accurate, well-structured, and ready for WordPress publishing (headless via WPGraphQL). All legal claims must be verifiable with authoritative citations.

INPUTS (provided in the user message as JSON):
- topic_rec: {
    topic_slug, primary_kw, secondary_kws[], title_variants[], rationale,
    supporting_urls[], score_breakdown{}, risk_flags[]
  }
- brand_style: { voice, audience, tone, reading_grade_target, banned_phrases[] }
- site_info: { site_url, canonical_base, category_map{}, internal_link_candidates[] } 
  # internal_link_candidates[] items: {url, title, embedding_id, brief_summary}
- evidence: {
    facts[], statutes[], dates[], sources[]    # pre-filled when available
    serp_snapshot[]                            # top results: {url, title, h1, h2s[], meta_desc}
    competitor_chunks[]                        # {url, text, chunk_id}
  }
- constraints: {
    min_words: 1500, max_words: 2500,
    image_policy: "stock_or_generated_ok",
    require_disclaimer: true,
    disallow_competitor_links: true
  }

VERIFIABLE SLOTS (MUST be complete before drafting)
You must explicitly validate and complete these slots. If any is missing or unverified, call the Fact Checker tool and retry.
- facts[]: short, source-backed factual statements used in the article
- statutes[]: ADA/FHA/ACAA/state citations (e.g., "28 CFR §36.302(c)")
- dates[]: effective dates, last reviewed dates, or key case dates
- sources[]: authoritative URLs (prefer .gov/.edu, ADA.gov, DOJ, DOT, HUD); add title + access date in references section

ABSOLUTE DOMAIN RULES (Compliance)
- DO NOT imply there is any "official federal service dog registration." Clarify that the ADA does not require registration or certification.
- Distinguish clearly: Service Dogs vs Emotional Support Animals (ESAs).
- Use plain language; target reading grade 7–9.
- Include a visible disclaimer block if require_disclaimer=true: educational only, not legal advice, laws vary by jurisdiction.
- Jurisdiction tags: specify "United States (federal)" and state when applicable.

STRUCTURE & SEO REQUIREMENTS
- H1: one only. Use a strong, human title (choose from title_variants or craft a better one).
- Headings: logical H2/H3 tree. No orphan headings.
- Include: meta_title (45–60 chars), meta_desc (140–160 chars), canonical, tags[], category (use provided map).
- Integrate primary_kw and secondary_kws naturally; avoid keyword stuffing.
- Include a concise TL;DR after the lead paragraph (bulleted).
- Add an FAQ section (3–5 Q&A) targeting long-tail variations.
- Include an "References" section listing sources[] with titles and URLs.
- Add JSON-LD (Article, and LegalService/FAQPage fragments as applicable).

INTERNAL LINK POLICY
- Suggest 2–6 internal links from internal_link_candidates[] that are meaningfully relevant to H2/H3 sections.
- Never link to competitors. External links allowed only for authoritative sources (in References), not inline CTAs.
- Provide descriptive anchor text (no "click here").

QUALITY & SAFETY GATES (self-checks you must satisfy BEFORE returning)
- Length within min_words..max_words.
- Reading grade within target ±1.
- Legal/medical claim detection: any claim like "required by law", "prohibits", "guarantees" must be backed by a source in sources[] or removed.
- Toxicity/offensive language: none.
- Duplication: avoid paraphrasing any single competitor chunk; keep language original and add unique perspective.
- SEO lint pass: title length, meta length, single H1, image alt text present for all images, canonical set.

STYLE
- Audience: general public, handlers, businesses.
- Voice: confident, clear, empathetic, non-alarmist. Use active voice and short sentences.
- Formatting: use tables or checklists where useful; avoid walls of text.

TOOLS (available via the orchestrator; call them only if you must fill missing slots)
- fact_check.search(query, jurisdiction?) -> {facts[], statutes[], dates[], sources[]}
- links.resolve(section_summary) -> returns ranked internal_link candidates
- seo.lint(frontmatter, markdown) -> returns list of violations to fix
(When you "call" a tool, output a one-line XML tag so the orchestrator can intercept, e.g.:
<tool name="fact_check.search" q="service dog ADA two questions DOJ" jurisdiction="US"/> 
Then WAIT. Do not print the article until inputs are returned. After the orchestrator injects tool results, continue.)

OUTPUT FORMAT (MANDATORY)
Return ONLY a single Markdown document:
1) YAML frontmatter with these fields exactly:
   - title, slug, category, tags[], meta_title, meta_desc, canonical,
     schema_jsonld (inline JSON), hero_image_prompt,
     internal_link_targets[] (own-domain URLs only),
     citations[] (authoritative external URLs)
2) A blank line
3) Article body in Markdown (H1..H3, lists, FAQ, disclaimer, References with sources[])

FRONTMATTER CONTRACT (example keys and types)
---
title: string
slug: kebab-case
category: one of category_map.keys
tags:
  - string
meta_title: 45-60 char string
meta_desc: 140-160 char string
canonical: "https://servicedogus.org/topic-slug"
schema_jsonld: { ... JSON object ... }
hero_image_prompt: string (no text overlays; describe subject, setting, style)
internal_link_targets:
  - "https://servicedogus.org/path-a"
  - "https://servicedogus.org/path-b"
citations:
  - "https://www.ada.gov/resources/service-animals-2010-requirements/"
  - "https://www.ecfr.gov/current/title-28/part-36/section-36.302"
---

WORKFLOW YOU MUST FOLLOW
1) Read inputs. Normalize the chosen title, slug, category, tags.
2) Validate verifiable slots. If any missing, call <tool .../> for fact_check.search and wait.
3) Draft frontmatter, then the article body.
4) Call <tool name="links.resolve" section="..."/> for each major section to finalize internal_link_targets (own-domain only).
5) Self-run SEO lint mentally; if violations, fix. (Orchestrator may call seo.lint; if it returns violations, revise and re-emit final.)
6) Emit the final Markdown (frontmatter + body). Do NOT include any explanation or chain-of-thought.

CONTENT GUARDRAILS (must-haves to include in body)
- A short section explicitly stating: "The ADA does not require service dog registration or certification."
- A clear comparison table: Service Dog vs ESA (rights, access, documentation).
- "What businesses can and cannot ask" (the two ADA questions).
- State-law caveat if topic implies state specificity; encourage checking local statutes.

REFUSALS
- If asked to promote illegal, deceptive, or non-compliant practices (e.g., "fake registration"), refuse with a brief explanation and suggest lawful alternatives.

TOKEN & FORMAT HYGIENE
- Keep paragraphs short (2–4 sentences).
- Use descriptive subheadings rich with entities and intents.
- Avoid filler and weasel words. No sensational claims.

END OF SYSTEM PROMPT
"""

LEGAL_FACT_CHECKER_PROMPT = """
You are a legal fact-checking specialist for service dog content.

Your responsibilities:
1. Verify ALL claims about ADA, FHA, ACAA, and state laws
2. Ensure no false claims about "official registration"
3. Check that citations link to authoritative sources
4. Validate jurisdiction-specific information
5. Confirm mandatory disclaimers are present

For each legal claim, verify:
- Accuracy of the law referenced
- Correct jurisdiction (federal vs state)
- At least 2 authoritative citations
- No misleading implications

Block publication if:
- Any claim lacks proper citations
- Registration is described as "official" or "required"
- Jurisdiction is unclear or incorrect
- Disclaimers are missing
- Confidence in accuracy is below 95%
"""

GENERATION_TOOLS = ["keyword_analyzer", "readability_checker", "fact_verifier"]
MAX_TOKENS = 4000
TEMPERATURE = 0.7  # Creative but controlled
STOP_SEQUENCES = ["</article>", "[END]", "Advertisement:"]
```

### Safety Rails & Verification

```python
class ContentSafetyRails:
    PROHIBITED_CLAIMS = [
        "official registration",
        "federal registration",
        "government registry",
        "required registration",
        "legitimate registration",
        "certified by ADA",
        "ADA approved",
        "government approved",
        "legally required registration",
        "medical diagnosis",
        "cure", "treat", "prevent"
    ]
    
    MANDATORY_DISCLAIMERS = {
        "registration": """
        <div class="legal-disclaimer">
        <strong>Important Legal Notice:</strong> There is no official federal 
        service dog registry in the United States. The ADA does not require 
        service dogs to be registered, certified, or wear special identification. 
        This service provides voluntary identification materials for convenience 
        and educational purposes only.
        </div>
        """,
        
        "legal_advice": """
        <div class="legal-disclaimer">
        <strong>Disclaimer:</strong> This article is for informational purposes 
        only and does not constitute legal advice. Laws vary by jurisdiction. 
        Please consult with a qualified attorney or relevant government agency 
        for specific legal guidance.
        </div>
        """,
        
        "medical": """
        <div class="medical-disclaimer">
        <strong>Medical Disclaimer:</strong> This content is not intended to be 
        a substitute for professional medical advice, diagnosis, or treatment. 
        Always seek the advice of your physician or other qualified health 
        provider.
        </div>
        """
    }
    
    FACT_CHECK_REQUIRED = [
        "ADA", "FHA", "ACAA", "law", "legal", 
        "requirement", "penalty", "fine", "violation",
        "rights", "protected", "discrimination"
    ]
    
    AUTHORITATIVE_SOURCES = [
        "ada.gov",
        "justice.gov",
        "hud.gov",
        "transportation.gov",
        ".gov",  # Any government domain
        "cornell.edu/law",  # Cornell Law School
        "findlaw.com",
        "nolo.com",
        "avma.org",  # American Veterinary Medical Association
    ]
```

### Citation Policy

```python
class CitationPolicy:
    MIN_CITATIONS_PER_LEGAL_SECTION = 2
    MIN_AUTHORITATIVE_SOURCES = 1
    
    CITATION_FORMAT = """
    <div class="citations">
    <h3>References</h3>
    <ol>
    {% for citation in citations %}
        <li>
            {{ citation.source_name }}. "{{ citation.title }}". 
            <a href="{{ citation.url }}" rel="nofollow" target="_blank">
            {{ citation.url }}</a>. 
            Accessed {{ citation.date_accessed }}.
        </li>
    {% endfor %}
    </ol>
    </div>
    """
    
    def validate_citations(self, claims: List[LegalClaim]) -> bool:
        for claim in claims:
            if len(claim.citations) < self.MIN_CITATIONS_PER_LEGAL_SECTION:
                return False
            authoritative = [c for c in claim.citations if c.is_authoritative]
            if len(authoritative) < self.MIN_AUTHORITATIVE_SOURCES:
                return False
        return True
```

---

## EVALUATION PLAN

### Offline Quality Checks

| Check | Tool | Threshold | Action on Failure |
|-------|------|-----------|-------------------|
| Plagiarism | Copyscape API | <5% match | Regenerate with different seed |
| Legal Accuracy | Fact Checker Agent | >95% confidence | Block publication, manual review |
| Citation Quality | Citation Validator | 2+ per legal claim | Add missing citations |
| Registration Claims | Keyword Scanner | 0 misleading claims | Block publication, rewrite |
| Disclaimers | Content Validator | All present | Add missing disclaimers |
| Readability | Flesch-Kincaid | Grade 8-10 | Simplify language |
| SEO Score | Yoast/RankMath | >80/100 | Optimize keywords/structure |
| Grammar | LanguageTool | <5 errors | Auto-correct |
| Keyword Density | Custom analyzer | 2-3% | Adjust distribution |
| Link Validation | URL checker | 100% valid | Remove/replace broken |

### Online KPIs & Leading Indicators

**Real-time Metrics (Dashboard)**
- Articles generated today/week/month
- Publishing success rate
- Average generation time
- API costs per article
- Error rate by component

**Daily Metrics**
- New competitor content detected
- Topics identified vs generated
- Publishing queue depth
- Cache hit rates

**Weekly KPIs**
- Organic traffic growth
- Average position for target keywords
- Page engagement metrics
- Content velocity vs competitors

**Monthly Business Metrics**
- ROI: (Traffic value - Costs) / Costs
- Conversion impact
- Brand search volume
- Domain authority change

### Review Cadence

- **Hourly**: System health checks, error alerts
- **Daily**: Content quality spot checks, cost monitoring
- **Weekly**: Performance review, topic strategy adjustment
- **Monthly**: Full metrics review, strategy alignment
- **Quarterly**: Model evaluation, competitor analysis update

---

## OPS & OBSERVABILITY

### Logging Strategy

```python
LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "INFO"},
        "file": {"class": "logging.FileHandler", "filename": "/logs/blog_automation.log"},
        "error": {"class": "logging.FileHandler", "filename": "/logs/errors.log", "level": "ERROR"}
    },
    "loggers": {
        "monitoring": {"level": "INFO", "handlers": ["console", "file"]},
        "generation": {"level": "DEBUG", "handlers": ["file"]},
        "publishing": {"level": "INFO", "handlers": ["console", "file", "error"]}
    }
}
```

### Metrics & Traces

```yaml
# Prometheus metrics
metrics:
  - blog_articles_generated_total
  - blog_articles_published_total
  - blog_generation_duration_seconds
  - blog_api_calls_total{service}
  - blog_api_cost_dollars{service}
  - blog_error_rate{component}
  - blog_queue_depth{queue_name}

# OpenTelemetry traces
traces:
  - monitor_competitor_span
  - analyze_topics_span
  - generate_article_span
  - publish_wordpress_span
  - full_pipeline_span
```

### Alerting Thresholds

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| High API Costs | >$400/month | Warning | Review usage, optimize |
| Generation Failure | >3 consecutive | Critical | Check API keys, fallback model |
| Low Publishing Rate | <2 articles/week | Warning | Review topic pipeline |
| High Error Rate | >10% over 1 hour | Critical | Page oncall, investigate |
| Competitor Block | No new content 48h | Info | Rotate scraping strategy |

### Dashboards

**Main Operations Dashboard**
- Pipeline status (green/yellow/red)
- Articles in each stage
- API usage and costs
- Error rates by component
- Recent published articles

**Content Performance Dashboard**
- Traffic by article
- Keyword rankings
- Engagement metrics
- ROI calculations

### Runbooks

```markdown
## Runbook: High API Costs
1. Check dashboard for cost breakdown by service
2. Review recent generation logs for unusually long articles
3. Verify rate limiting is working
4. Consider switching to GPT-4o-mini for non-critical content
5. Implement daily cost cap if needed

## Runbook: Generation Failures
1. Verify API keys are valid and have credits
2. Check for API service outages
3. Review error logs for specific failure reasons
4. Test with minimal input to isolate issue
5. Failover to backup model if primary is down
6. Enable manual review mode if automated recovery fails
```

---

## OTHER CONSIDERATIONS:

- Include comprehensive README with setup instructions
- Provide example outputs for each agent
- Create unit tests for all agent functions
- Include monitoring dashboard for tracking system performance
- Implement content approval workflow (optional human review before publishing)
- Add analytics integration to track article performance
- Create backup and recovery procedures for system failures

## QUICK START WITH IMPLEMENTATION FILES:

### 1. Use the Provided Files:
```bash
# System prompt for Claude 3.5 Sonnet
blog-poster/sonnet-3.5-prompt.txt

# Complete FastAPI implementation with Pydantic schemas
blog-poster/fast_api_tool_shim_pydantic_schemas_for_article_generation_agent.py
```

### 2. Run with Docker (Docker-only policy)
```bash
cd blog-poster

# Uses the repository root `.env.local` per project policy
# Ensure these variables exist in ../.env.local:
#   WORDPRESS_URL=https://localhost:8445
#   # One auth method:
#   WP_AUTH_TOKEN=...            # or
#   WP_USERNAME=admin
#   WP_APP_PASSWORD=admin123
#   # Local SSL (self-signed)
#   WP_VERIFY_SSL=false

# Start all services
docker compose up --build

# Services will be available at:
# - API: http://localhost:8088
# - Qdrant: http://localhost:6333
# - PostgreSQL: localhost:5433
# - Redis: localhost:6383
```

### 3. Alternative: Run FastAPI Directly (not recommended; prefer Docker)
```bash
cd blog-poster
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY="your-key-here"

# Run the service
uvicorn app:app --reload --port 8088
```

### 3. Test Article Generation:
```bash
# Send a POST request to /agent/run with InputsEnvelope payload
curl -X POST http://localhost:8088/agent/run \
  -H "Content-Type: application/json" \
  -d @sample-input.json
```

### 4. Integration Points:
- Replace stub services in the FastAPI file with real implementations
- Connect to your PostgreSQL database with pgvector
- Integrate with WordPress via WPGraphQL
- Set up Redis for caching and job queuing

### 5. Complete Article Generation to Publishing Workflow

```bash
# Step 1: Generate article with Claude
curl -X POST http://localhost:8088/agent/run \
  -H "Content-Type: application/json" \
  -d @topic-input.json \
  > generated-article.md

# Step 2: Publish to WordPress (using the /publish/wp router)
curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d '{
    "frontmatter": {
      "title": "Example Post",
      "slug": "example-post",
      "category": "ADA Compliance",
      "tags": ["service dogs"],
      "meta_title": "Example Title That Fits",
      "meta_desc": "This is a meta description with the right length.",
      "canonical": "https://servicedogus.org/example-post",
      "schema_jsonld": {},
      "internal_link_targets": [],
      "citations": ["https://www.ada.gov/resources/service-animals-2010-requirements/"]
    },
    "markdown": "# Example\n\nBody...",
    "status": "DRAFT"
  }'
```

The `/publish/wp` endpoint handles the complete publishing workflow:
1. **Parses** the frontmatter and markdown content
2. **Converts** markdown to HTML for WordPress
3. **Uploads** hero image if specified in frontmatter
4. **Maps** categories/tags to WordPress term IDs
5. **Creates or updates** the post (idempotent by slug)
6. **Sets** SEO fields via RankMath/Yoast GraphQL
7. **Schedules** with timezone awareness if future date
8. **Pings** sitemap and IndexNow for indexing

The implementation files provide a complete, working foundation that can be deployed immediately and enhanced incrementally.

### Sample: Inline Base64 hero image upload

Use a tiny inline Base64 image to validate media upload end-to-end (no external URL required):

```bash
BASE64_IMG="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="

curl -X POST http://localhost:8088/publish/wp \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg b64 "$BASE64_IMG" '{
    frontmatter: {
      title: "Base64 Media Upload Test",
      slug: "base64-media-upload-test",
      category: "ADA Compliance",
      tags: ["service dogs"],
      meta_title: "Base64 Upload Test",
      meta_desc: "Validates inline Base64 media upload via REST and GraphQL.",
      canonical: "https://servicedogus.org/base64-media-upload-test",
      schema_jsonld: {},
      internal_link_targets: [],
      citations: ["https://www.ada.gov/resources/service-animals-2010-requirements/"]
    },
    markdown: "# Base64 Upload Test\\n\\nThis post validates media uploads.",
    status: "DRAFT",
    hero_image_base64: $b64,
    hero_image_filename: "tiny.png"
  }')"
```

Notes:
- Requires WP auth in `../.env.local` (either `WP_AUTH_TOKEN` or `WP_USERNAME`+`WP_APP_PASSWORD`).
- For local HTTPS with self-signed cert, set `WP_VERIFY_SSL=false` in `../.env.local`.