#!/usr/bin/env python3
"""
Test WordPress Publishing - Automated Version
"""

import asyncio
import json
import os
from pathlib import Path

# Add the project root to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from wordpress_publisher import WordPressPublisher

async def test_publish():
    """Test publishing an article to WordPress"""
    
    print("=" * 60)
    print("WordPress Publishing Test (Automated)")
    print("=" * 60)
    
    # Initialize publisher
    publisher = WordPressPublisher()
    
    # Test connection first
    print("\n1. Testing WordPress connection...")
    connected = await publisher.test_connection()
    
    if not connected:
        print("❌ Failed to connect to WordPress")
        print(f"   URL: {publisher.wordpress_url}")
        print(f"   Username: {publisher.username}")
        print(f"   Checking configuration...")
        print(f"   WORDPRESS_URL: {os.getenv('WORDPRESS_URL')}")
        print(f"   WP_USERNAME: {os.getenv('WP_USERNAME')}")
        print(f"   WP_APP_PASSWORD: {'Set' if os.getenv('WP_APP_PASSWORD') else 'Not set'}")
        return
    
    print(f"✅ Connected to WordPress at {publisher.wordpress_url}")
    
    # Load a test article
    article_path = "data/articles/service-dog-training-essential-skills-requirements_20250811_080421.json"
    
    if not os.path.exists(article_path):
        print(f"❌ Article file not found: {article_path}")
        # Try to list available articles
        print("\nAvailable articles:")
        for f in os.listdir("data/articles"):
            if f.endswith(".json") and f != "null-20250810_214702.json":
                print(f"   - {f}")
        return
    
    print(f"\n2. Loading article from: {article_path}")
    
    with open(article_path, 'r') as f:
        article_data = json.load(f)
    
    print(f"   Title: {article_data.get('title', 'No title')}")
    print(f"   Word Count: {article_data.get('word_count', 0)}")
    
    # Prepare content for publishing
    print("\n3. Preparing content for WordPress...")
    
    # Create a test post data structure
    post_data = {
        "title": "[TEST] " + article_data.get("title", "Test Article"),
        "content": article_data.get("content_markdown", ""),
        "meta_title": article_data.get("meta_title", ""),
        "meta_description": article_data.get("meta_description", ""),
        "primary_keyword": article_data.get("primary_keyword", ""),
        "secondary_keywords": article_data.get("secondary_keywords", []),
        # Note: Categories and tags need IDs, not names - leaving empty for now
        "tags": None,  
        "categories": None,
        "status": "draft"  # Publish as draft for safety
    }
    
    print("   Post will be published as DRAFT with [TEST] prefix")
    print("   Note: Categories and tags not set (requires ID lookup)")
    
    # Publish to WordPress
    print("\n4. Publishing to WordPress...")
    
    try:
        # Prepare meta data for WordPress
        meta_data = {
            "meta_description": post_data["meta_description"],
            "primary_keyword": post_data["primary_keyword"],
            "secondary_keywords": ", ".join(post_data["secondary_keywords"]) if post_data["secondary_keywords"] else ""
        }
        
        result = await publisher.create_post(
            title=post_data["title"],
            content=post_data["content"],
            status=post_data["status"],
            tags=post_data["tags"],
            categories=post_data["categories"],
            meta=meta_data
        )
        
        if result and result.get("success"):
            print(f"\n✅ Successfully published to WordPress!")
            print(f"   Post ID: {result.get('post_id')}")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   URL: {result.get('link', 'No URL available')}")
            
            if result.get('status') == 'draft':
                print(f"\n   📝 Note: Article published as DRAFT")
                print(f"   Log into WordPress to review and publish: {publisher.wordpress_url}/wp-admin")
                print(f"   Username: {publisher.username}")
        else:
            print(f"❌ Failed to publish article")
            print(f"   Result: {result}")
            
    except Exception as e:
        print(f"❌ Error publishing article: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_publish())