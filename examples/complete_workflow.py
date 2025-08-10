#!/usr/bin/env python3
"""
Complete Workflow: Generate Article → Publish to WordPress
This bypasses the connection test issue and publishes directly
"""
import httpx
import asyncio
import base64
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8088"
WP_URL = "http://localhost:8084"
USERNAME = "anthony"
PASSWORD = "uSn8r9f32DM4y^bXRuS9kb3K"


async def generate_article():
    """Generate an article using the API"""
    print("=" * 60)
    print("Step 1: Generating Article with AI")
    print("=" * 60)
    
    params = {
        "topic": "Understanding Service Dog Access Rights Under the ADA",
        "primary_keyword": "service dog access rights",
        "secondary_keywords": ["ADA compliance", "public accommodations", "handler rights"],
        "min_words": 500,
        "max_words": 800
    }
    
    print(f"Topic: {params['topic']}")
    print(f"Primary Keyword: {params['primary_keyword']}")
    print("\nGenerating article (this may take 30-60 seconds)...")
    print("Note: This requires valid ANTHROPIC_API_KEY or OPENAI_API_KEY in .env.local")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"{API_URL}/article/generate",
                params=params
            )
            
            if response.status_code == 200:
                article = response.json()
                if article:
                    print(f"\n✅ Article generated successfully!")
                    print(f"   Title: {article.get('title', 'No title')}")
                    print(f"   Word Count: {article.get('word_count', 'Unknown')}")
                    print(f"   SEO Score: {article.get('seo_score', 0)}/100")
                    
                    # Save locally
                    filename = f"data/articles/complete-test-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
                    try:
                        import os
                        os.makedirs("data/articles", exist_ok=True)
                        with open(filename, 'w') as f:
                            json.dump(article, f, indent=2)
                        print(f"   💾 Saved to: {filename}")
                    except:
                        pass
                    
                    return article
                else:
                    print("❌ Article generation returned empty response")
                    return None
            else:
                print(f"❌ Article generation failed: {response.status_code}")
                error_detail = response.json().get('detail', 'Unknown error')
                print(f"   Error: {error_detail}")
                
                if "AuthenticationError" in str(error_detail):
                    print("\n⚠️  API Key Issue Detected!")
                    print("   Please ensure you have valid API keys in .env.local:")
                    print("   - ANTHROPIC_API_KEY=sk-ant-api03-...")
                    print("   - or OPENAI_API_KEY=sk-...")
                return None
                
        except httpx.TimeoutException:
            print("❌ Request timed out after 120 seconds")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


async def publish_to_wordpress(article):
    """Publish the article directly to WordPress"""
    print("\n" + "=" * 60)
    print("Step 2: Publishing to WordPress")
    print("=" * 60)
    
    if not article:
        # Create a sample article if generation failed
        print("⚠️  No AI-generated article. Creating sample content...")
        article = {
            "title": f"Sample Post - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "content_html": """
<h2>Service Dog Access Rights</h2>
<p>This is a sample post demonstrating the Blog Poster system's ability to publish to WordPress.</p>

<h3>Key Points:</h3>
<ul>
    <li>Service dogs are allowed in all public accommodations under the ADA</li>
    <li>Only two questions may be asked about a service dog</li>
    <li>No registration or certification is required</li>
</ul>

<p><em>Note: This is sample content. With valid AI API keys, this would be a full article.</em></p>
""",
            "slug": f"sample-post-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "meta_title": "Service Dog Access Rights - Sample Post",
            "meta_description": "A sample post about service dog access rights under the ADA"
        }
    
    # Prepare auth
    credentials = f"{USERNAME}:{PASSWORD}"
    auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
    
    # Prepare post data
    post_data = {
        "title": article.get("title", "Untitled Post"),
        "content": article.get("content_html") or article.get("content_markdown", ""),
        "status": "draft",
        "slug": article.get("slug", f"post-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    }
    
    print(f"Publishing: {post_data['title']}")
    print(f"Status: DRAFT (for review)")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{WP_URL}/wp-json/wp/v2/posts",
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                },
                json=post_data
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"\n✅ Successfully published to WordPress!")
                print(f"   Post ID: {result['id']}")
                print(f"   Status: {result['status']}")
                print(f"\n📝 View/Edit in WordPress:")
                print(f"   {WP_URL}/wp-admin/post.php?post={result['id']}&action=edit")
                print(f"\n🔗 Preview Link:")
                print(f"   {result['link']}?preview=true")
                return result
            else:
                print(f"❌ Publishing failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error publishing: {e}")
            return None


async def main():
    """Run the complete workflow"""
    print("\n🚀 Complete Blog Poster Workflow Test")
    print("=" * 60)
    print("This test will:")
    print("1. Generate an article using AI (if API keys are configured)")
    print("2. Publish it to WordPress as a draft")
    print("3. Provide links to view/edit the post")
    print("=" * 60)
    
    # Step 1: Generate article
    article = await generate_article()
    
    # Step 2: Publish to WordPress
    result = await publish_to_wordpress(article)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Workflow Summary")
    print("=" * 60)
    
    if article and article.get('title'):
        print("✅ Article Generation: Success")
        if article.get('cost_tracking'):
            cost = article['cost_tracking'].get('cost', 0)
            print(f"   Cost: ${cost:.4f}")
    else:
        print("⚠️  Article Generation: Used sample content")
        print("   (Add valid AI API keys to generate real content)")
    
    if result:
        print("✅ WordPress Publishing: Success")
        print(f"   Post ID: {result['id']}")
    else:
        print("❌ WordPress Publishing: Failed")
    
    print("\n✨ Next Steps:")
    if result:
        print("1. Review the draft post in WordPress admin")
        print("2. Make any necessary edits")
        print("3. Publish when ready")
    else:
        print("1. Check WordPress connection and credentials")
        print("2. Ensure JSON Basic Authentication plugin is active")
    
    if not article or not article.get('title'):
        print("\n💡 To generate real articles with AI:")
        print("   Add to .env.local:")
        print("   ANTHROPIC_API_KEY=your-key-here")
        print("   or OPENAI_API_KEY=your-key-here")


if __name__ == "__main__":
    asyncio.run(main())