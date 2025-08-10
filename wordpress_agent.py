"""
WordPress Publishing Agent
Handles publishing articles to WordPress via WPGraphQL and REST API
"""
import os
import asyncio
import httpx
import json
from typing import Dict, Optional, List, Literal, Any
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, HttpUrl
from gql import gql, Client
from gql.transport.httpx import HTTPXAsyncTransport
import logging

logger = logging.getLogger(__name__)

# Import from app.py if needed
try:
    from app import ArticleDraft, FactCheckOutput
except ImportError:
    # Define minimal versions for standalone use
    class ArticleDraft(BaseModel):
        title: str
        slug: str
        content_markdown: str
        content_html: str
        meta_title: str
        meta_desc: str
        canonical: HttpUrl
        tags: List[str]
        category: str
        hero_image_prompt: str
        internal_link_targets: List[HttpUrl]
        citations: List[HttpUrl]
        jurisdiction: str
        
    class FactCheckOutput(BaseModel):
        verified: bool
        confidence_score: float


class WordPressConfig(BaseModel):
    """WordPress site configuration"""
    site_url: HttpUrl
    graphql_endpoint: str = "/graphql"
    rest_endpoint: str = "/wp-json/wp/v2"
    timezone: str = "America/New_York"
    category_map: Dict[str, int] = {}
    jwt_token: Optional[str] = None
    refresh_token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    indexnow_key: Optional[str] = None
    cdn_config: Optional[Dict[str, Any]] = None
    social_config: Optional[Dict[str, Any]] = None


class MediaUploadResult(BaseModel):
    """Result from WP REST API media upload"""
    id: int
    source_url: HttpUrl
    media_type: str
    alt_text: str
    caption: Optional[str]


class WordPressPost(BaseModel):
    """WordPress post data from GraphQL"""
    id: str  # GraphQL ID
    databaseId: int
    slug: str
    uri: str
    link: HttpUrl
    status: str
    modified: datetime


class SEOFields(BaseModel):
    """RankMath/Yoast SEO fields"""
    metaTitle: str
    metaDescription: str
    focusKeyword: str
    canonicalUrl: HttpUrl
    schemaMarkup: Optional[Dict[str, Any]] = None
    ogTitle: Optional[str] = None
    ogDescription: Optional[str] = None
    ogImage: Optional[HttpUrl] = None


class PublishingInput(BaseModel):
    article: ArticleDraft
    fact_check_result: FactCheckOutput
    status: Literal["draft", "pending", "publish", "future"] = "draft"
    scheduled_gmt: Optional[datetime] = None
    featured_image_path: Optional[str] = None
    external_id: str
    force_update: bool = False


class PublishingOutput(BaseModel):
    post: WordPressPost
    media: Optional[MediaUploadResult] = None
    seo_fields_set: bool = False
    categories_set: List[int] = []
    tags_set: List[str] = []
    sitemap_pinged: bool = False
    indexnow_submitted: bool = False
    cache_invalidated: bool = False
    operation: Literal["created", "updated", "skipped"]


