"""
Competitor Monitoring Agent
Tracks competitor content, identifies trends, and suggests topics
"""
import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging

from pydantic import BaseModel, Field, HttpUrl
from scrapers import WebScraper, CompetitorMonitor, CompetitorContent, ScrapedContent

logger = logging.getLogger(__name__)


class TrendingTopic(BaseModel):
    """A trending topic identified from competitor analysis"""
    topic: str
    frequency: int
    sources: List[HttpUrl]
    keywords: List[str]
    first_seen: datetime
    last_seen: datetime
    trend_score: float  # 0-100, higher is more trending
    suggested_angle: Optional[str] = None


class ContentGap(BaseModel):
    """A content opportunity not covered by our site"""
    topic: str
    competitor_coverage: int  # Number of competitors covering this
    our_coverage: int  # Number of our articles on this
    opportunity_score: float  # 0-100, higher is better opportunity
    suggested_keywords: List[str]
    competitor_examples: List[HttpUrl]


class CompetitorInsights(BaseModel):
    """Aggregated insights from competitor monitoring"""
    scan_date: datetime
    competitors_analyzed: int
    total_content_pieces: int
    trending_topics: List[TrendingTopic]
    content_gaps: List[ContentGap]
    top_performing_content: List[Dict[str, Any]]
    recommended_topics: List[str]


