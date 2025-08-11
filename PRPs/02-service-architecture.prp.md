name: "Service Architecture & Agent Implementation"
description: |

## Purpose
Transform stubbed agents into fully functional, production-ready services with proper job queuing, retry logic, and error handling for reliable content generation at scale.

## Core Principles
1. **Resilience**: Automatic retries, circuit breakers, graceful degradation
2. **Scalability**: Async processing, horizontal scaling capability
3. **Observability**: Comprehensive logging, metrics, and tracing
4. **Modularity**: Clear separation of concerns, pluggable agents

---

## Goal
Implement all five core agents with real functionality, integrated through a robust job queue system using Celery and Redis, with proper error handling and monitoring.

## Why
- **Current State**: Agents are mocked/stubbed, synchronous execution blocks API
- **Production Need**: Async processing, fault tolerance, parallel execution
- **Scale Requirements**: Handle 100+ articles/day, multiple concurrent pipelines
- **Reliability**: 99.9% success rate for content generation

## What
Complete implementation of:
1. **Competitor Monitoring Agent** - Automated content discovery
2. **Topic Analysis Agent** - SEO opportunity identification  
3. **Article Generation Agent** - AI-powered content creation
4. **Legal Fact Checker Agent** - ADA compliance verification
5. **WordPress Publishing Agent** - Automated deployment

### Success Criteria
- [ ] All 5 agents fully implemented with real logic
- [ ] Celery task queue with Redis backend
- [ ] Retry logic with exponential backoff
- [ ] Circuit breaker pattern for external APIs
- [ ] Comprehensive error handling
- [ ] Performance metrics and monitoring
- [ ] 95%+ test coverage on agent logic
- [ ] Parallel pipeline execution support

## All Needed Context

### Current Architecture Issues
```yaml
Problems:
  Synchronous Execution:
    - API blocks during pipeline runs
    - No parallel processing
    - Timeouts on long operations
    
  No Error Recovery:
    - Single failure breaks entire pipeline
    - No retry mechanism
    - Lost work on crashes
    
  Stubbed Implementations:
    - Agents return mock data
    - No real API integrations
    - No actual content generation
```

### Target Architecture
```yaml
Components:
  API Layer:
    - FastAPI (existing)
    - Async endpoints
    - WebSocket for real-time updates
    
  Job Queue:
    - Celery 5.3+
    - Redis as broker
    - Result backend in PostgreSQL
    
  Agent Workers:
    - Separate Celery workers per agent type
    - Horizontal scaling capability
    - Resource isolation
    
  External Services:
    - Jina AI for web scraping
    - Anthropic/OpenAI for content generation
    - Bright Data for competitor monitoring
    - WordPress REST API
```

### Agent Implementations

#### 1. Competitor Monitoring Agent
```python
# src/agents/competitor_monitor.py
from celery import Task
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup

class CompetitorMonitorAgent(Task):
    """Monitors competitor websites for new content"""
    
    def __init__(self):
        self.jina_client = JinaClient()
        self.bright_data = BrightDataClient()
        
    @celery.task(bind=True, max_retries=3)
    def analyze_competitor(self, competitor_url: str) -> Dict:
        """Analyze a competitor website for new content"""
        try:
            # Scrape competitor site
            content = await self.jina_client.scrape(competitor_url)
            
            # Extract articles
            articles = self.extract_articles(content)
            
            # Analyze topics and keywords
            analysis = self.analyze_content_trends(articles)
            
            # Store in database
            self.store_competitor_data(competitor_url, analysis)
            
            return {
                'competitor': competitor_url,
                'new_articles': len(articles),
                'trending_topics': analysis['topics'],
                'keywords': analysis['keywords']
            }
            
        except Exception as e:
            self.retry(countdown=60 * (self.request.retries + 1))
            
    def extract_articles(self, html: str) -> List[Dict]:
        """Extract article data from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # Common article selectors
        selectors = [
            'article',
            '.post',
            '.blog-post',
            '[itemtype*="Article"]'
        ]
        
        for selector in selectors:
            for element in soup.select(selector):
                article = {
                    'title': self.extract_title(element),
                    'url': self.extract_url(element),
                    'date': self.extract_date(element),
                    'content': self.extract_content(element)
                }
                if article['title']:
                    articles.append(article)
                    
        return articles
```

