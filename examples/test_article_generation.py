#!/usr/bin/env python3
"""
Test script for Article Generation with real LLM integration
Tests both direct agent usage and API endpoints
"""
import asyncio
import os
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.article_generation_agent import (
    ArticleGenerationAgent, 
    SEORequirements,
    LLMProvider
)


async def test_direct_generation():
    """Test article generation directly with the agent"""
    print("🤖 Testing Direct Article Generation")
    print("=" * 50)
    
    # Check for API keys
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    
    print(f"\n🔑 API Keys Status:")
    print(f"  • Anthropic: {'✅ Configured' if has_anthropic else '❌ Not configured'}")
    print(f"  • OpenAI: {'✅ Configured' if has_openai else '❌ Not configured'}")
    
    if not has_anthropic and not has_openai:
        print("\n❌ Error: No LLM API keys configured!")
        print("  Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env.local")
        return
    
    # Initialize agent
    provider = LLMProvider.ANTHROPIC if has_anthropic else LLMProvider.OPENAI
    agent = ArticleGenerationAgent(
        default_provider=provider,
        max_cost_per_article=0.50
    )
    
    # Define test topic and SEO requirements
    test_topic = "How to Travel with a Service Dog: Complete Guide for Air Travel"
    
    seo_reqs = SEORequirements(
        primary_keyword="traveling with service dog",
        secondary_keywords=[
            "service dog air travel",
            "ADA requirements",
            "airline policies",
            "documentation",
            "international travel"
        ],
        min_words=1500,
        max_words=2000
    )
    
    print(f"\n📝 Generating article about: {test_topic}")
    print(f"  • Primary keyword: {seo_reqs.primary_keyword}")
    print(f"  • Target length: {seo_reqs.min_words}-{seo_reqs.max_words} words")
    print("\n⏳ This may take 30-60 seconds...")
    
    try:
        # Generate article
        article = await agent.generate_article(
            topic=test_topic,
            seo_requirements=seo_reqs,
            brand_voice="professional, empathetic, and informative",
            target_audience="Service dog handlers planning to travel",
            additional_context="Focus on practical tips and recent airline policy changes"
        )
        
        print(f"\n✅ Article generated successfully!")
        print(f"  • Title: {article.title}")
        print(f"  • Word count: {article.word_count}")
        print(f"  • SEO score: {article.seo_score:.1f}/100")
        print(f"  • Reading time: {article.estimated_reading_time} minutes")
        print(f"  • Cost: ${article.cost_tracking.cost:.4f}" if article.cost_tracking else "  • Cost: N/A")
        
        print(f"\n📊 SEO Metadata:")
        print(f"  • Meta title ({len(article.meta_title)} chars): {article.meta_title}")
        print(f"  • Meta description ({len(article.meta_description)} chars):")
        print(f"    {article.meta_description}")
        
        print(f"\n📄 First 500 characters of content:")
        print("-" * 40)
        print(article.content_markdown[:500] + "...")
        
        # Save to file
        output_file = Path("data/articles") / f"{article.slug}.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(f"# {article.title}\n\n")
            f.write(f"**Meta Title:** {article.meta_title}\n")
            f.write(f"**Meta Description:** {article.meta_description}\n")
            f.write(f"**Keywords:** {', '.join([article.primary_keyword] + article.secondary_keywords)}\n\n")
            f.write("---\n\n")
            f.write(article.content_markdown)
        
        print(f"\n💾 Article saved to: {output_file}")
        
        # Get cost summary
        cost_summary = agent.get_cost_summary()
        print(f"\n💰 Cost Summary:")
        print(f"  • Total cost: ${cost_summary['total_cost']:.4f}")
        print(f"  • Average per article: ${cost_summary['average_cost_per_article']:.4f}")
        
    except Exception as e:
        print(f"\n❌ Error generating article: {str(e)}")
        print("\nPossible issues:")
        print("  1. API key is invalid")
        print("  2. Rate limit exceeded")
        print("  3. Network connection issues")