class CompetitorMonitoringAgent:
    """
    Agent responsible for monitoring competitor content and identifying opportunities
    """
    
    def __init__(
        self,
        competitors: List[str] = None,
        cache_dir: str = "data/competitors",
        scan_frequency_hours: int = 24
    ):
        """
        Initialize the competitor monitoring agent
        
        Args:
            competitors: List of competitor domains to monitor
            cache_dir: Directory to cache scraped content
            scan_frequency_hours: How often to scan competitors
        """
        self.scraper = WebScraper()
        self.monitor = CompetitorMonitor(self.scraper)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.scan_frequency = timedelta(hours=scan_frequency_hours)
        self.last_scan = None
        
        # Default competitors for ServiceDogUS
        default_competitors = [
            "servicedogcentral.org",
            "assistancedogsinternational.org",
            "usserviceanimals.org",
            "nsarco.com",
            "iaadp.org",
            "akc.org/expert-advice/training/service-dog-training",
            "pawsitivityservicedogs.com",
            "4pawsforability.org"
        ]
        
        # Add competitors
        for domain in (competitors or default_competitors):
            self.monitor.add_competitor(domain)
        
        # Track our own content for gap analysis
        self.our_content_topics = set()
        self.our_content_keywords = set()
    
    async def scan_competitors(self, force: bool = False) -> List[CompetitorContent]:
        """
        Scan all configured competitors for new content
        
        Args:
            force: Force scan even if recently scanned
        
        Returns:
            List of competitor content
        """
        # Check if we should scan
        if not force and self.last_scan:
            time_since_scan = datetime.now() - self.last_scan
            if time_since_scan < self.scan_frequency:
                logger.info(f"Skipping scan, last scan was {time_since_scan.total_seconds()/3600:.1f} hours ago")
                return self._load_cached_content()
        
        logger.info("Starting competitor scan...")
        
        # Scan competitors
        content = await self.monitor.scan_competitors()
        
        # Cache the results
        self._cache_content(content)
        self.last_scan = datetime.now()
        
        logger.info(f"Scanned {len(content)} pieces of content from competitors")
        
        return content
    
    def analyze_trends(self, content: List[CompetitorContent]) -> List[TrendingTopic]:
        """
        Analyze competitor content to identify trending topics
        
        Args:
            content: List of competitor content
        
        Returns:
            List of trending topics
        """
        # Aggregate topics across all content
        topic_data = {}
        
        for item in content:
            for topic in item.topics:
                if topic not in topic_data:
                    topic_data[topic] = {
                        "frequency": 0,
                        "sources": [],
                        "keywords": set(),
                        "dates": []
                    }
                
                topic_data[topic]["frequency"] += 1
                topic_data[topic]["sources"].append(item.source_url)
                topic_data[topic]["keywords"].update(item.keywords)
                topic_data[topic]["dates"].append(item.scraped_content.scraped_at)
        
        # Convert to TrendingTopic objects
        trending_topics = []
        for topic, data in topic_data.items():
            # Calculate trend score based on frequency and recency
            dates = data["dates"]
            if dates:
                days_old = (datetime.now() - min(dates)).days
                recency_score = max(0, 100 - (days_old * 10))  # Lose 10 points per day old
            else:
                recency_score = 0
            
            frequency_score = min(100, data["frequency"] * 20)  # Cap at 100
            trend_score = (recency_score + frequency_score) / 2
            
            trending_topics.append(TrendingTopic(
                topic=topic,
                frequency=data["frequency"],
                sources=list(set(data["sources"]))[:5],  # Limit to 5 sources
                keywords=list(data["keywords"])[:10],  # Top 10 keywords
                first_seen=min(dates) if dates else datetime.now(),
                last_seen=max(dates) if dates else datetime.now(),
                trend_score=trend_score,
                suggested_angle=self._generate_angle_suggestion(topic)
            ))
        
        # Sort by trend score
        trending_topics.sort(key=lambda x: x.trend_score, reverse=True)
        
        return trending_topics[:10]  # Return top 10 trending topics
    
    def identify_content_gaps(
        self,
        competitor_content: List[CompetitorContent]
    ) -> List[ContentGap]:
        """
        Identify topics competitors cover that we don't
        
        Args:
            competitor_content: List of competitor content
        
        Returns:
            List of content gaps
        """
        # Aggregate competitor topics
        competitor_topics = {}
        
        for item in competitor_content:
            for topic in item.topics:
                if topic not in competitor_topics:
                    competitor_topics[topic] = {
                        "count": 0,
                        "sources": [],
                        "keywords": set()
                    }
                
                competitor_topics[topic]["count"] += 1
                competitor_topics[topic]["sources"].append(item.source_url)
                competitor_topics[topic]["keywords"].update(item.keywords)
        
        # Identify gaps (topics we don't cover well)
        content_gaps = []
        
        for topic, data in competitor_topics.items():
            # Check our coverage (simplified - would query our database in production)
            our_coverage = 1 if topic in self.our_content_topics else 0
            
            # Calculate opportunity score
            competitor_coverage = data["count"]
            coverage_gap = competitor_coverage - our_coverage
            
            if coverage_gap > 0:
                # Higher score for topics many competitors cover but we don't
                opportunity_score = min(100, coverage_gap * 25)
                
                content_gaps.append(ContentGap(
                    topic=topic,
                    competitor_coverage=competitor_coverage,
                    our_coverage=our_coverage,
                    opportunity_score=opportunity_score,
                    suggested_keywords=list(data["keywords"])[:10],
                    competitor_examples=list(set(data["sources"]))[:3]
                ))
        
        # Sort by opportunity score
        content_gaps.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        return content_gaps[:10]  # Return top 10 gaps
    
    def _generate_angle_suggestion(self, topic: str) -> str:
        """
        Generate a unique angle suggestion for a topic
        
        Args:
            topic: The topic to generate an angle for
        
        Returns:
            Suggested angle for the topic
        """
        # This would use LLM in production, but for now use templates
        angle_templates = {
            "ADA compliance": "Focus on recent 2024 updates and common misconceptions",
            "Service dogs": "Personal stories from handlers with practical tips",
            "ESA": "Clear distinction from service dogs with legal requirements",
            "Training": "Step-by-step guide with video demonstrations",
            "Laws": "State-by-state comparison with interactive map",
            "Rights": "Real-world scenarios and how to handle them",
            "Public access": "Business owner's guide to service dog laws",
            "Housing": "Template letters and documentation for landlords",
            "Healthcare": "Working with medical professionals for documentation",
            "Veterans": "VA benefits and service dog acquisition process"
        }
        
        return angle_templates.get(topic, f"Comprehensive guide to {topic} for service dog handlers")
    
    async def generate_insights(self) -> CompetitorInsights:
        """
        Generate comprehensive insights from competitor monitoring
        
        Returns:
            CompetitorInsights with trends, gaps, and recommendations
        """
        # Scan competitors
        content = await self.scan_competitors()
        
        # Analyze trends
        trending_topics = self.analyze_trends(content)
        
        # Identify content gaps
        content_gaps = self.identify_content_gaps(content)
        
        # Identify top performing content (simplified)
        top_content = self._identify_top_performing(content)
        
        # Generate topic recommendations
        recommendations = self._generate_recommendations(trending_topics, content_gaps)
        
        return CompetitorInsights(
            scan_date=datetime.now(),
            competitors_analyzed=len(self.monitor.competitors),
            total_content_pieces=len(content),
            trending_topics=trending_topics,
            content_gaps=content_gaps,
            top_performing_content=top_content,
            recommended_topics=recommendations
        )
    
    def _identify_top_performing(
        self,
        content: List[CompetitorContent],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Identify top performing competitor content
        
        Args:
            content: List of competitor content
            limit: Number of top items to return
        
        Returns:
            List of top performing content metadata
        """
        # In production, this would look at engagement metrics
        # For now, we'll use word count and topic relevance as proxies
        
        top_content = []
        
        for item in content[:limit]:
            top_content.append({
                "url": str(item.source_url),
                "title": item.title,
                "domain": item.domain,
                "topics": item.topics,
                "word_count": item.scraped_content.word_count,
                "content_type": item.content_type
            })
        
        return top_content
    
    def _generate_recommendations(
        self,
        trends: List[TrendingTopic],
        gaps: List[ContentGap]
    ) -> List[str]:
        """
        Generate topic recommendations based on trends and gaps
        
        Args:
            trends: List of trending topics
            gaps: List of content gaps
        
        Returns:
            List of recommended topics to write about
        """
        recommendations = []
        
        # High-scoring trends
        for trend in trends[:3]:
            if trend.trend_score > 70:
                recommendations.append(
                    f"{trend.topic}: {trend.suggested_angle}"
                )
        
        # High-opportunity gaps
        for gap in gaps[:3]:
            if gap.opportunity_score > 60:
                recommendations.append(
                    f"{gap.topic}: Fill gap with focus on {', '.join(gap.suggested_keywords[:3])}"
                )
        
        # Combine trending + gap (sweet spot)
        trending_topics = {t.topic for t in trends}
        gap_topics = {g.topic for g in gaps}
        sweet_spots = trending_topics.intersection(gap_topics)
        
        for topic in list(sweet_spots)[:2]:
            recommendations.append(
                f"{topic}: High opportunity - trending with low competition"
            )
        
        return list(set(recommendations))[:5]  # Return top 5 unique recommendations
    
    def _cache_content(self, content: List[CompetitorContent]):
        """Cache scraped content to disk"""
        cache_file = self.cache_dir / f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert to serializable format
        data = []
        for item in content:
            data.append({
                "source_url": str(item.source_url),
                "domain": item.domain,
                "title": item.title,
                "topics": item.topics,
                "keywords": item.keywords,
                "content_type": item.content_type,
                "scraped_at": item.scraped_content.scraped_at.isoformat(),
                "word_count": item.scraped_content.word_count
            })
        
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Clean old cache files (keep last 7 days)
        self._clean_old_cache()
    
    def _clean_old_cache(self, days_to_keep: int = 7):
        """Remove cache files older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for cache_file in self.cache_dir.glob("scan_*.json"):
            # Parse date from filename
            try:
                date_str = cache_file.stem.replace("scan_", "")
                file_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
                
                if file_date < cutoff_date:
                    cache_file.unlink()
                    logger.info(f"Removed old cache file: {cache_file}")
            except Exception as e:
                logger.warning(f"Could not parse cache file date: {cache_file}, error: {e}")
    
    def _load_cached_content(self) -> List[CompetitorContent]:
        """Load the most recent cached content"""
        cache_files = sorted(self.cache_dir.glob("scan_*.json"))
        
        if not cache_files:
            return []
        
        latest_cache = cache_files[-1]
        
        with open(latest_cache, 'r') as f:
            data = json.load(f)
        
        # Convert back to CompetitorContent objects
        content = []
        for item in data:
            # Create minimal ScrapedContent for cached data
            scraped = ScrapedContent(
                url=item["source_url"],
                title=item["title"],
                content="",  # Content not cached for space
                scraper_used="cached",
                scraped_at=datetime.fromisoformat(item["scraped_at"]),
                word_count=item["word_count"]
            )
            
            content.append(CompetitorContent(
                source_url=item["source_url"],
                domain=item["domain"],
                title=item["title"],
                topics=item["topics"],
                keywords=item["keywords"],
                content_type=item["content_type"],
                scraped_content=scraped
            ))
        
        return content
    
    def set_our_content(self, topics: List[str], keywords: List[str]):
        """
        Set our own content topics and keywords for gap analysis
        
        Args:
            topics: List of topics we cover
            keywords: List of keywords we target
        """
        self.our_content_topics = set(topics)
        self.our_content_keywords = set(keywords)
    
    async def close(self):
        """Clean up resources"""
        await self.scraper.close()


# Example usage
async def main():
    """Example of using the competitor monitoring agent"""
    
    # Initialize agent
    agent = CompetitorMonitoringAgent(
        competitors=[
            "servicedogcentral.org",
            "assistancedogsinternational.org"
        ]
    )
    
    # Set our content (would come from database in production)
    agent.set_our_content(
        topics=["Service dogs", "ADA compliance", "Training"],
        keywords=["service dog", "ada", "training", "certification"]
    )
    
    # Generate insights
    insights = await agent.generate_insights()
    
    print(f"Analyzed {insights.competitors_analyzed} competitors")
    print(f"Found {insights.total_content_pieces} content pieces")
    
    print("\n📈 Trending Topics:")
    for topic in insights.trending_topics[:5]:
        print(f"  - {topic.topic} (score: {topic.trend_score:.1f})")
        print(f"    Angle: {topic.suggested_angle}")
    
    print("\n🎯 Content Gaps:")
    for gap in insights.content_gaps[:5]:
        print(f"  - {gap.topic} (opportunity: {gap.opportunity_score:.1f})")
        print(f"    Competitors: {gap.competitor_coverage}, Us: {gap.our_coverage}")
    
    print("\n💡 Recommended Topics:")
    for rec in insights.recommended_topics:
        print(f"  - {rec}")
    
    await agent.close()


if __name__ == "__main__":
    asyncio.run(main())