#### 2. Topic Analysis Agent
```python
# src/agents/topic_analyzer.py
from celery import Task
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class TopicAnalyzerAgent(Task):
    """Analyzes competitor content to identify topic opportunities"""
    
    @celery.task(bind=True)
    def identify_opportunities(self, competitor_data: Dict) -> Dict:
        """Identify content gaps and opportunities"""
        
        # Get our existing content
        our_articles = self.get_our_articles()
        
        # Analyze competitor topics
        competitor_topics = self.extract_topics(competitor_data)
        
        # Find content gaps
        gaps = self.find_content_gaps(our_articles, competitor_topics)
        
        # Calculate SEO potential
        opportunities = []
        for gap in gaps:
            opportunity = {
                'topic': gap['topic'],
                'keywords': self.identify_keywords(gap),
                'search_volume': self.get_search_volume(gap['keywords']),
                'competition': self.assess_competition(gap['keywords']),
                'priority_score': self.calculate_priority(gap)
            }
            opportunities.append(opportunity)
            
        # Sort by priority
        opportunities.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return {
            'opportunities': opportunities[:10],
            'total_gaps_found': len(gaps),
            'recommended_topic': opportunities[0] if opportunities else None
        }
        
    def extract_topics(self, competitor_data: Dict) -> List[str]:
        """Extract topics using TF-IDF and clustering"""
        texts = [article['content'] for article in competitor_data['articles']]
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Get top terms
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.sum(axis=0).A1
        top_indices = scores.argsort()[-20:][::-1]
        
        topics = [feature_names[i] for i in top_indices]
        return topics
```

#### 3. Article Generation Agent
```python
# src/agents/article_generator.py
from celery import Task
from anthropic import AsyncAnthropic
import asyncio

class ArticleGeneratorAgent(Task):
    """Generates SEO-optimized articles using Claude"""
    
    def __init__(self):
        self.claude = AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.cost_tracker = CostTracker()
        
    @celery.task(bind=True, max_retries=2)
    async def generate_article(self, topic: Dict) -> Dict:
        """Generate a complete SEO-optimized article"""
        
        # Check cost budget
        if not self.cost_tracker.check_budget():
            raise BudgetExceededException("Monthly budget exceeded")
            
        try:
            # Generate article outline
            outline = await self.generate_outline(topic)
            
            # Generate sections in parallel
            sections = await asyncio.gather(*[
                self.generate_section(section, topic)
                for section in outline['sections']
            ])
            
            # Combine into full article
            article = self.combine_sections(sections)
            
            # Generate SEO metadata
            metadata = await self.generate_metadata(article, topic)
            
            # Internal linking
            article = self.add_internal_links(article)
            
            # Track costs
            self.cost_tracker.record_generation(
                tokens=metadata['total_tokens'],
                cost=metadata['total_cost']
            )
            
            return {
                'title': metadata['title'],
                'content_markdown': article,
                'meta_title': metadata['meta_title'],
                'meta_description': metadata['meta_description'],
                'keywords': topic['keywords'],
                'word_count': len(article.split()),
                'seo_score': self.calculate_seo_score(article, metadata),
                'generation_cost': metadata['total_cost']
            }
            
        except Exception as e:
            if self.request.retries < self.max_retries:
                self.retry(countdown=120)
            raise
            
    async def generate_outline(self, topic: Dict) -> Dict:
        """Generate article outline based on topic"""
        prompt = f"""
        Create a detailed outline for an SEO-optimized article about service dogs.
        
        Topic: {topic['topic']}
        Target Keywords: {', '.join(topic['keywords'])}
        Search Intent: {topic.get('intent', 'informational')}
        
        Requirements:
        - 8-10 main sections
        - Include FAQ section
        - Focus on ADA compliance
        - Target 2000+ words
        
        Return as structured JSON.
        """
        
        response = await self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.content[0].text)
```

