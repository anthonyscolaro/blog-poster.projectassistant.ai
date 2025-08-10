#!/usr/bin/env python3
"""
Test WordPress Publishing
Tests the WordPress publishing functionality with Basic Authentication
"""
import asyncio
import httpx
from datetime import datetime

# API Configuration
API_URL = "http://localhost:8088"
WP_URL = "http://localhost:8084"


async def test_wordpress_connection():
    """Test WordPress connection"""
    print("=" * 60)
    print("Testing WordPress Connection")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/wordpress/test")
        result = response.json()
        
        if result.get("connected"):
            print(f"✅ Connected to WordPress: {result['wordpress_url']}")
            print(f"   Auth Method: {result['auth_method']}")
            print(f"   Environment: {'Local' if result['is_local'] else 'Production'}")
            
            if result.get("categories"):
                print(f"\n   Available Categories:")
                for cat in result["categories"]:
                    print(f"   - {cat['name']} (ID: {cat['id']})")
            
            if result.get("tags"):
                print(f"\n   Available Tags:")
                for tag in result["tags"]:
                    print(f"   - {tag['name']} (ID: {tag['id']})")
        else:
            print(f"❌ Failed to connect: {result.get('error')}")
            return False
    
    return True


async def publish_test_article():
    """Publish a test article to WordPress"""
    print("\n" + "=" * 60)
    print("Publishing Test Article")
    print("=" * 60)
    
    # Create test content
    title = f"Test Article - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    content = """
<h2>This is a Test Article</h2>
<p>This article was automatically generated and published by the Blog Poster API.</p>

<h3>Features Tested</h3>
<ul>
    <li>Basic Authentication with JSON Basic Auth plugin</li>
    <li>Creating posts via REST API</li>
    <li>Setting post status (draft)</li>
    <li>Generating URL slugs</li>
</ul>

<h3>Service Dog Information</h3>
<p>Service dogs are specially trained animals that provide assistance to people with disabilities. 
Under the Americans with Disabilities Act (ADA), service dogs are allowed to accompany their 
handlers in all public accommodations.</p>

<blockquote>
<p><strong>Note:</strong> This is a test post and will be saved as a draft for review.</p>
</blockquote>
"""
    
    # Publish via API
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{API_URL}/publish/wp",
            params={
                "title": title,
                "content": content,
                "status": "draft",
                "slug": "test-article-" + datetime.now().strftime("%Y%m%d-%H%M"),
                "meta_title": "Test Article - SEO Title",
                "meta_description": "This is a test article to verify WordPress publishing functionality"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print(f"✅ Article published successfully!")
                print(f"\n📝 Post Details:")
                print(f"   Post ID: {result['post_id']}")
                print(f"   Status: {result['status']}")
                print(f"   Slug: {result['slug']}")
                print(f"\n🔗 Links:")
                print(f"   Edit: {result['edit_link']}")
                print(f"   Preview: {result['preview_link']}")
                print(f"\n✨ Next Steps:")
                print(f"   1. Click the edit link above to review in WordPress admin")
                print(f"   2. Make any necessary edits")
                print(f"   3. Publish when ready")
                return True
            else:
                print(f"❌ Publishing failed: {result.get('error')}")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False


async def main():
    """Run all tests"""
    print("\n🚀 WordPress Publishing Test Suite")
    print("=" * 60)
    
    # Test connection
    connected = await test_wordpress_connection()
    if not connected:
        print("\n⚠️  Cannot proceed without WordPress connection")
        return
    
    # Ask user if they want to publish a test article
    print("\n" + "=" * 60)
    response = input("Do you want to publish a test article? (y/n): ")
    
    if response.lower() == 'y':
        success = await publish_test_article()
        
        if success:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed. Check the logs above.")
    else:
        print("Skipping article publication test.")
    
    print("\n" + "=" * 60)
    print("Test suite complete!")


if __name__ == "__main__":
    asyncio.run(main())