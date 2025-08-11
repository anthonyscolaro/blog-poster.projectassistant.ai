#!/usr/bin/env python3
"""
Test script to generate an article and publish to PRODUCTION WordPress (ServiceDogUS.org)
"""
import os
import asyncio
import httpx
import base64
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

# Load PRODUCTION environment variables (override any existing)
load_dotenv('.env.prod', override=True)

async def generate_article_with_anthropic():
    """Generate an article using Anthropic API"""
    print("=" * 60)
    print("📝 Generating Article with Anthropic API")
    print("=" * 60)
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found")
        return None
    
    print(f"✓ Using API key: {api_key[:20]}...")
    
    try:
        client = Anthropic(api_key=api_key)
        
        # Generate article about service dogs
        print("\n⏳ Generating article (this may take 20-30 seconds)...")
        
        prompt = """Write a comprehensive, SEO-optimized blog article about "5 Essential Service Dog Commands for Anxiety Support" that includes:

1. An engaging title (under 60 characters)
2. A meta description (under 155 characters)
3. The full article content (1500-2000 words) in HTML format
4. Focus on practical tips and ADA compliance
5. Include proper H2 and H3 headings
6. Add internal structure with lists and sections

Format your response as JSON with these fields:
{
  "title": "article title",
  "meta_description": "meta description",
  "content": "full HTML content",
  "slug": "url-friendly-slug"
}

Make it informative, practical, and helpful for people with anxiety who need service dog commands."""

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Parse the response
        import json
        content = response.content[0].text
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                article_data = json.loads(json_str)
            else:
                # Fallback: create structured data from response
                article_data = {
                    "title": "5 Essential Service Dog Commands for Anxiety Support",
                    "meta_description": "Learn the 5 most important service dog commands for anxiety support. Expert training tips for ADA-compliant service dogs.",
                    "content": content,
                    "slug": f"service-dog-commands-anxiety-{datetime.now().strftime('%Y%m%d')}"
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, use the content as-is
            article_data = {
                "title": "5 Essential Service Dog Commands for Anxiety Support",
                "meta_description": "Learn the 5 most important service dog commands for anxiety support.",
                "content": content,
                "slug": f"service-dog-commands-{datetime.now().strftime('%Y%m%d')}"
            }
        
        print(f"\n✅ Article generated successfully!")
        print(f"   Title: {article_data['title']}")
        print(f"   Meta: {article_data['meta_description']}")
        print(f"   Content length: {len(article_data['content'])} characters")
        
        return article_data
        
    except Exception as e:
        print(f"\n❌ Error generating article: {str(e)}")
        return None


async def publish_to_wordpress(article_data):
    """Publish the generated article to WordPress"""
    print("\n" + "=" * 60)
    print("📤 Publishing to PRODUCTION WordPress")
    print("=" * 60)
    
    # Get credentials from environment
    wp_url = os.getenv('WORDPRESS_URL')
    username = os.getenv('WP_USERNAME')
    password = os.getenv('WP_APP_PASSWORD')
    
    print(f"WordPress URL: {wp_url}")
    print(f"Username: {username}")
    print(f"Expected: https://wp.servicedogus.org")
    
    if not all([wp_url, username, password]):
        print("❌ Missing WordPress credentials in .env.prod")
        return None
    
    # Create auth header
    credentials = f"{username}:{password}"
    auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
    
    # Prepare post data
    post_data = {
        "title": article_data["title"],
        "content": article_data["content"],
        "status": "draft",  # Create as draft for safety
        "slug": article_data["slug"],
        "excerpt": article_data["meta_description"]
    }
    
    print(f"Publishing: {post_data['title']}")
    print(f"Status: {post_data['status']}")
    
    # Make the request
    async with httpx.AsyncClient(timeout=30.0, verify=False) as client:  # verify=False for local testing
        try:
            response = await client.post(
                f"{wp_url}/wp-json/wp/v2/posts",
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                },
                json=post_data
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"\n✅ Article published successfully!")
                print(f"   Post ID: {result['id']}")
                print(f"   Status: {result['status']}")
                print(f"   Link: {result['link']}")
                print(f"\n📝 Edit in WordPress:")
                print(f"   {wp_url}/wp-admin/post.php?post={result['id']}&action=edit")
                return result
            else:
                print(f"\n❌ Failed to publish article")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"\n❌ Error publishing: {e}")
            return None


async def main():
    """Run the complete production test"""
    print("\n🚀 Blog Poster - PRODUCTION Test (ServiceDogUS.org)")
    print("=" * 60)
    print("This test will:")
    print("1. Generate an article using Anthropic Claude API")
    print("2. Publish it to PRODUCTION WordPress as a draft")
    print("3. Target: https://wp.servicedogus.org")
    print("=" * 60)
    
    # Confirm production posting - auto-confirmed for testing
    print("\n⚠️  Proceeding with PRODUCTION posting (auto-confirmed for testing)")
    print("   Creating draft article on ServiceDogUS.org")
    
    # Step 1: Generate article
    article = await generate_article_with_anthropic()
    
    if not article:
        print("\n⚠️ Article generation failed. Stopping test.")
        return
    
    # Step 2: Publish to WordPress
    result = await publish_to_wordpress(article)
    
    if result:
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Production posting tested:")
        print("✅ Anthropic API key is working")
        print("✅ Article generation is working")
        print("✅ Production WordPress publishing is working")
        print("\nNext steps:")
        print("1. Review the draft in WordPress admin")
        print("2. Publish the article if it looks good")
        print("3. Run the full automated workflow for regular posting")
    else:
        print("\n" + "=" * 60)
        print("⚠️ Production publishing failed. Please check:")
        print("1. WordPress URL is correct: https://wp.servicedogus.org")
        print("2. Application Password is valid")
        print("3. WordPress REST API is enabled")
        print("4. User has publishing permissions")


if __name__ == "__main__":
    asyncio.run(main())