#### 4. Legal Fact Checker Agent
```python
# src/agents/fact_checker.py
from celery import Task
import re
from typing import List, Dict

class LegalFactCheckerAgent(Task):
    """Verifies legal claims and ADA compliance statements"""
    
    def __init__(self):
        self.legal_db = LegalDatabase()
        self.ada_rules = self.load_ada_rules()
        
    @celery.task(bind=True)
    def verify_article(self, article: Dict) -> Dict:
        """Verify all legal claims in article"""
        
        # Extract claims
        claims = self.extract_legal_claims(article['content_markdown'])
        
        # Verify each claim
        verification_results = []
        for claim in claims:
            result = {
                'claim': claim['text'],
                'location': claim['position'],
                'verification': self.verify_claim(claim),
                'suggested_correction': None
            }
            
            if not result['verification']['is_accurate']:
                result['suggested_correction'] = self.suggest_correction(claim)
                
            verification_results.append(result)
            
        # Check for required disclaimers
        disclaimers = self.check_disclaimers(article['content_markdown'])
        
        # Calculate accuracy score
        accuracy_score = self.calculate_accuracy_score(verification_results)
        
        return {
            'is_approved': accuracy_score >= 0.95,
            'accuracy_score': accuracy_score,
            'total_claims': len(claims),
            'verified_claims': len([r for r in verification_results if r['verification']['is_accurate']]),
            'corrections_needed': [r for r in verification_results if r['suggested_correction']],
            'missing_disclaimers': disclaimers['missing'],
            'verification_details': verification_results
        }
        
    def extract_legal_claims(self, content: str) -> List[Dict]:
        """Extract legal claims from content"""
        claims = []
        
        # Patterns for legal claims
        patterns = [
            r'under the ADA[^.]*\.',
            r'legally required[^.]*\.',
            r'federal law[^.]*\.',
            r'Title [IVX]+ of[^.]*\.',
            r'\d{1,2} CFR §[\d.]+[^.]*\.',
            r'Americans with Disabilities Act[^.]*\.'
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                claims.append({
                    'text': match.group(),
                    'position': match.start(),
                    'type': 'legal_claim'
                })
                
        return claims
        
    def verify_claim(self, claim: Dict) -> Dict:
        """Verify a legal claim against ADA database"""
        # Check against known ADA rules
        for rule in self.ada_rules:
            if self.claim_matches_rule(claim['text'], rule):
                return {
                    'is_accurate': True,
                    'source': rule['citation'],
                    'confidence': 0.95
                }
                
        return {
            'is_accurate': False,
            'source': None,
            'confidence': 0.0
        }
```

#### 5. WordPress Publishing Agent (Enhanced)
```python
# src/agents/wordpress_publisher.py
from celery import Task
import httpx
from typing import Dict

class WordPressPublisherAgent(Task):
    """Publishes articles to WordPress with SEO optimization"""
    
    @celery.task(bind=True, max_retries=3)
    async def publish_article(self, article: Dict, options: Dict = None) -> Dict:
        """Publish article to WordPress"""
        
        try:
            # Convert markdown to WordPress blocks
            blocks = self.markdown_to_blocks(article['content_markdown'])
            
            # Prepare post data
            post_data = {
                'title': article['title'],
                'content': blocks,
                'status': options.get('status', 'draft'),
                'categories': await self.map_categories(article['keywords']),
                'tags': await self.create_tags(article['keywords']),
                'meta': {
                    '_yoast_wpseo_title': article['meta_title'],
                    '_yoast_wpseo_metadesc': article['meta_description'],
                    '_yoast_wpseo_focuskw': article['keywords'][0]
                }
            }
            
            # Create or update post
            if article.get('wp_post_id'):
                result = await self.update_post(article['wp_post_id'], post_data)
            else:
                result = await self.create_post(post_data)
                
            # Update internal links
            await self.update_internal_links(result['id'])
            
            # Trigger SEO plugin analysis
            await self.trigger_seo_analysis(result['id'])
            
            return {
                'success': True,
                'post_id': result['id'],
                'post_url': result['link'],
                'edit_url': result['edit_link']
            }
            
        except Exception as e:
            if self.request.retries < self.max_retries:
                self.retry(countdown=30 * (self.request.retries + 1))
            raise
```

### Job Queue Configuration

```python
# src/celery_app.py
from celery import Celery
from kombu import Queue

app = Celery('blog_poster')

app.conf.update(
    broker_url='redis://localhost:6384/0',
    result_backend='postgresql://user:pass@localhost:5433/blogposter',
    
    # Task routing
    task_routes={
        'agents.competitor_monitor.*': {'queue': 'monitoring'},
        'agents.topic_analyzer.*': {'queue': 'analysis'},
        'agents.article_generator.*': {'queue': 'generation'},
        'agents.fact_checker.*': {'queue': 'verification'},
        'agents.wordpress_publisher.*': {'queue': 'publishing'}
    },
    
    # Queues
    task_queues=(
        Queue('monitoring', priority=1),
        Queue('analysis', priority=2),
        Queue('generation', priority=3),
        Queue('verification', priority=4),
        Queue('publishing', priority=5)
    ),
    
    # Retry policy
    task_retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    },
    
    # Rate limiting
    task_annotations={
        'agents.article_generator.generate_article': {
            'rate_limit': '10/m'  # 10 articles per minute max
        },
        'agents.competitor_monitor.analyze_competitor': {
            'rate_limit': '30/m'  # 30 sites per minute
        }
    },
    
    # Performance
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True
)
```

