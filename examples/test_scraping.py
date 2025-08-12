#!/usr/bin/env python3
"""
Test script for web scraping functionality
Tests Jina AI and Bright Data integrations
"""
import asyncio
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapers.scrapers import WebScraper, CompetitorMonitor
from agents.competitor_monitoring_agent import CompetitorMonitoringAgent


async def test_basic_scraping():
    """Test basic scraping functionality"""
    print("🔍 Testing Web Scraping")
    print("=" * 50)
    
    # Initialize scraper
    scraper = WebScraper()
    
    # Test URLs
    test_urls = [
        "https://www.ada.gov/resources/service-animals-2010-requirements/",
        "https://www.akc.org/expert-advice/training/service-dog-training-101/"
    ]
    
    for url in test_urls:
        print(f"\n📄 Scraping: {url}")
        try:
            content = await scraper.scrape(url)
            print(f"  ✅ Scraper used: {content.scraper_used}")
            print(f"  📝 Title: {content.title or 'No title'}")
            print(f"  📊 Word count: {content.word_count}")
            if content.meta_keywords:
                print(f"  🏷️ Keywords: {', '.join(content.meta_keywords[:5])}")
        except Exception as e:
            print(f"  ❌ Failed: {str(e)}")
    
    await scraper.close()


async def test_competitor_monitoring():
    """Test competitor monitoring agent"""
    print("\n\n🎯 Testing Competitor Monitoring")
    print("=" * 50)
    
    # Initialize agent with a couple competitors
    agent = CompetitorMonitoringAgent(
        competitors=[
            "servicedogcentral.org",
            "assistancedogsinternational.org"
        ]
    )
    
    # Set our content (simulated)
    agent.set_our_content(
        topics=["Service dogs", "ADA compliance"],
        keywords=["service dog", "ada", "training"]
    )
    
    print("\n📊 Generating competitor insights...")
    
    try:
        # Generate insights
        insights = await agent.generate_insights()
        
        print(f"\n✅ Analysis Complete!")
        print(f"  • Competitors analyzed: {insights.competitors_analyzed}")
        print(f"  • Content pieces found: {insights.total_content_pieces}")
        
        # Show trending topics
        if insights.trending_topics:
            print(f"\n📈 Top Trending Topics:")
            for i, topic in enumerate(insights.trending_topics[:3], 1):
                print(f"  {i}. {topic.topic} (score: {topic.trend_score:.1f})")
                if topic.suggested_angle:
                    print(f"     💡 Angle: {topic.suggested_angle}")
        
        # Show content gaps
        if insights.content_gaps:
            print(f"\n🎯 Top Content Gaps:")
            for i, gap in enumerate(insights.content_gaps[:3], 1):
                print(f"  {i}. {gap.topic}")
                print(f"     • Competitors covering: {gap.competitor_coverage}")
                print(f"     • Our coverage: {gap.our_coverage}")
                print(f"     • Opportunity score: {gap.opportunity_score:.1f}")
        
        # Show recommendations
        if insights.recommended_topics:
            print(f"\n💡 Recommended Topics to Write:")
            for i, rec in enumerate(insights.recommended_topics[:3], 1):
                print(f"  {i}. {rec}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have API keys configured:")
        print("  - JINA_API_KEY for Jina AI")
        print("  - BRIGHT_DATA_API_KEY for Bright Data (optional)")
    
    await agent.close()


async def test_fallback_scraping():
    """Test scraper fallback mechanism"""
    print("\n\n🔄 Testing Scraper Fallback")
    print("=" * 50)
    
    # Create scraper with no API keys to force BeautifulSoup fallback
    scraper = WebScraper(jina_api_key=None, bright_data_api_key=None)
    
    print("\n📝 Testing with BeautifulSoup fallback (no API keys)...")
    
    url = "https://www.example.com"
    try:
        content = await scraper.scrape(url)
        print(f"  ✅ Successfully scraped with: {content.scraper_used}")
        print(f"  📝 Title: {content.title or 'No title'}")
        print(f"  📊 Word count: {content.word_count}")
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
    
    await scraper.close()


async def main():
    """Run all tests"""
    print("🚀 Blog Poster - Web Scraping Test Suite")
    print("=" * 70)
    
    # Check for API keys
    has_jina = bool(os.getenv("JINA_API_KEY"))
    has_bright = bool(os.getenv("BRIGHT_DATA_API_KEY"))
    
    print(f"\n🔑 API Keys Status:")
    print(f"  • Jina AI: {'✅ Configured' if has_jina else '❌ Not configured'}")
    print(f"  • Bright Data: {'✅ Configured' if has_bright else '❌ Not configured'}")
    
    if not has_jina:
        print("\n⚠️ Warning: No Jina API key found. Will use fallback scrapers.")
        print("  Set JINA_API_KEY environment variable for best results.")
    
    # Run tests
    await test_basic_scraping()
    await test_fallback_scraping()
    
    if has_jina or has_bright:
        await test_competitor_monitoring()
    else:
        print("\n⚠️ Skipping competitor monitoring test (requires API keys)")
    
    print("\n\n✅ All tests complete!")


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(".env.local")
    
    # Run tests
    asyncio.run(main())