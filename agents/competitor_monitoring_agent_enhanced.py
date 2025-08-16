"""
Enhanced Competitor Monitoring Agent with Jina AI Integration
Performs deep competitive analysis, content gap identification, and strategic recommendations
"""
import os
import re
import json
import asyncio
import aiohttp
import hashlib
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, urljoin
import logging
from collections import Counter, defaultdict

from pydantic import BaseModel, Field, HttpUrl
from bs4 import BeautifulSoup
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class CompetitorProfile(BaseModel):
    """Detailed profile of a competitor website"""
    domain: str
    name: str
    description: Optional[str] = None
    focus_areas: List[str] = Field(default_factory=list)
    content_frequency: Optional[str] = None  # "daily", "weekly", "monthly"
    estimated_traffic: Optional[int] = None
    social_presence: Dict[str, str] = Field(default_factory=dict)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    last_analyzed: datetime = Field(default_factory=datetime.now)


class ContentMetrics(BaseModel):
    """Metrics for a piece of content"""
    url: HttpUrl
    title: str
    word_count: int
    reading_time_minutes: int
    keyword_density: Dict[str, float]
    internal_links: int
    external_links: int
    images_count: int
    headings_structure: Dict[str, int]  # h1, h2, h3 counts
    meta_description: Optional[str] = None
    published_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    estimated_traffic: Optional[int] = None


class TrendingTopic(BaseModel):
    """Enhanced trending topic with predictive analytics"""
    topic: str
    frequency: int
    sources: List[HttpUrl]
    keywords: List[str]
    first_seen: datetime
    last_seen: datetime
    trend_score: float  # 0-100
    momentum: str  # "rising", "stable", "declining"
    predicted_peak: Optional[datetime] = None
    suggested_angles: List[str]
    competitor_saturation: float  # 0-1, how saturated the topic is


class ContentGap(BaseModel):
    """Enhanced content gap with strategic insights"""
    topic: str
    gap_type: str  # "missing", "underserved", "outdated", "quality"
    competitor_coverage: int
    our_coverage: int
    opportunity_score: float  # 0-100
    difficulty_score: float  # 0-100, how hard to compete
    suggested_keywords: List[str]
    competitor_examples: List[HttpUrl]
    strategic_approach: str
    estimated_traffic_potential: Optional[int] = None


class CompetitivePosition(BaseModel):
    """Our competitive position analysis"""
    market_share_estimate: float  # 0-1
    content_quality_score: float  # 0-100
    topic_coverage_score: float  # 0-100
    content_freshness_score: float  # 0-100
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]  # SWOT analysis


class CompetitorInsights(BaseModel):
    """Comprehensive competitive intelligence report"""
    scan_date: datetime
    competitors_analyzed: int
    total_content_pieces: int
    new_content_since_last_scan: int
    trending_topics: List[TrendingTopic]
    content_gaps: List[ContentGap]
    top_performing_content: List[ContentMetrics]
    competitor_profiles: List[CompetitorProfile]
    our_position: CompetitivePosition
    strategic_recommendations: List[str]
    action_items: List[Dict[str, Any]]