### Error Handling & Resilience

```python
# src/utils/circuit_breaker.py
from typing import Callable
import time

class CircuitBreaker:
    """Circuit breaker for external service calls"""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open
        
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'half-open'
            else:
                raise ServiceUnavailableException("Circuit breaker is open")
                
        try:
            result = func(*args, **kwargs)
            if self.state == 'half-open':
                self.state = 'closed'
                self.failure_count = 0
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
                
            raise

# src/utils/retry_strategy.py
from functools import wraps
import random
import time

def exponential_backoff_retry(max_retries=3, base_delay=1, max_delay=60):
    """Decorator for exponential backoff retry"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                        
                    # Calculate delay with jitter
                    delay = min(base_delay * (2 ** retries), max_delay)
                    jitter = random.uniform(0, delay * 0.1)
                    time.sleep(delay + jitter)
                    
            return None
        return wrapper
    return decorator
```

### Monitoring & Observability

```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
pipeline_runs = Counter('pipeline_runs_total', 'Total pipeline runs', ['status'])
agent_tasks = Counter('agent_tasks_total', 'Total agent tasks', ['agent', 'status'])
task_duration = Histogram('task_duration_seconds', 'Task duration', ['agent', 'task'])
active_pipelines = Gauge('active_pipelines', 'Currently active pipelines')
api_errors = Counter('api_errors_total', 'API errors', ['service', 'error_type'])

# Decorators
def track_metrics(agent_name: str, task_name: str):
    """Decorator to track task metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                agent_tasks.labels(agent=agent_name, status='success').inc()
                return result
            except Exception as e:
                agent_tasks.labels(agent=agent_name, status='failure').inc()
                raise
            finally:
                duration = time.time() - start
                task_duration.labels(agent=agent_name, task=task_name).observe(duration)
        return wrapper
    return decorator
```

### Testing Strategy

```python
# tests/test_agents.py
import pytest
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_competitor_monitor_agent():
    """Test competitor monitoring agent"""
    agent = CompetitorMonitorAgent()
    
    with patch('agents.competitor_monitor.JinaClient') as mock_jina:
        mock_jina.scrape.return_value = "<html>...</html>"
        
        result = await agent.analyze_competitor("https://example.com")
        
        assert result['competitor'] == "https://example.com"
        assert 'new_articles' in result
        assert 'trending_topics' in result

@pytest.mark.asyncio
async def test_article_generation_with_retry():
    """Test article generation with retry logic"""
    agent = ArticleGeneratorAgent()
    
    with patch('agents.article_generator.AsyncAnthropic') as mock_claude:
        # Simulate failure then success
        mock_claude.messages.create.side_effect = [
            Exception("API Error"),
            Mock(content=[Mock(text='{"title": "Test Article"})])
        ]
        
        result = await agent.generate_article.retry()
        assert result['title'] == "Test Article"
```

### Deployment Configuration

```yaml
# docker-compose.production.yml
services:
  celery-worker:
    build: .
    command: celery -A src.celery_app worker -l info -Q generation,verification
    environment:
      - C_FORCE_ROOT=true
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 2G
          
  celery-beat:
    build: .
    command: celery -A src.celery_app beat -l info
    
  flower:
    build: .
    command: celery -A src.celery_app flower
    ports:
      - "5555:5555"
```

---

## Implementation Priority
1. **Week 1**: Celery setup and basic job queue
2. **Week 2**: Implement Article Generator and Fact Checker agents
3. **Week 3**: Implement Competitor Monitor and Topic Analyzer
4. **Week 4**: Error handling, monitoring, and testing

## Success Metrics
- 99.9% pipeline completion rate
- < 5 minute average pipeline execution
- Zero data loss on failures
- 100% retry success within 3 attempts
- < 1% error rate on external API calls