async def test_api_generation():
    """Test article generation through API endpoints"""
    print("\n\n🌐 Testing Article Generation via API")
    print("=" * 50)
    
    import httpx
    
    base_url = "http://localhost:8088"
    
    # Check if API is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/health")
            if response.status_code != 200:
                print("❌ API is not running. Start it with: docker compose up")
                return
    except Exception:
        print("❌ Cannot connect to API at http://localhost:8088")
        print("  Start the API with: docker compose up")
        return
    
    print("✅ API is running")
    
    # Test article generation endpoint
    async with httpx.AsyncClient(timeout=120.0) as client:
        print("\n📝 Requesting article generation...")
        
        payload = {
            "topic": "Service Dog Etiquette: What Not to Do When You See a Working Dog",
            "primary_keyword": "service dog etiquette",
            "secondary_keywords": [
                "working dog",
                "service dog rules",
                "how to act around service dogs",
                "ADA guidelines"
            ],
            "min_words": 1200,
            "max_words": 1800,
            "use_competitor_insights": False  # Skip for faster testing
        }
        
        try:
            response = await client.post(
                f"{base_url}/article/generate",
                json=payload
            )
            
            if response.status_code == 200:
                article = response.json()
                print(f"\n✅ Article generated via API!")
                print(f"  • Title: {article['title']}")
                print(f"  • Word count: {article['word_count']}")
                print(f"  • SEO score: {article['seo_score']:.1f}/100")
                print(f"  • Cost: ${article.get('cost_tracking', {}).get('cost', 0):.4f}")
            else:
                print(f"\n❌ API returned error: {response.status_code}")
                print(f"  Response: {response.text}")
                
        except httpx.TimeoutException:
            print("\n⏱️ Request timed out (>120 seconds)")
            print("  Article generation can take time with LLMs")
        except Exception as e:
            print(f"\n❌ Error calling API: {str(e)}")
    
    # Test cost endpoint
    print("\n💰 Checking generation costs...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_url}/article/costs")
            if response.status_code == 200:
                costs = response.json()
                print(f"  • Total cost: ${costs.get('total_cost', 0):.4f}")
                print(f"  • Articles generated: {costs.get('articles_generated', 0)}")
        except Exception as e:
            print(f"  ❌ Could not get costs: {e}")


async def test_with_competitor_insights():
    """Test article generation using competitor insights"""
    print("\n\n🔍 Testing Article Generation with Competitor Insights")
    print("=" * 50)
    
    # This requires both scraping and LLM APIs
    has_jina = bool(os.getenv("JINA_API_KEY"))
    has_llm = bool(os.getenv("ANTHROPIC_API_KEY")) or bool(os.getenv("OPENAI_API_KEY"))
    
    if not has_jina:
        print("⚠️ Jina API key not configured - skipping competitor insights test")
        return
    
    if not has_llm:
        print("⚠️ No LLM API key configured - skipping this test")
        return
    
    from agents.competitor_monitoring_agent import CompetitorMonitoringAgent
    
    print("📊 Gathering competitor insights...")
    
    # Get competitor insights
    comp_agent = CompetitorMonitoringAgent(
        competitors=["servicedogcentral.org"]  # Just one for speed
    )
    
    try:
        insights = await comp_agent.generate_insights()
        
        if insights.trending_topics:
            trending_topic = insights.trending_topics[0]
            print(f"\n📈 Found trending topic: {trending_topic.topic}")
            print(f"  • Trend score: {trending_topic.trend_score:.1f}")
            print(f"  • Suggested angle: {trending_topic.suggested_angle}")
            
            # Generate article based on trending topic
            print(f"\n📝 Generating article based on trend...")
            
            agent = ArticleGenerationAgent()
            seo_reqs = SEORequirements(
                primary_keyword=trending_topic.topic.lower(),
                secondary_keywords=trending_topic.keywords[:5],
                min_words=1500,
                max_words=2000
            )
            
            article = await agent.generate_article(
                topic=trending_topic.topic,
                seo_requirements=seo_reqs,
                brand_voice="professional and informative",
                target_audience="Service dog handlers",
                additional_context=trending_topic.suggested_angle,
                competitor_insights={
                    "trending": True,
                    "trend_score": trending_topic.trend_score,
                    "competitor_sources": [str(url) for url in trending_topic.sources[:3]]
                }
            )
            
            print(f"\n✅ Article generated from competitor insights!")
            print(f"  • Title: {article.title}")
            print(f"  • Based on trend with score: {trending_topic.trend_score:.1f}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    finally:
        await comp_agent.close()


async def main():
    """Run all tests"""
    print("🚀 Blog Poster - Article Generation Test Suite")
    print("=" * 70)
    
    # Test direct generation
    await test_direct_generation()
    
    # Test API generation
    await test_api_generation()
    
    # Test with competitor insights
    await test_with_competitor_insights()
    
    print("\n\n✅ All tests complete!")
    print("\n📌 Next steps:")
    print("  1. Review generated articles in data/articles/")
    print("  2. Check SEO scores and optimize if needed")
    print("  3. Use /publish/wp endpoint to publish to WordPress")


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv(".env.local")
    
    # Run tests
    asyncio.run(main())