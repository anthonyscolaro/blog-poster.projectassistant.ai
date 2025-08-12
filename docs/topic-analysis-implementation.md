# Topic Analysis Agent - Implementation Guide

## FEATURE:

- Pydantic AI-powered Topic Analysis Agent with multiple sub-agents and real SEO data sources
- Google Ads Keyword Planner integration for keyword research and search volume data
- Screaming Frog SEO Spider integration for competitor analysis and technical SEO insights
- Multi-agent architecture with specialized research tools for comprehensive topic analysis
- Real-time trend analysis using Google Trends and social media signals
- Content gap identification through competitor content analysis
- CLI interface for running topic analysis and generating recommendations

## ARCHITECTURE:

### Primary Agent: Topic Analysis Orchestrator
- Coordinates multiple data sources and sub-agents
- Aggregates insights from keyword research, competitor analysis, and trend data
- Generates prioritized topic recommendations with SEO metrics

### Sub-Agents:

1. **Keyword Research Agent**
   - Google Ads API integration (using MCC account)
   - Keyword Planner data extraction
   - Search volume, competition, and CPC analysis
   - Keyword clustering and semantic grouping

2. **Competitor Analysis Agent**
   - Screaming Frog API integration
   - Competitor content crawling and analysis
   - SERP feature identification
   - Content structure and optimization patterns

3. **Trend Analysis Agent**
   - Google Trends API (pytrends)
   - Reddit API for community insights
   - Social media trend detection
   - Seasonal pattern identification

4. **Content Gap Agent**
   - Jina AI for content extraction
   - Topic modeling and clustering
   - Gap scoring algorithm
   - Opportunity prioritization

## DATA SOURCES:

### 1. Google Ads Keyword Planner (via MCC)
```python
# Required credentials
GOOGLE_ADS_CLIENT_ID = "your-client-id"
GOOGLE_ADS_CLIENT_SECRET = "your-client-secret"
GOOGLE_ADS_REFRESH_TOKEN = "your-refresh-token"
GOOGLE_ADS_DEVELOPER_TOKEN = "your-developer-token"
GOOGLE_ADS_CUSTOMER_ID = "your-mcc-customer-id"

# Data available:
- Exact search volumes
- Competition metrics
- CPC bid ranges
- Keyword ideas and variations
- Historical metrics
- Forecast data
```

### 2. Screaming Frog SEO Spider
```python
# Required credentials
SCREAMING_FROG_LICENSE = "your-license-key"
SCREAMING_FROG_API_URL = "http://localhost:8089"  # Local API

# Data available:
- Competitor URL structure
- Title/meta optimization
- Header analysis (H1, H2, etc.)
- Internal linking patterns
- Schema markup usage
- Content length analysis
- Image optimization
```

### 3. Free Supplementary Sources
```python
# Google Trends
- Search interest over time
- Regional interest data
- Related queries and topics
- Rising vs. top queries

# People Also Ask (via SERP scraping)
- Related questions
- Question clusters
- Intent mapping

# Reddit API
- Trending discussions
- Community pain points
- User language patterns
```

## IMPLEMENTATION COMPONENTS:

### 1. Core Dependencies
```python
# requirements.txt
pydantic-ai>=0.1.0
google-ads>=24.0.0
pytrends>=4.9.0
praw>=7.7.0  # Reddit API
httpx>=0.27.0
beautifulsoup4>=4.12.0
selenium>=4.15.0  # For SERP scraping
pandas>=2.1.0
numpy>=1.24.0
scikit-learn>=1.3.0  # For clustering
```

### 2. Project Structure
```
src/
├── agents/
│   └── topic_analysis/
│       ├── __init__.py
│       ├── agent.py           # Main orchestrator agent
│       ├── tools.py           # Tool functions
│       ├── prompts.py         # System prompts
│       └── sub_agents/
│           ├── keyword_research.py
│           ├── competitor_analysis.py
│           ├── trend_analysis.py
│           └── content_gap.py
├── integrations/
│   ├── google_ads/
│   │   ├── client.py
│   │   ├── keyword_planner.py
│   │   └── utils.py
│   ├── screaming_frog/
│   │   ├── api_client.py
│   │   ├── crawler.py
│   │   └── parser.py
│   └── scrapers/
│       ├── serp_scraper.py
│       └── people_also_ask.py
├── models/
│   ├── keywords.py
│   ├── competitors.py
│   ├── topics.py
│   └── recommendations.py
└── utils/
    ├── clustering.py
    ├── scoring.py
    └── caching.py
```

