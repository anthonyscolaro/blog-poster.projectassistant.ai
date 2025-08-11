"""
WordPress Publisher Module
Handles publishing to WordPress with environment-specific authentication
"""
import os
import base64
import httpx
import json
from typing import Dict, Optional, Any, Literal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WordPressPublisher:
    """
    Publishes content to WordPress using environment-appropriate authentication
    """
    
    def __init__(
        self, 
        wp_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_method: Optional[str] = None,
        verify_ssl: Optional[bool] = None
    ):
        # Use provided parameters or fall back to environment
        self.wordpress_url = wp_url or os.getenv("WORDPRESS_URL", "http://localhost:8084")
        self.auth_method = auth_method or os.getenv("WP_AUTH_METHOD", "basic")
        self.username = username or os.getenv("WP_USERNAME", "admin")
        self.password = password or os.getenv("WP_PASSWORD", os.getenv("WP_APP_PASSWORD", "admin123"))
        self.verify_ssl = verify_ssl if verify_ssl is not None else os.getenv("WP_VERIFY_SSL", "false").lower() == "true"
        
        # Determine if we're in local or production
        self.is_local = "localhost" in self.wordpress_url or "127.0.0.1" in self.wordpress_url
        
        # API endpoints - use pretty permalinks now that they're configured
        self.api_base = f"{self.wordpress_url}/wp-json/wp/v2"
        
        logger.info(f"WordPress Publisher initialized for {self.wordpress_url}")
        logger.info(f"Using {self.auth_method} authentication")
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers based on environment"""
        headers = {"Content-Type": "application/json"}
        
        if self.auth_method == "basic" or self.is_local:
            # Basic Authentication for local development
            credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            headers["Authorization"] = f"Basic {credentials}"
        elif self.auth_method == "application":
            # Application Password for production
            credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            headers["Authorization"] = f"Basic {credentials}"
        
        return headers
    
    async def test_connection(self) -> bool:
        """Test connection to WordPress API"""
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl) as client:
                response = await client.get(
                    f"{self.api_base}/posts?per_page=1",
                    headers=self._get_auth_headers()
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    async def create_post(
        self,
        title: str,
        content: str,
        status: Literal["draft", "publish"] = "draft",
        categories: Optional[list] = None,
        tags: Optional[list] = None,
        meta: Optional[Dict[str, Any]] = None,
        slug: Optional[str] = None,
        is_markdown: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new WordPress post
        
        Args:
            title: Post title
            content: Post content (Markdown or HTML)
            status: Post status (draft or publish)
            categories: List of category IDs
            tags: List of tag IDs
            meta: Meta fields (SEO, etc.)
            slug: URL slug
            is_markdown: Whether content is in Markdown format (default: True)
            
        Returns:
            Dict with post details including ID and edit URL
        """
        # Convert markdown to WordPress blocks if needed
        if is_markdown:
            from ..utils.markdown_to_wp_blocks import markdown_to_wp_blocks
            _, content = markdown_to_wp_blocks(content, parse_frontmatter=False)
            logger.info("Converted markdown to WordPress blocks")
        
        # Prepare post data
        post_data = {
            "title": title,
            "content": content,
            "status": status,
            "slug": slug or self._generate_slug(title)
        }
        
        # Add categories and tags if provided
        if categories:
            post_data["categories"] = categories
        if tags:
            post_data["tags"] = tags
        
        # Add meta fields if provided (requires additional plugins)
        if meta:
            post_data["meta"] = meta
        
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl, timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_base}/posts",
                    headers=self._get_auth_headers(),
                    json=post_data
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    
                    # Build response with useful information
                    return {
                        "success": True,
                        "post_id": result.get("id"),
                        "slug": result.get("slug"),
                        "status": result.get("status"),
                        "link": result.get("link"),
                        "edit_link": f"{self.wordpress_url}/wp-admin/post.php?post={result.get('id')}&action=edit",
                        "preview_link": result.get("link") + "?preview=true" if status == "draft" else result.get("link"),
                        "created_at": result.get("date"),
                        "modified_at": result.get("modified")
                    }
                else:
                    error_msg = f"Failed to create post: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('message', '')}"
                    except:
                        error_msg += f" - {response.text[:200]}"
                    
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "status_code": response.status_code
                    }
                    
        except httpx.TimeoutException:
            error_msg = "Request timed out after 30 seconds"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    async def update_post(
        self,
        post_id: int,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing WordPress post"""
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl, timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_base}/posts/{post_id}",
                    headers=self._get_auth_headers(),
                    json=updates
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "post_id": result.get("id"),
                        "link": result.get("link"),
                        "edit_link": f"{self.wordpress_url}/wp-admin/post.php?post={result.get('id')}&action=edit"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to update post: {response.status_code}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_categories(self) -> list:
        """Get all categories from WordPress"""
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl) as client:
                response = await client.get(
                    f"{self.api_base}/categories?per_page=100",
                    headers=self._get_auth_headers()
                )
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []
    
    async def get_tags(self) -> list:
        """Get all tags from WordPress"""
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl) as client:
                response = await client.get(
                    f"{self.api_base}/tags?per_page=100",
                    headers=self._get_auth_headers()
                )
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            logger.error(f"Failed to get tags: {e}")
            return []
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')[:50]  # Limit length