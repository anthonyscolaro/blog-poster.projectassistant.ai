"""
Web Scraping Module with Multiple Provider Support
Supports Jina AI (primary) and Bright Data (fallback) for robust content extraction
"""
import os
import json
import asyncio
import hashlib
from typing import Optional, Dict, List, Any, Literal
from datetime import datetime
from urllib.parse import urlparse, quote
import httpx
from pydantic import BaseModel, HttpUrl, Field
import logging
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class ScrapedContent(BaseModel):
    """Structured data from scraped content"""
    url: HttpUrl
    title: Optional[str] = None
    content: str
    markdown: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: List[str] = Field(default_factory=list)
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    images: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)
    scraper_used: str
    scraped_at: datetime = Field(default_factory=datetime.now)
    word_count: int = 0
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.content:
            self.word_count = len(self.content.split())


class CompetitorContent(BaseModel):
    """Analyzed competitor content"""
    source_url: HttpUrl
    domain: str
    title: str
    topics: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    content_type: Literal["blog", "news", "social", "product", "other"]
    sentiment: Optional[float] = None  # -1 to 1
    engagement_metrics: Dict[str, Any] = Field(default_factory=dict)
    scraped_content: ScrapedContent


class WebScraper:
    """
    Multi-provider web scraping with automatic fallback
    Priority: Jina AI -> Bright Data -> BeautifulSoup
    """
    
    def __init__(
        self,
        jina_api_key: Optional[str] = None,
        bright_data_api_key: Optional[str] = None,
        timeout: int = 30
    ):
        # Try to get API keys from secure storage or environment
        from src.utils.api_key_utils import get_jina_api_key, get_bright_data_api_key
        
        self.jina_api_key = jina_api_key or get_jina_api_key()
        self.bright_data_api_key = bright_data_api_key or get_bright_data_api_key()
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        
        # Check available scrapers
        self.available_scrapers = []
        if self.jina_api_key:
            self.available_scrapers.append("jina")
            logger.info("Jina AI scraper configured")
        if self.bright_data_api_key:
            self.available_scrapers.append("bright_data")
            logger.info("Bright Data scraper configured")
        self.available_scrapers.append("beautifulsoup")  # Always available
        
        if not self.available_scrapers:
            logger.warning("No API keys configured, falling back to BeautifulSoup only")
    
    async def scrape(self, url: str, prefer_scraper: Optional[str] = None) -> ScrapedContent:
        """
        Scrape a URL with automatic fallback between providers
        
        Args:
            url: URL to scrape
            prefer_scraper: Preferred scraper to use (jina, bright_data, beautifulsoup)
        
        Returns:
            ScrapedContent with extracted data
        """
        scrapers_to_try = []
        
        # If a specific scraper is preferred and available, try it first
        if prefer_scraper and prefer_scraper in self.available_scrapers:
            scrapers_to_try.append(prefer_scraper)
        
        # Add remaining scrapers as fallbacks
        for scraper in self.available_scrapers:
            if scraper not in scrapers_to_try:
                scrapers_to_try.append(scraper)
        
        last_error = None
        for scraper_name in scrapers_to_try:
            try:
                logger.info(f"Attempting to scrape {url} with {scraper_name}")
                
                if scraper_name == "jina":
                    return await self._scrape_with_jina(url)
                elif scraper_name == "bright_data":
                    return await self._scrape_with_bright_data(url)
                elif scraper_name == "beautifulsoup":
                    return await self._scrape_with_beautifulsoup(url)
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Failed to scrape with {scraper_name}: {str(e)}")
                continue
        
        # If all scrapers failed, raise the last error
        raise Exception(f"All scrapers failed for {url}. Last error: {str(last_error)}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _scrape_with_jina(self, url: str) -> ScrapedContent:
        """Scrape using Jina AI's r.jina.ai service"""
        jina_url = f"https://r.jina.ai/{url}"
        
        headers = {
            "Authorization": f"Bearer {self.jina_api_key}",
            "Accept": "application/json",
            "X-Return-Format": "markdown"
        }
        
        response = await self.client.get(jina_url, headers=headers)
        response.raise_for_status()
        
        # Jina returns markdown directly
        content = response.text
        
        # Try to extract title from markdown (usually first # heading)
        title = None
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        return ScrapedContent(
            url=url,
            title=title,
            content=content,
            markdown=content,
            scraper_used="jina"
        )
    
    async def _scrape_with_bright_data(self, url: str) -> ScrapedContent:
        """Scrape using Bright Data's Web Scraper API"""
        
        # Bright Data endpoint for web scraping
        # Note: This is a simplified implementation - Bright Data has various endpoints
        # for different types of scraping (social media, e-commerce, etc.)
        endpoint = "https://api.brightdata.com/datasets/v3/trigger"
        
        headers = {
            "Authorization": f"Bearer {self.bright_data_api_key}",
            "Content-Type": "application/json"
        }
        
        # Determine dataset ID based on URL domain
        domain = urlparse(url).netloc.lower()
        dataset_id = self._get_bright_data_dataset_id(domain)
        
        payload = {
            "dataset_id": dataset_id,
            "format": "json",
            "data": [{"url": url}]
        }
        
        response = await self.client.post(
            endpoint,
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Parse Bright Data response (structure varies by dataset)
        content = self._parse_bright_data_response(data, domain)
        
        return content
    
    def _get_bright_data_dataset_id(self, domain: str) -> str:
        """Get appropriate Bright Data dataset ID based on domain"""
        # Map common domains to Bright Data dataset IDs
        # These would be configured based on your Bright Data account
        dataset_map = {
            "instagram.com": "gd_ltppn085pokosxh13",  # Instagram dataset
            "facebook.com": "gd_facebook_dataset_id",
            "twitter.com": "gd_twitter_dataset_id",
            "x.com": "gd_twitter_dataset_id",
            "linkedin.com": "gd_linkedin_dataset_id",
            "tiktok.com": "gd_tiktok_dataset_id",
            # Default web scraper for other domains
            "default": "gd_web_scraper_default"
        }
        
        for key in dataset_map:
            if key in domain:
                return dataset_map[key]
        
        return dataset_map["default"]
    
    def _parse_bright_data_response(self, data: Dict, domain: str) -> ScrapedContent:
        """Parse Bright Data response based on the dataset type"""
        # Bright Data returns different structures for different datasets
        # This is a simplified parser
        
        content_data = data[0] if isinstance(data, list) else data
        
        # Extract common fields
        title = content_data.get("title", "")
        content = content_data.get("content", content_data.get("description", ""))
        author = content_data.get("author", content_data.get("user_posted", ""))
        
        # For social media posts
        if any(social in domain for social in ["instagram", "facebook", "twitter", "tiktok"]):
            content = content_data.get("description", content_data.get("text", ""))
            images = content_data.get("photos", content_data.get("images", []))
            engagement = {
                "likes": content_data.get("likes", 0),
                "comments": content_data.get("num_comments", 0),
                "shares": content_data.get("shares", 0),
                "views": content_data.get("views", 0)
            }
        else:
            images = content_data.get("images", [])
            engagement = {}
        
        return ScrapedContent(
            url=content_data.get("url", domain),
            title=title,
            content=content,
            author=author,
            images=images,
            scraper_used="bright_data"
        )
    
    async def _scrape_with_beautifulsoup(self, url: str) -> ScrapedContent:
        """Fallback scraper using BeautifulSoup for simple HTML parsing"""
        response = await self.client.get(url, follow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = None
        if soup.title:
            title = soup.title.string
        elif soup.find('h1'):
            title = soup.find('h1').get_text().strip()
        
        # Extract meta description
        meta_desc = None
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content')
        
        # Extract meta keywords
        keywords = []
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag:
            keywords = [k.strip() for k in keywords_tag.get('content', '').split(',')]
        
        # Extract main content (try common content containers)
        content = ""
        content_selectors = [
            'article', 'main', '.content', '#content', 
            '.post-content', '.entry-content', '.article-body'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                content = content_elem.get_text(separator='\n', strip=True)
                break
        
        # Fallback to body if no content container found
        if not content:
            body = soup.find('body')
            if body:
                # Remove script and style elements
                for script in body(["script", "style"]):
                    script.decompose()
                content = body.get_text(separator='\n', strip=True)
        
        # Extract images
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # Make absolute URL if relative
                if not src.startswith('http'):
                    from urllib.parse import urljoin
                    src = urljoin(url, src)
                images.append(src)
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http'):
                links.append(href)
        
        return ScrapedContent(
            url=url,
            title=title,
            content=content,
            meta_description=meta_desc,
            meta_keywords=keywords,
            images=images[:10],  # Limit to first 10 images
            links=links[:20],    # Limit to first 20 links
            scraper_used="beautifulsoup"
        )
    
    async def scrape_multiple(
        self, 
        urls: List[str], 
        max_concurrent: int = 5
    ) -> List[ScrapedContent]:
        """
        Scrape multiple URLs concurrently
        
        Args:
            urls: List of URLs to scrape
            max_concurrent: Maximum concurrent requests
        
        Returns:
            List of ScrapedContent objects
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_limit(url):
            async with semaphore:
                try:
                    return await self.scrape(url)
                except Exception as e:
                    logger.error(f"Failed to scrape {url}: {str(e)}")
                    return None
        
        results = await asyncio.gather(*[scrape_with_limit(url) for url in urls])
        
        # Filter out None results from failed scrapes
        return [r for r in results if r is not None]
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class CompetitorMonitor:
    """
    Monitor competitor websites and extract valuable insights
    """
    
    def __init__(self, scraper: Optional[WebScraper] = None):
        self.scraper = scraper or WebScraper()
        self.competitors = []
        
    def add_competitor(self, domain: str, check_paths: List[str] = None):
        """
        Add a competitor to monitor
        
        Args:
            domain: Competitor domain (e.g., "example.com")
            check_paths: Specific paths to check (e.g., ["/blog", "/news"])
        """
        if not domain.startswith('http'):
            domain = f"https://{domain}"
        
        self.competitors.append({
            "domain": domain,
            "paths": check_paths or ["/", "/blog", "/news", "/resources"]
        })
    
    async def scan_competitors(self) -> List[CompetitorContent]:
        """
        Scan all configured competitors and extract content
        
        Returns:
            List of analyzed competitor content
        """
        all_content = []
        
        for competitor in self.competitors:
            domain = competitor["domain"]
            
            # Build URLs to scan
            urls = []
            for path in competitor["paths"]:
                url = f"{domain}{path}" if path.startswith('/') else f"{domain}/{path}"
                urls.append(url)
            
            # Scrape all URLs for this competitor
            scraped_contents = await self.scraper.scrape_multiple(urls)
            
            # Analyze each piece of content
            for content in scraped_contents:
                analyzed = self._analyze_content(content)
                all_content.append(analyzed)
        
        return all_content
    
    def _analyze_content(self, scraped: ScrapedContent) -> CompetitorContent:
        """
        Analyze scraped content to extract topics and insights
        
        Args:
            scraped: Raw scraped content
        
        Returns:
            Analyzed competitor content
        """
        # Extract domain from URL
        domain = urlparse(str(scraped.url)).netloc
        
        # Basic topic extraction (would be enhanced with NLP/LLM)
        topics = self._extract_topics(scraped.content)
        
        # Extract keywords from meta or content
        keywords = scraped.meta_keywords
        if not keywords and scraped.content:
            # Simple keyword extraction (would use TF-IDF or similar in production)
            keywords = self._extract_keywords(scraped.content)
        
        # Determine content type
        content_type = self._classify_content_type(scraped.url, scraped.content)
        
        return CompetitorContent(
            source_url=scraped.url,
            domain=domain,
            title=scraped.title or "Untitled",
            topics=topics,
            keywords=keywords,
            content_type=content_type,
            scraped_content=scraped
        )
    
    def _extract_topics(self, content: str) -> List[str]:
        """
        Extract main topics from content
        This is a simplified version - would use NLP/LLM in production
        """
        # Common ADA/Service Dog related topics to look for
        topic_keywords = {
            "ADA compliance": ["ada", "americans with disabilities", "compliance"],
            "Service dogs": ["service dog", "service animal", "assistance dog"],
            "ESA": ["emotional support", "esa", "comfort animal"],
            "Training": ["training", "obedience", "behavior"],
            "Laws": ["law", "legal", "regulation", "requirement"],
            "Rights": ["rights", "access", "accommodation"],
            "Public access": ["public", "access", "restaurant", "store", "airplane"],
            "Housing": ["housing", "apartment", "landlord", "rent"],
            "Healthcare": ["healthcare", "medical", "doctor", "therapy"],
            "Veterans": ["veteran", "ptsd", "military", "va"]
        }
        
        content_lower = content.lower()
        found_topics = []
        
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    found_topics.append(topic)
                    break
        
        return list(set(found_topics))
    
    def _extract_keywords(self, content: str, max_keywords: int = 10) -> List[str]:
        """
        Extract keywords from content
        Simple implementation - would use TF-IDF or TextRank in production
        """
        # Common stop words to exclude
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
            'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this',
            'it', 'from', 'be', 'are', 'was', 'were', 'been'
        }
        
        # Simple word frequency approach
        words = content.lower().split()
        word_freq = {}
        
        for word in words:
            # Clean word
            word = ''.join(c for c in word if c.isalnum())
            
            # Skip short words and stop words
            if len(word) < 4 or word in stop_words:
                continue
            
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:max_keywords]]
    
    def _classify_content_type(self, url: str, content: str) -> str:
        """
        Classify the type of content based on URL and content
        """
        url_str = str(url).lower()
        content_lower = content.lower() if content else ""
        
        if any(x in url_str for x in ['/blog', '/post', '/article']):
            return "blog"
        elif any(x in url_str for x in ['/news', '/press', '/announcement']):
            return "news"
        elif any(x in url_str for x in ['/product', '/shop', '/store']):
            return "product"
        elif any(x in url_str for x in ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']):
            return "social"
        elif len(content_lower) > 2000 and any(x in content_lower for x in ['guide', 'how to', 'tutorial']):
            return "blog"
        else:
            return "other"


# Usage example
async def main():
    """Example usage of the scraping system"""
    
    # Initialize scraper with API keys
    scraper = WebScraper(
        jina_api_key=os.getenv("JINA_API_KEY"),
        bright_data_api_key=os.getenv("BRIGHT_DATA_API_KEY")
    )
    
    # Example 1: Scrape a single URL
    try:
        content = await scraper.scrape("https://www.ada.gov/resources/service-animals-2010-requirements/")
        print(f"Scraped {content.url} using {content.scraper_used}")
        print(f"Title: {content.title}")
        print(f"Word count: {content.word_count}")
    except Exception as e:
        print(f"Failed to scrape: {e}")
    
    # Example 2: Monitor competitors
    monitor = CompetitorMonitor(scraper)
    monitor.add_competitor("servicedogcentral.org", ["/blog", "/resources"])
    monitor.add_competitor("assistancedogsinternational.org", ["/", "/news"])
    
    competitor_content = await monitor.scan_competitors()
    
    for content in competitor_content:
        print(f"\nCompetitor: {content.domain}")
        print(f"Title: {content.title}")
        print(f"Topics: {', '.join(content.topics)}")
        print(f"Type: {content.content_type}")
    
    await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())