#!/usr/bin/env python3
"""
Test Full Workflow: Generate and Publish Article
"""
import asyncio
import httpx
import json
from datetime import datetime

API_URL = "http://localhost:8088"


async def generate_article():
    """Generate an article about service dogs"""
    print("=" * 60)
    print("Step 1: Generating Article")
    print("=" * 60)
    
    params = {
        "topic": "Essential Service Dog Commands Every Handler Should Know",
        "primary_keyword": "service dog commands",
        "secondary_keywords": ["ADA requirements", "training tips"],
        "min_words": 800,
        "max_words": 1200
    }
    
    print(f"Topic: {params['topic']}")
    print(f"Keywords: {params['primary_keyword']}, {', '.join(params['secondary_keywords'])}")
    print("Generating article (this may take 30-60 seconds)...")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"{API_URL}/article/generate",
                params=params
            )
            
            if response.status_code == 200:
                article = response.json()
                print(f"✅ Article generated successfully!")
                print(f"   Title: {article.get('title', 'N/A')}")
                print(f"   Word Count: {article.get('word_count', 'N/A')}")
                print(f"   SEO Score: {article.get('seo_score', 'N/A')}/100")
                return article
            else:
                print(f"❌ Failed to generate article: {response.status_code}")
                if response.text:
                    error = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                    print(f"   Error: {error}")
                return None
        except httpx.TimeoutException:
            print("❌ Request timed out after 120 seconds")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


async def publish_article(article):
    """Publish the generated article to WordPress"""
    print("\n" + "=" * 60)
    print("Step 2: Publishing to WordPress")
    print("=" * 60)
    
    if not article:
        print("⚠️  No article to publish")
        return False
    
    # Prepare content for WordPress
    title = article.get("title", f"Test Article - {datetime.now().strftime('%Y-%m-%d')}")
    content = article.get("content_html") or article.get("content_markdown", "")
    slug = article.get("slug", "test-article-" + datetime.now().strftime("%Y%m%d"))
    
    print(f"Publishing: {title}")
    print(f"Slug: {slug}")
    print("Status: DRAFT (for review)")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{API_URL}/publish/wp",
                params={
                    "title": title,
                    "content": content,
                    "status": "draft",
                    "slug": slug,
                    "meta_title": article.get("meta_title", title),
                    "meta_description": article.get("meta_description", "")
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    print(f"✅ Article published successfully!")
                    print(f"\n📝 Post Details:")
                    print(f"   Post ID: {result.get('post_id', 'N/A')}")
                    print(f"   Status: {result.get('status', 'N/A')}")
                    print(f"\n🔗 Links:")
                    if result.get('edit_link'):
                        print(f"   Edit: {result['edit_link']}")
                    if result.get('preview_link'):
                        print(f"   Preview: {result['preview_link']}")
                    return True
                else:
                    print(f"❌ Publishing failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ API request failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


async def test_wordpress_connection():
    """Quick test of WordPress connection"""
    print("Testing WordPress connection...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/wordpress/test")
        result = response.json()
        if result.get("connected"):
            print(f"✅ WordPress connected at {result['wordpress_url']}")
            return True
        else:
            print(f"⚠️  WordPress not connected: {result.get('error')}")
            print("   Note: WordPress publishing may fail")
            return False


async def main():
    """Run the full workflow"""
    print("\n🚀 Full Workflow Test: Generate → Publish")
    print("=" * 60)
    
    # Test WordPress connection (optional, don't block on failure)
    wordpress_ok = await test_wordpress_connection()
    
    # Step 1: Generate article
    article = await generate_article()
    
    if article:
        # Save article locally for backup
        filename = f"data/articles/generated-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        try:
            import os
            os.makedirs("data/articles", exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(article, f, indent=2)
            print(f"\n💾 Article saved to: {filename}")
        except:
            pass
        
        # Step 2: Publish to WordPress (if connected)
        if wordpress_ok:
            await publish_article(article)
        else:
            print("\n⚠️  Skipping WordPress publishing due to connection issues")
            print("   Article has been generated and saved locally")
    
    print("\n" + "=" * 60)
    print("Workflow complete!")
    
    # Show summary
    if article:
        print("\n📊 Summary:")
        print(f"   ✅ Article generated: {article.get('title', 'Yes')}")
        print(f"   {'✅' if wordpress_ok else '⚠️ '} WordPress publishing: {'Attempted' if wordpress_ok else 'Skipped'}")
        print(f"   ✅ Local backup saved")
        
        if article.get('cost_tracking'):
            cost = article['cost_tracking'].get('cost', 0)
            print(f"\n💰 Cost: ${cost:.4f}")


if __name__ == "__main__":
    asyncio.run(main())