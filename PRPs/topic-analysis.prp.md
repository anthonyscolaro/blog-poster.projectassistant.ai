name: "Topic Analysis Agent: Enterprise SEO Research & Opportunity Discovery System"
description: |

## Purpose
Build an intelligent Topic Analysis Agent that leverages Google Ads Keyword Planner (via MCC account) and Screaming Frog SEO Spider to identify high-value content opportunities through comprehensive keyword research, competitor analysis, and content gap identification.

## Core Principles
1. **Data-Driven Decisions**: Use real search volume and competition data from Google Ads
2. **Competitive Intelligence**: Analyze competitor content structure and optimization patterns
3. **Opportunity Scoring**: Prioritize topics by traffic potential and difficulty
4. **Automation First**: Minimize manual research through API integrations

---

## Goal
Create a production-ready Topic Analysis Agent that automatically discovers content opportunities by analyzing search data, competitor strategies, and market gaps to generate prioritized topic recommendations with detailed optimization guidance.

## Why
- **Eliminate Guesswork**: Replace assumptions with actual search data from Google Ads
- **Competitive Advantage**: Systematically identify gaps competitors haven't filled
- **ROI Focus**: Prioritize content creation based on traffic potential and difficulty
- **Time Efficiency**: Automate hours of manual keyword and competitor research
- **Data Integration**: Leverage existing Google Ads MCC and Screaming Frog licenses

## What
A Pydantic AI-powered agent system that:
- Integrates Google Ads API for precise keyword metrics
- Uses Screaming Frog API for competitor content analysis  
- Identifies content gaps through comparative analysis
- Generates prioritized topic recommendations with SEO guidance
- Provides content outlines based on successful competitor patterns

### Success Criteria
- [ ] Google Ads API integration with MCC account access
- [ ] Screaming Frog API integration for competitor crawling
- [ ] Keyword clustering and intent classification
- [ ] Content gap scoring algorithm
- [ ] Topic recommendation generation with metrics
- [ ] Caching system for API efficiency
- [ ] CLI interface for analysis workflows
- [ ] Comprehensive test coverage

## All Needed Context

### Documentation & References
```yaml
# Core Implementation Files
- file: docs/topic-analysis-implementation.md
  why: Complete implementation guide with architecture details
  
- file: agents/topic_analysis_agent.py
  why: Current agent implementation (to be updated)
  
- file: src/models/contracts.py
  why: Data models for topic analysis
  
- file: examples/test_full_workflow.py
  why: Integration testing patterns

# API Documentation
- url: https://developers.google.com/google-ads/api/docs/start
  why: Google Ads API setup and authentication
  
- url: https://www.screamingfrog.co.uk/seo-spider/api/
  why: Screaming Frog API documentation
  
- url: https://ai.pydantic.dev/
  why: Pydantic AI agent framework
```

### Current Architecture
```yaml
Data Sources:
  Google Ads:
    auth: OAuth2 with MCC account
    data:
      - Search volumes (exact)
      - Competition metrics
      - CPC ranges
      - Keyword suggestions
      - Trend data
      
  Screaming Frog:
    auth: License key
    data:
      - Competitor URLs
      - Title/meta analysis
      - Content structure
      - Internal linking
      - Schema markup
      
  Supplementary:
    - Google Trends (pytrends)
    - People Also Ask (SERP scraping)
    - Reddit discussions (PRAW)

Agent Structure:
  MainAgent:
    name: TopicAnalysisOrchestrator
    responsibilities:
      - Coordinate sub-agents
      - Aggregate insights
      - Generate recommendations
      
  SubAgents:
    - KeywordResearchAgent
    - CompetitorAnalysisAgent  
    - TrendAnalysisAgent
    - ContentGapAgent
```

### Key Implementation Details
```python
# Google Ads Integration
class GoogleAdsClient:
    def __init__(self, customer_id: str):
        self.client = GoogleAdsClient.load_from_env()
        self.customer_id = customer_id
    
    async def get_keyword_metrics(
        self,
        keywords: List[str],
        language: str = "en",
        location: str = "US"
    ) -> List[KeywordMetrics]:
        # Fetch search volumes, competition, CPC
        pass

# Screaming Frog Integration
class ScreamingFrogAPI:
    def __init__(self, license_key: str, port: int = 8089):
        self.base_url = f"http://localhost:{port}"
        self.license = license_key
    
    async def crawl_competitors(
        self,
        urls: List[str],
        depth: int = 2
    ) -> List[CompetitorContent]:
        # Crawl and analyze competitor content
        pass

# Topic Analysis Agent
class TopicAnalysisAgent:
    async def analyze(
        self,
        seed_keywords: List[str],
        competitors: List[str],
        our_content: List[str]
    ) -> TopicAnalysisReport:
        # 1. Expand keywords via Google Ads
        # 2. Get search metrics
        # 3. Analyze competitor content
        # 4. Identify gaps
        # 5. Score opportunities
        # 6. Generate recommendations
        pass
```

## Validation Scripts