class EnhancedCompetitorMonitoringAgent:
    """
    Advanced competitor monitoring with Jina AI integration and ML-based analysis
    """
    
    # Default competitors for service dog niche
    DEFAULT_COMPETITORS = {
        "servicedogcentral.org": "Service Dog Central",
        "assistancedogsinternational.org": "ADI - Assistance Dogs International",
        "usserviceanimals.org": "US Service Animals",
        "nsarco.com": "National Service Animal Registry",
        "iaadp.org": "International Association of Assistance Dog Partners",
        "akc.org": "American Kennel Club",
        "pawsitivityservicedogs.com": "Pawsitivity Service Dogs",
        "4pawsforability.org": "4 Paws for Ability",
        "caninecompanions.org": "Canine Companions",
        "guidingeyes.org": "Guiding Eyes for the Blind"
    }
    
    def __init__(
        self,
        competitors: Optional[Dict[str, str]] = None,
        jina_api_key: Optional[str] = None,
        cache_dir: str = "data/competitors",
        scan_frequency_hours: int = 24,
        enable_ml_analysis: bool = True
    ):
        """
        Initialize enhanced competitor monitoring agent
        
        Args:
            competitors: Dict of domain -> name for competitors
            jina_api_key: API key for Jina AI web scraping
            cache_dir: Directory to cache scraped content
            scan_frequency_hours: How often to scan competitors
            enable_ml_analysis: Whether to use ML for content analysis
        """
        self.competitors = competitors or self.DEFAULT_COMPETITORS
        self.jina_api_key = jina_api_key or os.getenv("JINA_API_KEY")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.scan_frequency = timedelta(hours=scan_frequency_hours)
        self.last_scan = None
        self.session = None
        
        self.enable_ml = enable_ml_analysis
        if self.enable_ml:
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.content_vectors = None
        
        # Track our own content
        self.our_content = []
        self.our_topics = set()
        self.our_keywords = set()
        
        # Competitor profiles cache
        self.competitor_profiles = {}
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def discover_competitors(
        self,
        seed_keywords: List[str],
        max_competitors: int = 20
    ) -> Dict[str, str]:
        """
        Discover new competitors through search
        
        Args:
            seed_keywords: Keywords to search for competitors
            max_competitors: Maximum number of competitors to discover
        
        Returns:
            Dict of newly discovered competitors {domain: name}
        """
        discovered = {}
        
        for keyword in seed_keywords:
            try:
                # Use Jina to search and extract domains
                search_url = f"https://s.jina.ai/{keyword}"
                headers = {"Authorization": f"Bearer {self.jina_api_key}"}
                
                if not self.session:
                    self.session = aiohttp.ClientSession()
                
                async with self.session.get(search_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract domains from search results
                        for result in data.get("results", [])[:5]:
                            domain = urlparse(result.get("url", "")).netloc
                            if domain and domain not in self.competitors:
                                discovered[domain] = result.get("title", domain)
                                
                                if len(discovered) >= max_competitors:
                                    break
            
            except Exception as e:
                logger.error(f"Failed to discover competitors for '{keyword}': {e}")
        
        logger.info(f"Discovered {len(discovered)} new competitors")
        return discovered
    
    async def analyze_competitor(self, domain: str) -> CompetitorProfile:
        """
        Deep analysis of a single competitor
        
        Args:
            domain: Competitor domain to analyze
        
        Returns:
            CompetitorProfile with detailed analysis
        """
        # Check cache first
        if domain in self.competitor_profiles:
            profile = self.competitor_profiles[domain]
            if datetime.now() - profile.last_analyzed < timedelta(days=7):
                return profile
        
        profile = CompetitorProfile(
            domain=domain,
            name=self.competitors.get(domain, domain)
        )
        
        try:
            # Scrape homepage for overview
            homepage_url = f"https://r.jina.ai/https://{domain}"
            headers = {"Authorization": f"Bearer {self.jina_api_key}"}
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(homepage_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Extract key information
                    profile.description = self._extract_description(content)
                    profile.focus_areas = self._identify_focus_areas(content)
                    
            # Analyze sitemap for content structure
            sitemap_data = await self._analyze_sitemap(domain)
            profile.content_frequency = sitemap_data.get("frequency", "unknown")
            
            # Identify strengths and weaknesses
            profile.strengths, profile.weaknesses = await self._analyze_strengths_weaknesses(
                domain, content
            )
            
        except Exception as e:
            logger.error(f"Failed to analyze competitor {domain}: {e}")
        
        # Cache the profile
        self.competitor_profiles[domain] = profile
        
        return profile
    
    async def scan_competitor_content(
        self,
        domain: str,
        limit: int = 50,
        since_date: Optional[datetime] = None
    ) -> List[ContentMetrics]:
        """
        Scan content from a specific competitor
        
        Args:
            domain: Competitor domain
            limit: Maximum number of articles to scan
            since_date: Only scan content published after this date
        
        Returns:
            List of ContentMetrics for scanned content
        """
        content_list = []
        
        try:
            # Get sitemap or recent posts page
            scan_url = f"https://r.jina.ai/https://{domain}/blog"
            headers = {
                "Authorization": f"Bearer {self.jina_api_key}",
                "X-Return-Format": "json"
            }
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(scan_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract article URLs
                    article_urls = self._extract_article_urls(data, domain)
                    
                    # Scan each article
                    for url in article_urls[:limit]:
                        metrics = await self._analyze_content(url)
                        if metrics:
                            if not since_date or (metrics.published_date and metrics.published_date > since_date):
                                content_list.append(metrics)
        
        except Exception as e:
            logger.error(f"Failed to scan content from {domain}: {e}")
        
        return content_list
    
    async def _analyze_content(self, url: str) -> Optional[ContentMetrics]:
        """Analyze a single piece of content"""
        try:
            scrape_url = f"https://r.jina.ai/{url}"
            headers = {"Authorization": f"Bearer {self.jina_api_key}"}
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(scrape_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Parse content
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract metrics
                    text = soup.get_text()
                    words = text.split()
                    word_count = len(words)
                    
                    # Extract title
                    title = ""
                    h1_tag = soup.find('h1')
                    if h1_tag:
                        title = h1_tag.get_text().strip()
                    
                    # Count headings
                    headings = {
                        'h1': len(soup.find_all('h1')),
                        'h2': len(soup.find_all('h2')),
                        'h3': len(soup.find_all('h3'))
                    }
                    
                    # Count links
                    all_links = soup.find_all('a', href=True)
                    internal_links = 0
                    external_links = 0
                    
                    for link in all_links:
                        href = link['href']
                        if href.startswith('http'):
                            if urlparse(url).netloc in href:
                                internal_links += 1
                            else:
                                external_links += 1
                        else:
                            internal_links += 1
                    
                    # Count images
                    images = len(soup.find_all('img'))
                    
                    # Calculate keyword density
                    keyword_density = self._calculate_keyword_density(text)
                    
                    # Extract meta description
                    meta_desc = None
                    meta_tag = soup.find('meta', attrs={'name': 'description'})
                    if meta_tag:
                        meta_desc = meta_tag.get('content', '')
                    
                    return ContentMetrics(
                        url=url,
                        title=title,
                        word_count=word_count,
                        reading_time_minutes=max(1, word_count // 200),
                        keyword_density=keyword_density,
                        internal_links=internal_links,
                        external_links=external_links,
                        images_count=images,
                        headings_structure=headings,
                        meta_description=meta_desc
                    )
        
        except Exception as e:
            logger.error(f"Failed to analyze content {url}: {e}")
        
        return None
    
    def _calculate_keyword_density(
        self,
        text: str,
        top_k: int = 10
    ) -> Dict[str, float]:
        """Calculate keyword density for top keywords"""
        words = re.findall(r'\b[a-z]+\b', text.lower())
        word_count = len(words)
        
        if word_count == 0:
            return {}
        
        # Count word frequencies
        word_freq = Counter(words)
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'was', 'are', 'were', 'been', 'be', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        for stop_word in stop_words:
            word_freq.pop(stop_word, None)
        
        # Calculate density for top keywords
        keyword_density = {}
        for word, count in word_freq.most_common(top_k):
            keyword_density[word] = (count / word_count) * 100
        
        return keyword_density
    
    async def identify_trending_topics(
        self,
        content_list: List[ContentMetrics],
        time_window_days: int = 30
    ) -> List[TrendingTopic]:
        """
        Identify trending topics using advanced analytics
        
        Args:
            content_list: List of content metrics
            time_window_days: Time window for trend analysis
        
        Returns:
            List of trending topics with predictions
        """
        # Extract topics from content
        topic_data = defaultdict(lambda: {
            'frequency': 0,
            'sources': [],
            'keywords': Counter(),
            'dates': [],
            'momentum_data': []
        })
        
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        
        for content in content_list:
            # Extract topics from title and keywords
            topics = self._extract_topics(content.title, content.keyword_density)
            
            for topic in topics:
                topic_data[topic]['frequency'] += 1
                topic_data[topic]['sources'].append(content.url)
                topic_data[topic]['keywords'].update(content.keyword_density.keys())
                
                if content.published_date:
                    topic_data[topic]['dates'].append(content.published_date)
                    # Track momentum (frequency over time)
                    days_ago = (datetime.now() - content.published_date).days
                    topic_data[topic]['momentum_data'].append(days_ago)
        
        # Analyze trends
        trending_topics = []
        
        for topic, data in topic_data.items():
            if not data['dates']:
                continue
            
            # Calculate trend score
            frequency_score = min(100, data['frequency'] * 10)
            
            # Calculate recency score
            if data['dates']:
                most_recent = max(data['dates'])
                days_since = (datetime.now() - most_recent).days
                recency_score = max(0, 100 - (days_since * 5))
            else:
                recency_score = 0
            
            # Calculate momentum
            momentum = self._calculate_momentum(data['momentum_data'])
            
            # Calculate saturation
            saturation = min(1.0, data['frequency'] / len(self.competitors))
            
            # Generate multiple angles
            angles = self._generate_content_angles(topic, data['keywords'].most_common(5))
            
            # Overall trend score
            trend_score = (frequency_score * 0.4 + recency_score * 0.4 + 
                          (100 if momentum == "rising" else 50 if momentum == "stable" else 20) * 0.2)
            
            trending_topics.append(TrendingTopic(
                topic=topic,
                frequency=data['frequency'],
                sources=list(set(data['sources']))[:5],
                keywords=[k for k, _ in data['keywords'].most_common(10)],
                first_seen=min(data['dates']) if data['dates'] else datetime.now(),
                last_seen=max(data['dates']) if data['dates'] else datetime.now(),
                trend_score=trend_score,
                momentum=momentum,
                suggested_angles=angles,
                competitor_saturation=saturation
            ))
        
        # Sort by trend score
        trending_topics.sort(key=lambda x: x.trend_score, reverse=True)
        
        return trending_topics[:20]
    
    def _calculate_momentum(self, momentum_data: List[int]) -> str:
        """Calculate trend momentum from time series data"""
        if len(momentum_data) < 3:
            return "stable"
        
        # Simple linear regression to determine trend
        x = np.array(range(len(momentum_data)))
        y = np.array(sorted(momentum_data))
        
        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]
            
            if slope > 0.5:
                return "rising"
            elif slope < -0.5:
                return "declining"
        
        return "stable"
    
    async def identify_content_gaps(
        self,
        competitor_content: List[ContentMetrics],
        our_content: List[Dict[str, Any]]
    ) -> List[ContentGap]:
        """
        Identify content gaps using ML-based analysis
        
        Args:
            competitor_content: Competitor content metrics
            our_content: Our content data
        
        Returns:
            List of content gaps with strategic insights
        """
        gaps = []
        
        # Build topic maps
        competitor_topics = self._build_topic_map(competitor_content)
        our_topics = self._build_topic_map(our_content)
        
        # Identify different types of gaps
        for topic, comp_data in competitor_topics.items():
            our_coverage = our_topics.get(topic, {'count': 0})['count']
            comp_coverage = comp_data['count']
            
            if our_coverage == 0:
                gap_type = "missing"
                difficulty = 60  # Moderate difficulty for new topics
            elif our_coverage < comp_coverage / 2:
                gap_type = "underserved"
                difficulty = 40  # Easier to expand existing content
            elif self._content_is_outdated(topic, our_topics):
                gap_type = "outdated"
                difficulty = 30  # Easy to update
            elif self._content_quality_gap(topic, comp_data, our_topics.get(topic, {})):
                gap_type = "quality"
                difficulty = 50  # Moderate effort to improve quality
            else:
                continue  # No significant gap
            
            # Calculate opportunity score
            search_volume_estimate = comp_coverage * 100  # Simple estimate
            competition_factor = 1 - (comp_coverage / max(10, comp_coverage))
            opportunity_score = (search_volume_estimate * competition_factor) / 10
            opportunity_score = min(100, opportunity_score)
            
            # Determine strategic approach
            strategy = self._determine_content_strategy(gap_type, difficulty, opportunity_score)
            
            gaps.append(ContentGap(
                topic=topic,
                gap_type=gap_type,
                competitor_coverage=comp_coverage,
                our_coverage=our_coverage,
                opportunity_score=opportunity_score,
                difficulty_score=difficulty,
                suggested_keywords=comp_data['keywords'][:10],
                competitor_examples=comp_data['urls'][:3],
                strategic_approach=strategy,
                estimated_traffic_potential=int(search_volume_estimate * 0.1)
            ))
        
        # Sort by opportunity score
        gaps.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        return gaps[:20]
    
    def _build_topic_map(self, content_list: List[Any]) -> Dict[str, Dict]:
        """Build a map of topics from content list"""
        topic_map = defaultdict(lambda: {
            'count': 0,
            'keywords': Counter(),
            'urls': [],
            'last_updated': None
        })
        
        for content in content_list:
            if isinstance(content, ContentMetrics):
                topics = self._extract_topics(content.title, content.keyword_density)
                for topic in topics:
                    topic_map[topic]['count'] += 1
                    topic_map[topic]['keywords'].update(content.keyword_density.keys())
                    topic_map[topic]['urls'].append(content.url)
                    if content.last_updated:
                        if not topic_map[topic]['last_updated'] or content.last_updated > topic_map[topic]['last_updated']:
                            topic_map[topic]['last_updated'] = content.last_updated
            else:
                # Handle our content format
                title = content.get('title', '')
                topics = self._extract_topics(title, {})
                for topic in topics:
                    topic_map[topic]['count'] += 1
        
        # Convert Counters to lists
        for topic_data in topic_map.values():
            topic_data['keywords'] = [k for k, _ in topic_data['keywords'].most_common(10)]
        
        return dict(topic_map)
    
    def _extract_topics(
        self,
        title: str,
        keywords: Dict[str, float]
    ) -> List[str]:
        """Extract topics from title and keywords"""
        topics = []
        
        # Topic patterns for service dog niche
        topic_patterns = {
            'ADA Compliance': r'\bADA\b|Americans with Disabilities|compliance',
            'Service Dog Training': r'training|train\w*\s+\w*dog',
            'Service Dog Laws': r'law|legal|rights|regulation',
            'ESA vs Service Dogs': r'ESA|emotional support',
            'Service Dog Breeds': r'breed|golden retriever|labrador|poodle',
            'Public Access': r'public|access|restaurant|store|business',
            'Handler Rights': r'handler|owner|disability',
            'Certification': r'certifi|registration|document',
            'Veterans': r'veteran|VA\b|military',
            'Housing': r'housing|apartment|landlord|rent',
            'Travel': r'travel|flying|airline|TSA',
            'Healthcare': r'doctor|medical|healthcare|hospital',
            'Tasks and Work': r'task|work|job|assist',
            'Puppy Training': r'puppy|young dog|early training',
            'Gear and Equipment': r'vest|harness|leash|equipment'
        }
        
        title_lower = title.lower()
        
        for topic, pattern in topic_patterns.items():
            if re.search(pattern, title_lower, re.IGNORECASE):
                topics.append(topic)
        
        # Also check high-value keywords
        for keyword, density in keywords.items():
            if density > 2.0:  # Significant keyword
                for topic, pattern in topic_patterns.items():
                    if re.search(pattern, keyword, re.IGNORECASE):
                        if topic not in topics:
                            topics.append(topic)
        
        return topics
    
    def _content_is_outdated(self, topic: str, our_topics: Dict) -> bool:
        """Check if our content on a topic is outdated"""
        topic_data = our_topics.get(topic, {})
        last_updated = topic_data.get('last_updated')
        
        if not last_updated:
            return False
        
        # Content older than 6 months is considered outdated
        return (datetime.now() - last_updated).days > 180
    
    def _content_quality_gap(
        self,
        topic: str,
        comp_data: Dict,
        our_data: Dict
    ) -> bool:
        """Determine if there's a quality gap in our content"""
        # Simple heuristic: if competitors have 3x more keywords, there's a quality gap
        comp_keywords = len(comp_data.get('keywords', []))
        our_keywords = len(our_data.get('keywords', []))
        
        return comp_keywords > our_keywords * 3
    
    def _determine_content_strategy(
        self,
        gap_type: str,
        difficulty: float,
        opportunity: float
    ) -> str:
        """Determine the strategic approach for a content gap"""
        strategies = {
            "missing": {
                "high_opp": "Create comprehensive pillar content to establish authority",
                "med_opp": "Develop focused article targeting specific user intent",
                "low_opp": "Consider if topic aligns with content strategy"
            },
            "underserved": {
                "high_opp": "Expand coverage with in-depth guides and case studies",
                "med_opp": "Add supporting content and internal linking",
                "low_opp": "Update existing content with fresh perspectives"
            },
            "outdated": {
                "high_opp": "Complete content refresh with 2024 updates",
                "med_opp": "Update statistics and add recent developments",
                "low_opp": "Quick refresh of key facts and dates"
            },
            "quality": {
                "high_opp": "Rewrite with expert insights and original research",
                "med_opp": "Enhance with visuals, examples, and better structure",
                "low_opp": "Improve readability and add missing elements"
            }
        }
        
        opp_level = "high_opp" if opportunity > 70 else "med_opp" if opportunity > 40 else "low_opp"
        
        return strategies.get(gap_type, {}).get(opp_level, "Analyze further before investing resources")
    
    async def analyze_competitive_position(
        self,
        competitor_content: List[ContentMetrics],
        our_content: List[Dict[str, Any]]
    ) -> CompetitivePosition:
        """
        Analyze our competitive position with SWOT analysis
        
        Args:
            competitor_content: Competitor content metrics
            our_content: Our content data
        
        Returns:
            CompetitivePosition with SWOT analysis
        """
        # Calculate various scores
        our_word_count = sum(c.get('word_count', 0) for c in our_content)
        comp_word_count = sum(c.word_count for c in competitor_content)
        
        # Market share estimate (content volume based)
        total_content = len(our_content) + len(competitor_content)
        market_share = len(our_content) / max(1, total_content)
        
        # Content quality score (based on average metrics)
        our_avg_words = our_word_count / max(1, len(our_content))
        comp_avg_words = comp_word_count / max(1, len(competitor_content))
        quality_score = min(100, (our_avg_words / max(1, comp_avg_words)) * 50)
        
        # Topic coverage score
        our_topics = set(self._build_topic_map(our_content).keys())
        comp_topics = set(self._build_topic_map(competitor_content).keys())
        coverage_score = len(our_topics) / max(1, len(comp_topics)) * 100
        
        # Freshness score (placeholder - would check dates in production)
        freshness_score = 70  # Assumed average
        
        # SWOT Analysis
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []
        
        if quality_score > 70:
            strengths.append("High-quality, comprehensive content")
        else:
            weaknesses.append("Content quality below competitor average")
        
        if coverage_score > 80:
            strengths.append("Broad topic coverage")
        else:
            weaknesses.append(f"Limited topic coverage ({len(our_topics)} topics vs {len(comp_topics)} competitor topics)")
        
        # Opportunities
        uncovered_topics = comp_topics - our_topics
        if uncovered_topics:
            opportunities.append(f"{len(uncovered_topics)} uncovered high-value topics")
        
        if market_share < 0.2:
            opportunities.append("Significant room for growth in market share")
        
        # Threats
        if len(competitor_content) > len(our_content) * 2:
            threats.append("Competitors producing content at higher volume")
        
        if freshness_score < 60:
            threats.append("Content freshness falling behind competitors")
        
        return CompetitivePosition(
            market_share_estimate=market_share,
            content_quality_score=quality_score,
            topic_coverage_score=coverage_score,
            content_freshness_score=freshness_score,
            strengths=strengths or ["Established presence in niche"],
            weaknesses=weaknesses or ["Room for improvement identified"],
            opportunities=opportunities or ["Market growth potential"],
            threats=threats or ["Increasing competition"]
        )
    
    def _generate_content_angles(
        self,
        topic: str,
        keywords: List[Tuple[str, int]]
    ) -> List[str]:
        """Generate unique content angles for a topic"""
        angles = []
        
        # Base angles by topic type
        angle_templates = {
            'ADA Compliance': [
                "2024 ADA Updates: What Service Dog Handlers Need to Know",
                "Common ADA Violations and How to Address Them",
                "State vs Federal Laws: A Comprehensive Comparison"
            ],
            'Service Dog Training': [
                "Step-by-Step Training Guide with Video Tutorials",
                "Professional vs Owner Training: Pros and Cons",
                "Task Training for Specific Disabilities"
            ],
            'ESA vs Service Dogs': [
                "Legal Differences Explained with Real Examples",
                "Converting ESA to Service Dog: Is It Possible?",
                "Housing Rights: ESA vs Service Dog Comparison"
            ],
            'Public Access': [
                "Business Owner's Complete Guide to Service Dogs",
                "Handling Access Challenges: Scripts and Strategies",
                "International Travel with Service Dogs"
            ]
        }
        
        # Get base angles for topic
        base_angles = angle_templates.get(topic, [
            f"Complete Guide to {topic}",
            f"{topic}: Common Myths Debunked",
            f"{topic}: Expert Tips and Best Practices"
        ])
        
        # Add keyword-specific angles
        if keywords:
            top_keyword = keywords[0][0] if keywords else topic.lower()
            base_angles.append(f"How {top_keyword} Impacts {topic}")
        
        return base_angles[:3]
    
    def _extract_description(self, content: str) -> str:
        """Extract description from scraped content"""
        # Simple extraction - take first paragraph
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 50 and not line.startswith('<'):
                return line[:200] + "..."
        return "No description available"
    
    def _identify_focus_areas(self, content: str) -> List[str]:
        """Identify main focus areas from content"""
        focus_patterns = {
            'Training': r'training|education|course|program',
            'Legal/Advocacy': r'legal|law|rights|advocacy|ADA',
            'Community': r'community|support|forum|group',
            'Resources': r'resource|guide|information|help',
            'Services': r'service|assistance|help|support'
        }
        
        found_areas = []
        content_lower = content.lower()
        
        for area, pattern in focus_patterns.items():
            if re.search(pattern, content_lower):
                found_areas.append(area)
        
        return found_areas
    
    async def _analyze_sitemap(self, domain: str) -> Dict[str, Any]:
        """Analyze website sitemap for content structure"""
        sitemap_data = {
            'frequency': 'unknown',
            'total_pages': 0,
            'last_updated': None
        }
        
        try:
            sitemap_url = f"https://r.jina.ai/https://{domain}/sitemap.xml"
            headers = {"Authorization": f"Bearer {self.jina_api_key}"}
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(sitemap_url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    
                    # Parse dates to determine frequency
                    dates = re.findall(r'<lastmod>(\d{4}-\d{2}-\d{2})', content)
                    if dates:
                        date_objs = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
                        date_objs.sort()
                        
                        if len(date_objs) > 1:
                            # Calculate average time between posts
                            deltas = [(date_objs[i+1] - date_objs[i]).days 
                                     for i in range(len(date_objs)-1)]
                            avg_delta = sum(deltas) / len(deltas)
                            
                            if avg_delta < 3:
                                sitemap_data['frequency'] = 'daily'
                            elif avg_delta < 10:
                                sitemap_data['frequency'] = 'weekly'
                            elif avg_delta < 35:
                                sitemap_data['frequency'] = 'monthly'
                            else:
                                sitemap_data['frequency'] = 'irregular'
                        
                        sitemap_data['last_updated'] = date_objs[-1] if date_objs else None
                    
                    # Count total pages
                    sitemap_data['total_pages'] = content.count('<loc>')
        
        except Exception as e:
            logger.debug(f"Could not analyze sitemap for {domain}: {e}")
        
        return sitemap_data
    
    async def _analyze_strengths_weaknesses(
        self,
        domain: str,
        content: str
    ) -> Tuple[List[str], List[str]]:
        """Analyze competitor strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Check for various quality indicators
        content_lower = content.lower()
        
        # Strengths
        if 'expert' in content_lower or 'professional' in content_lower:
            strengths.append("Expert content/professional credibility")
        
        if re.search(r'\b20\d{2}\b', content):  # Recent year mentioned
            strengths.append("Up-to-date content")
        
        if 'video' in content_lower or 'youtube' in content_lower:
            strengths.append("Multimedia content")
        
        if 'download' in content_lower or 'pdf' in content_lower:
            strengths.append("Downloadable resources")
        
        # Weaknesses (these are assumptions based on common issues)
        if not re.search(r'contact|email|phone', content_lower):
            weaknesses.append("Limited contact options")
        
        if not re.search(r'search', content_lower):
            weaknesses.append("No visible search functionality")
        
        # Default entries if none found
        if not strengths:
            strengths.append("Established domain presence")
        
        if not weaknesses:
            weaknesses.append("Potential opportunities for differentiation")
        
        return strengths, weaknesses
    
    def _extract_article_urls(self, data: Dict, domain: str) -> List[str]:
        """Extract article URLs from scraped data"""
        urls = []
        
        # Look for links in the content
        if isinstance(data, dict):
            content = data.get('content', '') or data.get('text', '')
        else:
            content = str(data)
        
        # Find all URLs
        url_pattern = r'href=["\'](https?://[^"\']+)["\']'
        found_urls = re.findall(url_pattern, content)
        
        # Also look for relative URLs
        relative_pattern = r'href=["\'](/[^"\']+)["\']'
        relative_urls = re.findall(relative_pattern, content)
        
        # Combine and filter
        for url in found_urls:
            if domain in url and any(indicator in url for indicator in ['blog', 'article', 'post', 'news']):
                urls.append(url)
        
        for rel_url in relative_urls:
            if any(indicator in rel_url for indicator in ['blog', 'article', 'post', 'news']):
                urls.append(f"https://{domain}{rel_url}")
        
        return list(set(urls))  # Remove duplicates
    
    async def generate_comprehensive_insights(
        self,
        deep_analysis: bool = True
    ) -> CompetitorInsights:
        """
        Generate comprehensive competitive intelligence report
        
        Args:
            deep_analysis: Whether to perform deep analysis of competitors
        
        Returns:
            CompetitorInsights with full competitive intelligence
        """
        logger.info("Starting comprehensive competitor analysis...")
        
        # Analyze each competitor
        all_content = []
        competitor_profiles = []
        
        for domain in self.competitors:
            logger.info(f"Analyzing competitor: {domain}")
            
            # Get competitor profile
            if deep_analysis:
                profile = await self.analyze_competitor(domain)
                competitor_profiles.append(profile)
            
            # Scan recent content
            content = await self.scan_competitor_content(domain, limit=20)
            all_content.extend(content)
        
        # Identify trends
        trending_topics = await self.identify_trending_topics(all_content)
        
        # Find content gaps
        content_gaps = await self.identify_content_gaps(all_content, self.our_content)
        
        # Analyze our position
        our_position = await self.analyze_competitive_position(all_content, self.our_content)
        
        # Generate strategic recommendations
        recommendations = self._generate_strategic_recommendations(
            trending_topics, content_gaps, our_position
        )
        
        # Create action items
        action_items = self._create_action_items(trending_topics, content_gaps)
        
        # Count new content (simplified - would track in production)
        new_content_count = len([c for c in all_content if c.published_date and 
                                (datetime.now() - c.published_date).days < 7])
        
        return CompetitorInsights(
            scan_date=datetime.now(),
            competitors_analyzed=len(self.competitors),
            total_content_pieces=len(all_content),
            new_content_since_last_scan=new_content_count,
            trending_topics=trending_topics[:10],
            content_gaps=content_gaps[:10],
            top_performing_content=sorted(all_content, 
                                         key=lambda x: x.word_count, 
                                         reverse=True)[:10],
            competitor_profiles=competitor_profiles,
            our_position=our_position,
            strategic_recommendations=recommendations,
            action_items=action_items
        )
    
    def _generate_strategic_recommendations(
        self,
        trends: List[TrendingTopic],
        gaps: List[ContentGap],
        position: CompetitivePosition
    ) -> List[str]:
        """Generate strategic recommendations based on analysis"""
        recommendations = []
        
        # Recommendations based on trends
        rising_trends = [t for t in trends if t.momentum == "rising"]
        if rising_trends:
            recommendations.append(
                f"Priority: Create content on rising trends - '{rising_trends[0].topic}' "
                f"(trend score: {rising_trends[0].trend_score:.0f})"
            )
        
        # Recommendations based on gaps
        high_opp_gaps = [g for g in gaps if g.opportunity_score > 70]
        if high_opp_gaps:
            recommendations.append(
                f"Opportunity: Fill high-value content gap - '{high_opp_gaps[0].topic}' "
                f"(potential traffic: {high_opp_gaps[0].estimated_traffic_potential})"
            )
        
        # Recommendations based on position
        if position.market_share_estimate < 0.2:
            recommendations.append(
                "Growth: Increase content production to gain market share "
                "(currently at {:.0%})".format(position.market_share_estimate)
            )
        
        if position.content_quality_score < 60:
            recommendations.append(
                "Quality: Improve content depth and comprehensiveness to match competitors"
            )
        
        if position.topic_coverage_score < 70:
            recommendations.append(
                "Coverage: Expand into underserved topics to improve coverage "
                f"(current score: {position.topic_coverage_score:.0f}/100)"
            )
        
        # Add strategic moves
        recommendations.append(
            "Differentiation: Focus on unique angles and original research to stand out"
        )
        
        return recommendations[:6]
    
    def _create_action_items(
        self,
        trends: List[TrendingTopic],
        gaps: List[ContentGap]
    ) -> List[Dict[str, Any]]:
        """Create specific action items with priorities"""
        action_items = []
        
        # High-priority trend articles
        for trend in trends[:3]:
            if trend.trend_score > 70:
                action_items.append({
                    'priority': 'HIGH',
                    'type': 'content_creation',
                    'title': f"Write: {trend.suggested_angles[0] if trend.suggested_angles else trend.topic}",
                    'topic': trend.topic,
                    'keywords': trend.keywords[:5],
                    'estimated_impact': 'High traffic potential',
                    'timeline': '1-2 weeks'
                })
        
        # Gap-filling content
        for gap in gaps[:2]:
            if gap.opportunity_score > 60:
                action_items.append({
                    'priority': 'MEDIUM',
                    'type': 'gap_filling',
                    'title': f"Create: {gap.topic} - {gap.strategic_approach}",
                    'topic': gap.topic,
                    'keywords': gap.suggested_keywords[:5],
                    'estimated_impact': f"{gap.estimated_traffic_potential} monthly visits",
                    'timeline': '2-3 weeks'
                })
        
        # Content updates
        action_items.append({
            'priority': 'LOW',
            'type': 'content_update',
            'title': 'Update: Refresh top 5 oldest articles with 2024 information',
            'estimated_impact': 'Improved rankings and user experience',
            'timeline': '1 week'
        })
        
        return action_items
    
    def set_our_content(
        self,
        content: List[Dict[str, Any]]
    ):
        """
        Set our content for comparison
        
        Args:
            content: List of our content items with title, keywords, etc.
        """
        self.our_content = content
        self.our_topics = set()
        self.our_keywords = set()
        
        for item in content:
            # Extract topics
            topics = self._extract_topics(item.get('title', ''), item.get('keywords', {}))
            self.our_topics.update(topics)
            
            # Extract keywords
            if 'keywords' in item:
                if isinstance(item['keywords'], dict):
                    self.our_keywords.update(item['keywords'].keys())
                elif isinstance(item['keywords'], list):
                    self.our_keywords.update(item['keywords'])


# Convenience function
async def create_competitor_monitor(
    enable_jina: bool = True
) -> EnhancedCompetitorMonitoringAgent:
    """Create and return an enhanced competitor monitoring agent"""
    return EnhancedCompetitorMonitoringAgent(
        enable_ml_analysis=True
    )