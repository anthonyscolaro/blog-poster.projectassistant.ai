"""
WordPress publishing endpoints
"""
import logging
from typing import List, Optional, Literal
from fastapi import APIRouter

from src.services.wordpress_publisher import WordPressPublisher

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/publish", tags=["wordpress"])


@router.post("/wp")
async def publish_to_wordpress(
    title: str,
    content: str,
    status: Literal["draft", "publish"] = "draft",
    slug: Optional[str] = None,
    category_name: Optional[str] = None,
    categories: Optional[List[int]] = None,
    tags: Optional[List[int]] = None,
    meta_title: Optional[str] = None,
    meta_description: Optional[str] = None
):
    """
    Publish an article to WordPress
    
    Args:
        title: Article title
        content: Article content (HTML or Markdown)
        status: Post status (draft or publish)
        slug: URL slug
        categories: List of category IDs
        tags: List of tag IDs
        meta_title: SEO meta title
        meta_description: SEO meta description
    """
    # Get active configuration profile
    try:
        from src.config.config_profiles import get_profile_manager
        manager = get_profile_manager()
        active_profile = manager.get_active_profile()
        
        if active_profile and active_profile.wordpress:
            # Use configuration from active profile
            publisher = WordPressPublisher(
                wp_url=active_profile.wordpress.url,
                username=active_profile.wordpress.username,
                password=active_profile.wordpress.password,
                auth_method=active_profile.wordpress.auth_method,
                verify_ssl=active_profile.wordpress.verify_ssl
            )
        else:
            # Fallback to environment variables
            publisher = WordPressPublisher()
    except Exception as e:
        logger.warning(f"Could not load active profile, using environment variables: {e}")
        publisher = WordPressPublisher()
    
    # Test connection first
    connected = await publisher.test_connection()
    if not connected:
        return {
            "success": False,
            "error": "Failed to connect to WordPress. Check credentials and URL."
        }
    
    # Handle category mapping if not provided but category_name is given
    if not categories and category_name:
        try:
            # Get all WordPress categories
            wp_categories = await publisher.get_categories()
            
            # Try to find exact match first
            category_id = None
            for cat in wp_categories:
                if cat['name'].lower() == category_name.lower():
                    category_id = cat['id']
                    break
            
            if category_id:
                categories = [category_id]
                logger.info(f"Mapped category '{category_name}' to WordPress category ID {category_id}")
            else:
                # Category doesn't exist - create it
                logger.info(f"Category '{category_name}' not found, will use default category")
                categories = []  # WordPress will use default category
        except Exception as e:
            logger.warning(f"Failed to map category '{category_name}': {e}")
            categories = []
    
    # Prepare meta fields if SEO data provided
    meta = {}
    if meta_title:
        meta["meta_title"] = meta_title
    if meta_description:
        meta["meta_description"] = meta_description
    
    # Create the post
    result = await publisher.create_post(
        title=title,
        content=content,
        status=status,
        slug=slug,
        categories=categories,
        tags=tags,
        meta=meta if meta else None
    )
    
    if result["success"]:
        logger.info(f"Successfully published post {result['post_id']}: {result['edit_link']}")
    else:
        logger.error(f"Failed to publish post: {result.get('error')}")
    
    return result


@router.get("/wp/test")
async def test_wordpress_connection():
    """Test WordPress connection and authentication"""
    publisher = WordPressPublisher()
    connected = await publisher.test_connection()
    
    if connected:
        # Get categories and tags for reference
        categories = await publisher.get_categories()
        tags = await publisher.get_tags()
        
        return {
            "connected": True,
            "wordpress_url": publisher.wordpress_url,
            "auth_method": publisher.auth_method,
            "is_local": publisher.is_local,
            "categories": [{"id": cat["id"], "name": cat["name"]} for cat in categories[:5]],
            "tags": [{"id": tag["id"], "name": tag["name"]} for tag in tags[:5]]
        }
    else:
        return {
            "connected": False,
            "error": "Failed to connect to WordPress",
            "wordpress_url": publisher.wordpress_url,
            "auth_method": publisher.auth_method
        }