### 3. Data Models (Pydantic)
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class KeywordMetrics(BaseModel):
    keyword: str
    search_volume: int
    competition: float  # 0-1 scale
    competition_index: str  # LOW, MEDIUM, HIGH
    top_page_bid_low: Optional[float]
    top_page_bid_high: Optional[float]
    trend: str  # RISING, STABLE, DECLINING
    seasonality: Optional[Dict[str, float]]
    
class CompetitorContent(BaseModel):
    url: str
    title: str
    meta_description: str
    h1: List[str]
    h2_structure: List[str]
    word_count: int
    internal_links: int
    external_links: int
    schema_types: List[str]
    optimization_score: float
    
class ContentGap(BaseModel):
    topic: str
    gap_type: str  # MISSING, UNDERSERVED, OUTDATED
    search_potential: int
    difficulty: float
    competitors_ranking: List[str]
    opportunity_score: float
    
class TopicRecommendation(BaseModel):
    title: str
    slug: str
    primary_keyword: KeywordMetrics
    secondary_keywords: List[KeywordMetrics]
    content_type: str
    target_word_count: int
    estimated_traffic: int
    difficulty_score: float
    priority_score: float
    competitor_benchmarks: List[CompetitorContent]
    content_outline: List[str]
    optimization_checklist: List[str]
```

## WORKFLOW:

### 1. Data Collection Phase
```python
async def collect_keyword_data():
    # 1. Get seed keywords from Google Ads
    # 2. Expand with Keyword Planner suggestions
    # 3. Fetch search volumes and competition
    # 4. Get trend data from Google Trends
    # 5. Cache results for efficiency
    
async def analyze_competitors():
    # 1. Identify top 10 competitors for each keyword
    # 2. Crawl with Screaming Frog API
    # 3. Extract content structure and optimization
    # 4. Identify successful patterns
    # 5. Store in vector database for similarity search
    
async def identify_gaps():
    # 1. Compare our content to competitors
    # 2. Find missing topics and keywords
    # 3. Identify underserved search intents
    # 4. Score opportunities by potential impact
```

### 2. Analysis Phase
```python
async def analyze_opportunities():
    # 1. Cluster keywords by topic and intent
    # 2. Calculate difficulty scores
    # 3. Estimate traffic potential
    # 4. Prioritize by business impact
    # 5. Generate content recommendations
```

### 3. Output Generation
```python
async def generate_recommendations():
    # Returns structured data:
    {
        "timestamp": "2024-01-15T10:00:00Z",
        "keywords_analyzed": 150,
        "gaps_identified": 45,
        "recommendations": [
            {
                "title": "PTSD Service Dogs: Complete Training Guide",
                "priority": 95,
                "estimated_monthly_traffic": 5000,
                "difficulty": "MEDIUM",
                "primary_keyword": {
                    "term": "PTSD service dog training",
                    "volume": 3200,
                    "competition": 0.45
                },
                "content_outline": [...],
                "optimization_tips": [...]
            }
        ]
    }
```

## CLI INTERFACE:

```bash
# Run full topic analysis
python -m topic_analysis analyze \
    --keywords "service dog,PTSD service dog" \
    --competitors "competitor1.com,competitor2.com" \
    --output-format json

# Quick opportunity scan
python -m topic_analysis quick-scan \
    --niche "service-dog" \
    --max-recommendations 10

# Competitor gap analysis
python -m topic_analysis gaps \
    --our-site "servicedogus.com" \
    --competitors "top-3-competitors.txt"

# Keyword expansion
python -m topic_analysis expand \
    --seed-keywords "anxiety service dog" \
    --max-keywords 50
```

## CONFIGURATION:

### .env.example
```bash
# Google Ads API Credentials (MCC Account)
GOOGLE_ADS_CLIENT_ID=your-client-id
GOOGLE_ADS_CLIENT_SECRET=your-client-secret
GOOGLE_ADS_REFRESH_TOKEN=your-refresh-token
GOOGLE_ADS_DEVELOPER_TOKEN=your-developer-token
GOOGLE_ADS_CUSTOMER_ID=your-mcc-customer-id

# Screaming Frog License
SCREAMING_FROG_LICENSE=your-license-key
SCREAMING_FROG_API_PORT=8089

# Reddit API (optional)
REDDIT_CLIENT_ID=your-client-id
REDDIT_CLIENT_SECRET=your-client-secret
REDDIT_USER_AGENT=TopicAnalysisBot/1.0