### 1. API Connection Test
```python
# test_connections.py
import asyncio
from integrations.google_ads import GoogleAdsClient
from integrations.screaming_frog import ScreamingFrogAPI

async def test_apis():
    # Test Google Ads connection
    gads = GoogleAdsClient(customer_id=os.getenv("GOOGLE_ADS_CUSTOMER_ID"))
    keywords = await gads.get_keyword_metrics(["service dog"])
    assert len(keywords) > 0
    
    # Test Screaming Frog
    sf = ScreamingFrogAPI(license_key=os.getenv("SCREAMING_FROG_LICENSE"))
    status = await sf.check_status()
    assert status["connected"] == True
    
    print("✅ All API connections successful")

asyncio.run(test_apis())
```

### 2. Topic Analysis Test
```python
# test_analysis.py
from agents.topic_analysis import TopicAnalysisAgent

async def test_topic_analysis():
    agent = TopicAnalysisAgent()
    
    report = await agent.analyze(
        seed_keywords=["PTSD service dog", "anxiety service dog"],
        competitors=["competitor1.com", "competitor2.com"],
        our_content=["existing-article-1", "existing-article-2"]
    )
    
    assert report.keywords_analyzed > 10
    assert len(report.recommendations) > 0
    assert report.recommendations[0].priority_score > 0
    
    print(f"✅ Found {len(report.recommendations)} topic opportunities")
```

### 3. CLI Usage Test
```bash
#!/bin/bash
# test_cli.sh

# Test keyword expansion
python -m topic_analysis expand \
    --seed-keywords "service dog training" \
    --max-keywords 20

# Test competitor gap analysis
python -m topic_analysis gaps \
    --our-site "servicedogus.com" \
    --competitors "example.com,example2.com"

# Test full analysis
python -m topic_analysis analyze \
    --keywords "PTSD service dog" \
    --output recommendations.json

echo "✅ CLI tests completed"
```

## Example Usage

### Running Full Analysis
```python
from agents.topic_analysis import TopicAnalysisAgent
import asyncio

async def main():
    agent = TopicAnalysisAgent()
    
    # Analyze service dog niche
    report = await agent.analyze(
        seed_keywords=[
            "PTSD service dog",
            "autism service dog",
            "service dog training",
            "service dog laws"
        ],
        competitors=[
            "usserviceanimals.org",
            "servicedogcertifications.org",
            "nsarco.com"
        ]
    )
    
    # Display top recommendations
    for rec in report.recommendations[:5]:
        print(f"""
        Title: {rec.title}
        Priority: {rec.priority_score}/100
        Traffic Potential: {rec.estimated_traffic}/mo
        Difficulty: {rec.difficulty_score}
        Primary Keyword: {rec.primary_keyword.keyword}
        Search Volume: {rec.primary_keyword.search_volume}
        """)

asyncio.run(main())
```

### Getting Quick Opportunities
```python
# Quick scan for opportunities
quick_recs = await agent.quick_scan(
    niche="service-dog",
    max_recommendations=10,
    min_search_volume=500,
    max_difficulty=0.6
)

for rec in quick_recs:
    print(f"- {rec.title} (Priority: {rec.priority_score})")
```

## Production Deployment Checklist

- [ ] Google Ads API credentials configured
- [ ] MCC account ID verified
- [ ] Screaming Frog license activated
- [ ] Screaming Frog API enabled (port 8089)
- [ ] Redis cache configured
- [ ] Environment variables set
- [ ] API rate limits configured
- [ ] Monitoring dashboards setup
- [ ] Error alerting configured
- [ ] Backup cache strategy

## Edge Cases & Error Handling

1. **Google Ads API Limits**
   - 15,000 requests per day limit
   - Implement request batching
   - Cache results for 24 hours
   
2. **Screaming Frog Memory**
   - Large competitor sites may exceed memory
   - Implement crawl depth limits
   - Use URL sampling for huge sites
   
3. **Zero Search Volume Keywords**
   - Filter out zero-volume keywords
   - Use semantic variations
   - Check for seasonal patterns
   
4. **Competitor Blocking**
   - Fallback to cached data
   - Use alternative user agents
   - Implement proxy rotation if needed

## Maintenance & Monitoring

```yaml
Metrics:
  - Keywords analyzed per day
  - API calls per source
  - Cache hit rate
  - Average analysis time
  - Recommendation acceptance rate
  
Alerts:
  - API authentication failures
  - Rate limit approaching (80%)
  - Cache storage > 80%
  - Analysis time > 5 minutes
  
Logs:
  - All API requests/responses
  - Keyword expansion trails
  - Gap identification logic
  - Recommendation scoring
```

## Expected ROI

- **Time Savings**: 10+ hours of manual research per week
- **Content Performance**: 3x higher traffic for data-driven topics
- **Competitive Edge**: Identify opportunities before competitors
- **Cost Efficiency**: Maximize existing tool investments (Google Ads, Screaming Frog)
- **Predictable Results**: Data-backed content decisions vs. guesswork