class WordPressPublishingAgent:
    """Handles article publishing to WordPress"""
    
    def __init__(self, config: WordPressConfig):
        self.config = config
        self.graphql_client = None
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self._setup_graphql()
    
    def _setup_graphql(self):
        """Initialize GraphQL client"""
        transport = HTTPXAsyncTransport(
            url=f"{self.config.site_url}{self.config.graphql_endpoint}",
            headers={"Authorization": f"Bearer {self.config.jwt_token}"} if self.config.jwt_token else {}
        )
        self.graphql_client = Client(transport=transport, fetch_schema_from_transport=False)
    
    async def authenticate(self) -> str:
        """Get JWT token from WordPress"""
        if self.config.jwt_token:
            return self.config.jwt_token
            
        mutation = gql("""
            mutation Login($username: String!, $password: String!) {
                login(input: {username: $username, password: $password}) {
                    authToken
                    refreshToken
                    user {
                        id
                        name
                    }
                }
            }
        """)
        
        result = await self.graphql_client.execute_async(
            mutation,
            variable_values={
                "username": self.config.username,
                "password": self.config.password
            }
        )
        
        self.config.jwt_token = result["login"]["authToken"]
        self.config.refresh_token = result["login"]["refreshToken"]
        
        # Update GraphQL client with auth token
        self._setup_graphql()
        
        return self.config.jwt_token
    
    async def load_category_map(self):
        """Load category IDs from WordPress"""
        query = gql("""
            query GetCategories {
                categories(first: 100) {
                    nodes {
                        databaseId
                        name
                        slug
                    }
                }
            }
        """)
        
        result = await self.graphql_client.execute_async(query)
        
        # Build category map
        for category in result["categories"]["nodes"]:
            self.config.category_map[category["name"]] = category["databaseId"]
        
        logger.info(f"Loaded {len(self.config.category_map)} categories")
        return self.config.category_map
    
    async def get_post_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Check if post exists by slug"""
        query = gql("""
            query GetPostBySlug($slug: String!) {
                post(id: $slug, idType: SLUG) {
                    id
                    databaseId
                    slug
                    uri
                    link
                    status
                    modified
                    meta {
                        external_id
                    }
                }
            }
        """)
        
        try:
            result = await self.graphql_client.execute_async(
                query,
                variable_values={"slug": slug}
            )
            return result.get("post")
        except Exception as e:
            logger.error(f"Error checking post existence: {e}")
            return None
    
    async def upload_media(self, file_path: str, alt_text: str) -> MediaUploadResult:
        """Upload media via WP REST API"""
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Media file not found: {file_path}")
        
        # Prepare multipart upload
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'image/jpeg')}
            data = {
                'alt_text': alt_text,
                'caption': f"Featured image for article"
            }
            
            headers = {}
            if self.config.jwt_token:
                headers['Authorization'] = f'Bearer {self.config.jwt_token}'
            
            # Upload to REST API
            response = await self.http_client.post(
                f"{self.config.site_url}{self.config.rest_endpoint}/media",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code != 201:
                raise Exception(f"Media upload failed: {response.text}")
            
            media_data = response.json()
            
            return MediaUploadResult(
                id=media_data["id"],
                source_url=media_data["source_url"],
                media_type=media_data["media_type"],
                alt_text=media_data.get("alt_text", ""),
                caption=media_data.get("caption", {}).get("rendered", "")
            )
    
    async def create_post(self, input: PublishingInput, media_id: Optional[int] = None) -> WordPressPost:
        """Create new WordPress post"""
        
        # Convert markdown to HTML if needed
        content = input.article.content_html or input.article.content_markdown
        
        # Build GraphQL mutation input
        post_input = {
            "title": input.article.title,
            "slug": input.article.slug,
            "content": content,
            "excerpt": input.article.meta_desc,
            "status": input.status.upper(),
        }
        
        # Add featured image if uploaded
        if media_id:
            post_input["featuredImageId"] = media_id
        
        # Set categories
        category_id = self.config.category_map.get(input.article.category)
        if category_id:
            post_input["categories"] = {"nodes": [{"id": category_id}]}
        
        # Set tags
        if input.article.tags:
            post_input["tags"] = {"nodes": [{"name": tag} for tag in input.article.tags]}
        
        # Schedule if future post
        if input.scheduled_gmt and input.status == "future":
            post_input["date"] = input.scheduled_gmt.isoformat()
        
        mutation = gql("""
            mutation CreatePost($input: CreatePostInput!) {
                createPost(input: $input) {
                    post {
                        id
                        databaseId
                        slug
                        uri
                        link
                        status
                        modified
                    }
                }
            }
        """)
        
        result = await self.graphql_client.execute_async(
            mutation,
            variable_values={"input": post_input}
        )
        
        post_data = result["createPost"]["post"]
        
        # Set external ID as post meta
        await self.set_post_meta(post_data["databaseId"], "external_id", input.external_id)
        
        return WordPressPost(**post_data)
    
    async def update_post(self, post_id: str, input: PublishingInput, media_id: Optional[int] = None) -> WordPressPost:
        """Update existing WordPress post"""
        
        content = input.article.content_html or input.article.content_markdown
        
        update_input = {
            "id": post_id,
            "title": input.article.title,
            "content": content,
            "excerpt": input.article.meta_desc,
            "status": input.status.upper(),
        }
        
        if media_id:
            update_input["featuredImageId"] = media_id
        
        mutation = gql("""
            mutation UpdatePost($input: UpdatePostInput!) {
                updatePost(input: $input) {
                    post {
                        id
                        databaseId
                        slug
                        uri
                        link
                        status
                        modified
                    }
                }
            }
        """)
        
        result = await self.graphql_client.execute_async(
            mutation,
            variable_values={"input": update_input}
        )
        
        return WordPressPost(**result["updatePost"]["post"])
    
    async def set_seo_fields(self, post_id: str, article: ArticleDraft) -> bool:
        """Set RankMath/Yoast SEO fields"""
        
        try:
            # This requires WPGraphQL for RankMath/Yoast to be installed
            mutation = gql("""
                mutation UpdateSEOFields($id: ID!, $seo: SEOInput!) {
                    updatePostSEO(input: {id: $id, seo: $seo}) {
                        post {
                            seo {
                                metaTitle
                                metaDescription
                                focusKeyword
                            }
                        }
                    }
                }
            """)
            
            seo_input = {
                "metaTitle": article.meta_title,
                "metaDescription": article.meta_desc,
                "focusKeyword": article.tags[0] if article.tags else "",
                "canonicalUrl": str(article.canonical)
            }
            
            await self.graphql_client.execute_async(
                mutation,
                variable_values={"id": post_id, "seo": seo_input}
            )
            
            return True
        except Exception as e:
            logger.warning(f"SEO fields update failed (plugin may not be installed): {e}")
            return False
    
    async def set_post_meta(self, post_id: int, key: str, value: str) -> bool:
        """Set post meta via REST API"""
        
        try:
            headers = {}
            if self.config.jwt_token:
                headers['Authorization'] = f'Bearer {self.config.jwt_token}'
            
            response = await self.http_client.post(
                f"{self.config.site_url}{self.config.rest_endpoint}/posts/{post_id}",
                json={"meta": {key: value}},
                headers=headers
            )
            
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to set post meta: {e}")
            return False
    
    async def ping_sitemap(self, sitemap_url: str):
        """Ping Google/Bing about sitemap update"""
        
        services = [
            f"https://www.google.com/ping?sitemap={sitemap_url}",
            f"https://www.bing.com/ping?sitemap={sitemap_url}"
        ]
        
        for service in services:
            try:
                await self.http_client.get(service)
                logger.info(f"Pinged sitemap to {service}")
            except Exception as e:
                logger.warning(f"Sitemap ping failed for {service}: {e}")
    
    async def submit_indexnow(self, url: str):
        """Submit URL to IndexNow for instant indexing"""
        
        if not self.config.indexnow_key:
            return False
        
        try:
            payload = {
                "host": str(self.config.site_url).replace("https://", "").replace("http://", ""),
                "key": self.config.indexnow_key,
                "urlList": [str(url)]
            }
            
            response = await self.http_client.post(
                "https://api.indexnow.org/indexnow",
                json=payload
            )
            
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"IndexNow submission failed: {e}")
            return False
    
    async def invalidate_cache(self, url: str):
        """Invalidate CDN cache for URL"""
        
        if not self.config.cdn_config:
            return False
        
        # Implementation depends on CDN provider
        # Example for Cloudflare:
        if self.config.cdn_config.get("provider") == "cloudflare":
            try:
                zone_id = self.config.cdn_config.get("zone_id")
                api_token = self.config.cdn_config.get("api_token")
                
                response = await self.http_client.post(
                    f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
                    json={"files": [str(url)]},
                    headers={"Authorization": f"Bearer {api_token}"}
                )
                
                return response.status_code == 200
            except Exception as e:
                logger.warning(f"Cache invalidation failed: {e}")
        
        return False
    
    async def post_publish_actions(self, post_url: str):
        """Execute post-publish automation"""
        
        # Ping sitemap
        sitemap_url = f"{self.config.site_url}/sitemap.xml"
        await self.ping_sitemap(sitemap_url)
        
        # Submit to IndexNow
        if self.config.indexnow_key:
            await self.submit_indexnow(post_url)
        
        # Invalidate CDN cache
        if self.config.cdn_config:
            await self.invalidate_cache(post_url)
    
    async def publish(self, input: PublishingInput) -> PublishingOutput:
        """Main publish method with idempotency"""
        
        # Ensure authenticated
        if not self.config.jwt_token:
            await self.authenticate()
        
        # Ensure categories loaded
        if not self.config.category_map:
            await self.load_category_map()
        
        # Check if post exists
        existing = await self.get_post_by_slug(input.article.slug)
        
        if existing and not input.force_update:
            # Check if same source
            if existing.get("meta", {}).get("external_id") == input.external_id:
                return PublishingOutput(
                    post=WordPressPost(**existing),
                    operation="skipped"
                )
        
        # Upload featured image if provided
        media = None
        media_id = None
        if input.featured_image_path:
            try:
                media = await self.upload_media(
                    input.featured_image_path,
                    input.article.hero_image_prompt
                )
                media_id = media.id
            except Exception as e:
                logger.error(f"Media upload failed: {e}")
        
        # Create or update post
        if existing:
            post = await self.update_post(existing["id"], input, media_id)
            operation = "updated"
        else:
            post = await self.create_post(input, media_id)
            operation = "created"
        
        # Set SEO fields
        seo_set = await self.set_seo_fields(post.id, input.article)
        
        # Post-publish actions
        sitemap_pinged = False
        indexnow_submitted = False
        cache_invalidated = False
        
        if input.status == "publish":
            await self.post_publish_actions(post.link)
            sitemap_pinged = True
            indexnow_submitted = bool(self.config.indexnow_key)
            cache_invalidated = bool(self.config.cdn_config)
        
        return PublishingOutput(
            post=post,
            media=media,
            seo_fields_set=seo_set,
            categories_set=[self.config.category_map.get(input.article.category, 0)],
            tags_set=input.article.tags,
            sitemap_pinged=sitemap_pinged,
            indexnow_submitted=indexnow_submitted,
            cache_invalidated=cache_invalidated,
            operation=operation
        )
    
    async def close(self):
        """Cleanup"""
        await self.http_client.aclose()


# Example usage
async def main():
    config = WordPressConfig(
        site_url="https://localhost:8445",
        username=os.getenv("WORDPRESS_ADMIN_USER", "admin"),
        password=os.getenv("WORDPRESS_ADMIN_PASSWORD", "admin123"),
        indexnow_key=os.getenv("INDEXNOW_KEY")
    )
    
    agent = WordPressPublishingAgent(config)
    
    try:
        # Authenticate
        await agent.authenticate()
        
        # Load categories
        await agent.load_category_map()
        
        # Example article
        article = ArticleDraft(
            title="Understanding ADA Service Dog Requirements",
            slug="ada-service-dog-requirements",
            content_markdown="# Understanding ADA Service Dog Requirements\n\nContent here...",
            content_html="<h1>Understanding ADA Service Dog Requirements</h1><p>Content here...</p>",
            meta_title="ADA Service Dog Requirements Guide",
            meta_desc="Learn about ADA requirements for service dogs, including training, registration, and public access rights.",
            canonical="https://servicedogus.org/ada-service-dog-requirements",
            tags=["ADA", "service dogs", "requirements"],
            category="ADA Compliance",
            hero_image_prompt="Service dog in vest helping handler",
            internal_link_targets=[],
            citations=["https://www.ada.gov/resources/service-animals-2010-requirements/"],
            jurisdiction="US-Federal"
        )
        
        fact_check = FactCheckOutput(
            verified=True,
            confidence_score=0.98
        )
        
        input = PublishingInput(
            article=article,
            fact_check_result=fact_check,
            status="draft",
            external_id="blog-agent-001"
        )
        
        # Publish
        result = await agent.publish(input)
        print(f"Published: {result.post.link} (Operation: {result.operation})")
        
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())