# AI Provider
ANTHROPIC_API_KEY=your-anthropic-key

# Cache Settings
CACHE_DIR=./data/cache
CACHE_TTL_HOURS=24

# Analysis Settings
MAX_COMPETITORS_PER_KEYWORD=10
MIN_SEARCH_VOLUME=100
MAX_KEYWORD_DIFFICULTY=0.7
```

## SETUP INSTRUCTIONS:

### 1. Google Ads API Setup
1. Go to https://ads.google.com/aw/apicenter
2. Create API credentials for your MCC account
3. Generate refresh token using Google's OAuth playground
4. Add credentials to .env file

### 2. Screaming Frog Setup
1. Install Screaming Frog SEO Spider
2. Enter license key in application
3. Enable API mode: Configuration > API Access > Enable
4. Set API port (default 8089)
5. Keep Screaming Frog running during analysis

### 3. Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run initial test
python -m topic_analysis test-connections
```

## TESTING:

### Unit Tests
```python
# tests/test_keyword_research.py
def test_keyword_planner_connection():
    """Test Google Ads API connection"""
    
def test_search_volume_extraction():
    """Test keyword metrics extraction"""

# tests/test_competitor_analysis.py  
def test_screaming_frog_api():
    """Test Screaming Frog API connection"""
    
def test_content_extraction():
    """Test competitor content parsing"""

# tests/test_gap_analysis.py
def test_gap_identification():
    """Test content gap detection algorithm"""
    
def test_opportunity_scoring():
    """Test opportunity prioritization"""
```

### Integration Tests
```python
# tests/test_full_workflow.py
async def test_complete_analysis():
    """Test end-to-end topic analysis workflow"""
    # 1. Collect keyword data
    # 2. Analyze competitors
    # 3. Identify gaps
    # 4. Generate recommendations
    # 5. Validate output format
```

## MONITORING & MAINTENANCE:

### API Usage Tracking
- Google Ads API: Track daily quota usage
- Screaming Frog: Monitor crawl limits
- Cache hit rates for efficiency

### Data Quality Checks
- Validate keyword volumes against manual checks
- Compare competitor data freshness
- Monitor recommendation relevance

### Performance Metrics
- Analysis completion time
- Cache efficiency
- API response times
- Error rates by source

## EDGE CASES & ERROR HANDLING:

1. **API Rate Limits**
   - Implement exponential backoff
   - Use caching aggressively
   - Queue requests when hitting limits

2. **Data Source Failures**
   - Fallback to cached data
   - Use alternative sources when available
   - Graceful degradation of features

3. **Invalid Keywords**
   - Filter profanity and irrelevant terms
   - Handle zero-volume keywords
   - Manage keyword length limits

4. **Competitor Issues**
   - Handle sites blocking crawlers
   - Manage JavaScript-heavy sites
   - Deal with rate limiting

## EXPECTED OUTPUTS:

### Topic Recommendation Example
```json
{
  "recommendation_id": "rec_20240115_001",
  "title": "How to Train a PTSD Service Dog: Professional Guide",
  "slug": "train-ptsd-service-dog-guide",
  "priority_score": 92.5,
  "metrics": {
    "estimated_monthly_traffic": 4500,
    "keyword_difficulty": 0.45,
    "content_competition": "MEDIUM",
    "monetization_potential": "HIGH"
  },
  "keywords": {
    "primary": "PTSD service dog training",
    "secondary": [
      "train service dog for PTSD",
      "PTSD service dog commands",
      "psychiatric service dog training"
    ]
  },
  "content_requirements": {
    "word_count": 2500,
    "headers": ["H1", "5 H2s", "10 H3s"],
    "images": 8,
    "videos": 2,
    "internal_links": 10,
    "external_links": 5
  },
  "competitor_insights": {
    "top_ranking_urls": [...],
    "common_topics_covered": [...],
    "optimization_patterns": [...]
  }
}
```

## FUTURE ENHANCEMENTS:

1. **Machine Learning Integration**
   - Predictive traffic modeling
   - Content success prediction
   - Automated outline generation

2. **Additional Data Sources**
   - YouTube keyword data
   - Amazon search trends
   - Pinterest trends for visual content

3. **Advanced Features**
   - Real-time SERP monitoring
   - Automated content brief generation
   - ROI prediction models

4. **Reporting Dashboard**
   - Web-based visualization
   - Scheduled reports
   - Slack/email notifications