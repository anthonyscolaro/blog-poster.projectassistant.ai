#!/usr/bin/env python3
"""
Test script that can use any environment file (.env.local, .env.prod, etc.)
Usage: python test_with_env.py [env_file]
Default: .env.local
"""
import sys
import os
import asyncio
import httpx
import base64
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

# Determine which env file to use
env_file = sys.argv[1] if len(sys.argv) > 1 else '.env.local'
print(f"🔧 Using environment file: {env_file}")

# Load environment variables
if not os.path.exists(env_file):
    print(f"❌ Environment file {env_file} not found")
    exit(1)

load_dotenv(env_file, override=True)

# Get configuration from environment variables
WP_URL = os.getenv('WORDPRESS_URL')
USERNAME = os.getenv('WP_USERNAME')
PASSWORD = os.getenv('WP_APP_PASSWORD')

print(f"📍 Target WordPress: {WP_URL}")
print(f"👤 Username: {USERNAME}")

# Validate required environment variables
if not all([WP_URL, USERNAME, PASSWORD]):
    print("❌ Missing required environment variables:")
    if not WP_URL:
        print("   WORDPRESS_URL not set")
    if not USERNAME:
        print("   WP_USERNAME not set")  
    if not PASSWORD:
        print("   WP_APP_PASSWORD not set")
    exit(1)

async def generate_article_with_anthropic():
    """Generate an article using Anthropic API"""
    print("\n" + "=" * 60)
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
        
        prompt = """Write a comprehensive, SEO-optimized blog article about "Understanding ADA Service Dog Requirements" that includes:

1. An engaging title (under 60 characters)
2. A meta description (under 155 characters)  
3. The full article content (1500-2000 words) in HTML format
4. Focus on practical ADA compliance information
5. Include proper H2 and H3 headings
6. Add internal structure with lists and sections

Format your response as JSON with these fields:
{
  "title": "article title",
  "meta_description": "meta description",
  "content": "full HTML content",
  "slug": "url-friendly-slug"
}

Make it informative and helpful for people who need to understand ADA service dog requirements."""

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
                    "title": "Understanding ADA Service Dog Requirements",
                    "meta_description": "Learn the essential ADA requirements for service dogs. Complete guide to legal rights, training standards, and compliance.",
                    "content": content,
                    "slug": f"ada-service-dog-requirements-{datetime.now().strftime('%Y%m%d')}"
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, use the content as-is
            article_data = {
                "title": "Understanding ADA Service Dog Requirements",
                "meta_description": "Learn the essential ADA requirements for service dogs.",
                "content": content,
                "slug": f"ada-service-dog-{datetime.now().strftime('%Y%m%d')}"
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
    print("📤 Publishing to WordPress")
    print("=" * 60)
    
    print(f"WordPress URL: {WP_URL}")
    print(f"Username: {USERNAME}")
    
    # Create auth header
    credentials = f"{USERNAME}:{PASSWORD}"
    auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
    
    # Prepare post data
    post_data = {
        "title": article_data["title"],
        "content": article_data["content"],
        "status": "draft",  # Always create as draft for safety
        "slug": article_data["slug"],
        "excerpt": article_data["meta_description"]
    }
    
    print(f"Publishing: {post_data['title']}")
    print(f"Status: {post_data['status']}")
    
    # Determine SSL verification based on URL
    verify_ssl = not WP_URL.startswith('http://localhost')
    
    # Make the request
    async with httpx.AsyncClient(timeout=30.0, verify=verify_ssl) as client:
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
                print(f"\n✅ Article published successfully!")
                print(f"   Post ID: {result['id']}")
                print(f"   Status: {result['status']}")
                print(f"   Link: {result['link']}")
                print(f"\n📝 Edit in WordPress:")
                print(f"   {WP_URL}/wp-admin/post.php?post={result['id']}&action=edit")
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
    """Run the complete test"""
    env_type = "PRODUCTION" if "prod" in env_file else "LOCAL"
    
    print(f"\n🚀 Blog Poster - {env_type} Test")
    print("=" * 60)
    print("This test will:")
    print("1. Generate an article using Anthropic Claude API")
    print("2. Publish it to WordPress as a draft")
    print(f"3. Target: {WP_URL}")
    print("=" * 60)
    
    # Step 1: Generate article
    article = await generate_article_with_anthropic()
    
    if not article:
        print("\n⚠️ Article generation failed. Stopping test.")
        return
    
    # Step 2: Publish to WordPress
    result = await publish_to_wordpress(article)
    
    if result:
        print("\n" + "=" * 60)
        print(f"🎉 SUCCESS! {env_type} posting tested:")
        print("✅ Anthropic API key is working")
        print("✅ Article generation is working") 
        print("✅ WordPress publishing is working")
        print("\nNext steps:")
        print("1. Review the draft in WordPress admin")
        print("2. Publish the article if it looks good")
        print("3. Run the full automated workflow for regular posting")
    else:
        print("\n" + "=" * 60)
        print(f"⚠️ {env_type} publishing failed. Please check:")
        print(f"1. WordPress URL is accessible: {WP_URL}")
        print("2. Credentials are correct")
        print("3. WordPress REST API is enabled")
        print("4. User has publishing permissions")

if __name__ == "__main__":
    asyncio.run(main())