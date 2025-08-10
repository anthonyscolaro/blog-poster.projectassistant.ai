#!/usr/bin/env python3
"""
Direct WordPress Publishing Test
Tests publishing directly without the connection test
"""
import httpx
import asyncio
import base64
from datetime import datetime

# Configuration
WP_URL = "http://localhost:8084"
USERNAME = "anthony"
PASSWORD = "uSn8r9f32DM4y^bXRuS9kb3K"


async def create_wordpress_post():
    """Create a post directly in WordPress"""
    print("=" * 60)
    print("Direct WordPress Publishing Test")
    print("=" * 60)
    
    # Create auth header
    credentials = f"{USERNAME}:{PASSWORD}"
    auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
    
    # Post data
    post_data = {
        "title": f"Blog Poster Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": """
<h2>Automated Blog Post</h2>
<p>This post was created by the Blog Poster system to test WordPress integration.</p>

<h3>Features Tested:</h3>
<ul>
    <li>✅ JSON Basic Authentication</li>
    <li>✅ WordPress REST API</li>
    <li>✅ Creating draft posts</li>
    <li>✅ Setting post metadata</li>
</ul>

<p><strong>Service Dog Information:</strong> Service dogs are specially trained to assist 
individuals with disabilities. Under the ADA, they are permitted in all public accommodations.</p>
""",
        "status": "draft",
        "slug": f"test-post-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    }
    
    print(f"Creating post: {post_data['title']}")
    print(f"Status: {post_data['status']}")
    
    # Make the request
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
                print(f"\n✅ Post created successfully!")
                print(f"   Post ID: {result['id']}")
                print(f"   Status: {result['status']}")
                print(f"   Link: {result['link']}")
                print(f"\n📝 Edit in WordPress:")
                print(f"   {WP_URL}/wp-admin/post.php?post={result['id']}&action=edit")
                return result
            else:
                print(f"\n❌ Failed to create post")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None


async def main():
    """Run the test"""
    print("\n🚀 Starting Direct WordPress Publishing Test")
    print("Using credentials from .env.local")
    print("=" * 60)
    
    result = await create_wordpress_post()
    
    if result:
        print("\n" + "=" * 60)
        print("✨ Success! You can now:")
        print("1. Check the post in WordPress admin")
        print("2. Run the full workflow test")
        print("3. Generate articles with AI and publish them")
    else:
        print("\n" + "=" * 60)
        print("⚠️  Test failed. Please check:")
        print("1. WordPress is running at http://localhost:8084")
        print("2. JSON Basic Authentication plugin is activated")
        print("3. Username and password are correct in .env.local")


if __name__ == "__main__":
    asyncio.run(main())