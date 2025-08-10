"""
FastAPI Tool Shim + WPGraphQL Publishing Agent

This module adds a WordPress Publishing endpoint to the existing FastAPI shim.
It converts Markdown+frontmatter to HTML, uploads a featured image, maps
categories/tags to term IDs, creates/updates posts (idempotent on slug),
optionally schedules publication, writes SEO fields (RankMath/Yoast when
available), and finally pings the sitemap and IndexNow.

Usage (compose): the `docker-compose.yml` runs an `api` service exposing
http://localhost:8088. Drop this file next to `app.py` and either import the
router there or run this as a standalone app.

Env required:
  WORDPRESS_URL=https://example.com
  WP_AUTH_TOKEN=...               # JWT or Application Passwords (Bearer)
  WP_SITEMAP_URL=                 # optional; fallback tries /wp-sitemap.xml and /sitemap.xml
  WP_SITE_TZ=America/New_York     # site timezone for local scheduling -> GMT
  INDEXNOW_KEY=                   # optional key
  INDEXNOW_ENDPOINT=https://api.indexnow.org/indexnow

Add to requirements.txt:
  requests
  pydantic
  fastapi
  uvicorn[standard]
  python-dateutil
  pytz
  markdown
"""
from __future__ import annotations

import base64
import io
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from dateutil import parser as dateparser
import pytz
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from markdown import markdown as md_to_html

# ------------------------------
# Pydantic models for publish API
# ------------------------------

class PublishFrontmatter(BaseModel):
    title: str
    slug: str
    category: str
    tags: List[str] = []
    meta_title: str
    meta_desc: str
    canonical: HttpUrl
    schema_jsonld: Dict[str, Any] = {}
    hero_image_prompt: Optional[str] = None  # informational only
    internal_link_targets: List[HttpUrl] = []
    citations: List[HttpUrl] = []
    # Optional direct category/tag IDs if you already resolved them
    category_id: Optional[str] = None  # WPGraphQL global ID preferred
    tag_ids: List[str] = []            # WPGraphQL global IDs preferred

class PublishRequest(BaseModel):
    frontmatter: PublishFrontmatter
    markdown: str
    # Optional image inputs
    hero_image_url: Optional[HttpUrl] = None
    hero_image_base64: Optional[str] = None  # data without data: prefix
    hero_image_filename: Optional[str] = "hero.jpg"
    # Scheduling
    status: str = Field("DRAFT", description="DRAFT|PUBLISH|FUTURE")
    schedule_local: Optional[str] = Field(
        None,
        description="ISO datetime in site local timezone when scheduling (e.g., 2025-08-12T09:00:00)",
    )
    site_timezone: Optional[str] = None  # if not provided, uses WP_SITE_TZ env
    # SEO plugin fields (shape depends on plugin; pass-through)
    seo: Optional[Dict[str, Any]] = None

class PublishResponse(BaseModel):
    status: str
    post: Optional[Dict[str, Any]] = None
    media: Optional[Dict[str, Any]] = None
    pinged: Dict[str, bool] = {}

# ------------------------------
# WP GraphQL / REST client
# ------------------------------

class WpGraphQLClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")
        self.gql = f"{self.base}/graphql"
        self.rest_media = f"{self.base}/wp-json/wp/v2/media"
        self.verify_ssl = os.getenv("WP_VERIFY_SSL", "true").lower() not in ("0", "false", "no")

        # Build auth headers from env: prefer Bearer token, else Basic (Application Password)
        token = os.getenv("WP_AUTH_TOKEN")
        username = os.getenv("WP_USERNAME")
        app_password = os.getenv("WP_APP_PASSWORD")
        wp_password = os.getenv("WORDPRESS_ADMIN_PASSWORD")

        auth_header: Dict[str, str] = {}
        if token:
            auth_header = {"Authorization": f"Bearer {token}"}
        elif username and wp_password:
            # Attempt JWT login via WPGraphQL Authentication (if installed)
            try:
                r = requests.post(
                    f"{self.base}/graphql",
                    headers={"Content-Type": "application/json"},
                    json={
                        "query": "mutation($u:String!,$p:String!){ login(input:{username:$u,password:$p}){ authToken refreshToken }}",
                        "variables": {"u": username, "p": wp_password},
                    },
                    verify=self.verify_ssl,
                    timeout=20,
                )
                r.raise_for_status()
                data = r.json().get("data", {})
                jwt = data.get("login", {}).get("authToken")
                if jwt:
                    auth_header = {"Authorization": f"Bearer {jwt}"}
            except Exception:
                pass
        if not auth_header and username and app_password:
            basic = base64.b64encode(f"{username}:{app_password}".encode()).decode()
            auth_header = {"Authorization": f"Basic {basic}"}
        if not auth_header:
            raise HTTPException(400, "Authentication required: set WP_AUTH_TOKEN or WP_USERNAME and WORDPRESS_ADMIN_PASSWORD or WP_APP_PASSWORD")

        self.headers = {"Content-Type": "application/json", **auth_header}

    def _gql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        r = requests.post(
            self.gql,
            headers=self.headers,
            json={"query": query, "variables": variables or {}},
            verify=self.verify_ssl,
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        if "errors" in data:
            raise HTTPException(400, detail=data["errors"])
        return data["data"]

    def get_post_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        q = """
        query($slug: ID!){
          post(id: $slug, idType: SLUG){ id databaseId slug status featuredImageId uri }
        }
        """
        d = self._gql(q, {"slug": slug})
        return d.get("post")

    def get_media_global_id(self, db_id: int) -> str:
        q = """
        query($id: ID!){ mediaItem(id:$id, idType:DATABASE_ID){ id sourceUrl } }
        """
        d = self._gql(q, {"id": db_id})
        mi = d.get("mediaItem")
        if not mi:
            raise HTTPException(400, detail="Media item not found after upload")
        return mi["id"]

    def upload_media(self, filename: str, content: bytes, mime: Optional[str] = None) -> Dict[str, Any]:
        headers = {k: v for k, v in self.headers.items() if k.lower() != "content-type"}
        files = {"file": (filename, content, mime or "application/octet-stream")}
        r = requests.post(self.rest_media, headers=headers, files=files, verify=self.verify_ssl, timeout=30)
        r.raise_for_status()
        media = r.json()  # contains numeric id
        media_global = self.get_media_global_id(media["id"])
        return {"dbId": media["id"], "globalId": media_global, "url": media.get("source_url") or media.get("sourceUrl")}

    def list_terms_map(self) -> Dict[str, Dict[str, str]]:
        """Fetch categories/tags and build name-> {id, databaseId} map for each taxonomy."""
        q = """
        query {
          categories(first: 1000){ nodes { id databaseId name slug } }
          tags(first: 1000){ nodes { id databaseId name slug } }
        }
        """
        d = self._gql(q)
        cat = {n["name"]: {"id": n["id"], "dbId": n["databaseId"], "slug": n["slug"]} for n in d["categories"]["nodes"]}
        tag = {n["name"]: {"id": n["id"], "dbId": n["databaseId"], "slug": n["slug"]} for n in d["tags"]["nodes"]}
        return {"categories": cat, "tags": tag}

    def create_or_update_post(
        self,
        *,
        front: PublishFrontmatter,
        html: str,
        seo: Optional[Dict[str, Any]] = None,
        media_global_id: Optional[str] = None,
        status: str = "DRAFT",
        date_gmt: Optional[str] = None,
        category_id: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        existing = self.get_post_by_slug(front.slug)
        input_base: Dict[str, Any] = {
            "clientMutationId": f"article-{front.slug}",
            "title": front.title,
            "content": html,
            "slug": front.slug,
            "status": status,
            "excerpt": front.meta_desc,
        }
        if date_gmt and status.upper() == "FUTURE":
            input_base["dateGmt"] = date_gmt
        if media_global_id:
            input_base["featuredImageId"] = media_global_id
        if category_id:
            input_base["categories"] = {"connect": [{"id": category_id}]}
        if tag_ids:
            input_base["tags"] = {"connect": [{"id": t} for t in tag_ids]}
        if seo:
            # Pass-through: only works if RankMath/Yoast WPGraphQL extension is installed
            input_base.update(seo)

        if existing:
            mutation = """
            mutation($input: UpdatePostInput!){
              updatePost(input:$input){ post{ id databaseId slug status dateGmt featuredImageId uri } }
            }
            """
            input_base["id"] = existing["id"]
        else:
            mutation = """
            mutation($input: CreatePostInput!){
              createPost(input:$input){ post{ id databaseId slug status dateGmt featuredImageId uri } }
            }
            """
        data = self._gql(mutation, {"input": input_base})
        return data.get("updatePost", data.get("createPost", {}))

# ------------------------------
# Helpers
# ------------------------------

def to_gmt_str(local_dt_str: str, site_tz: str) -> str:
    tz = pytz.timezone(site_tz)
    dt = dateparser.parse(local_dt_str)
    if dt.tzinfo is None:
        dt = tz.localize(dt)
    dt_gmt = dt.astimezone(pytz.UTC)
    return dt_gmt.strftime("%Y-%m-%dT%H:%M:%SZ")


def convert_markdown_to_html(markdown_text: str) -> str:
    # Basic Markdown -> HTML. You can extend with extensions as needed.
    return md_to_html(markdown_text, extensions=["extra", "sane_lists", "toc"])  # type: ignore


def ping_sitemaps(base_url: str, override: Optional[str] = None, verify: bool = True) -> Dict[str, bool]:
    tried = []
    ok = {}
    urls = [override] if override else []
    urls += [f"{base_url.rstrip('/')}/wp-sitemap.xml", f"{base_url.rstrip('/')}/sitemap.xml"]
    for u in urls:
        try:
            r = requests.get(u, timeout=10, verify=verify)
            ok[u] = r.ok
            tried.append(u)
            if r.ok:
                break
        except Exception:
            ok[u] = False
    if not ok:
        ok["none"] = False
    return ok


def indexnow_submit(endpoint: str, key: str, site: str, urls: List[str]) -> bool:
    try:
        payload = {
            "host": site.replace("https://", "").replace("http://", "").rstrip("/"),
            "key": key,
            "keyLocation": f"{site.rstrip('/')}/{key}.txt",
            "urlList": urls,
        }
        r = requests.post(endpoint, json=payload, timeout=10)
        return r.ok
    except Exception:
        return False

# ------------------------------
# Router and endpoint
# ------------------------------

router = APIRouter(prefix="/publish", tags=["publish"])

@router.post("/wp", response_model=PublishResponse)
def publish_to_wordpress(req: PublishRequest):
    # Prefer Docker internal URL if provided, else external
    wp_url = os.getenv("WORDPRESS_LOCAL_URL") or os.getenv("WORDPRESS_URL") or "https://localhost:8445"
    client = WpGraphQLClient(base_url=wp_url)

    # 1) Convert Markdown -> HTML
    html = convert_markdown_to_html(req.markdown)

    # 2) Upload hero image (if provided)
    media_info: Optional[Dict[str, Any]] = None
    if req.hero_image_base64:
        try:
            content = base64.b64decode(req.hero_image_base64)
            media_info = client.upload_media(req.hero_image_filename or "hero.jpg", content)
        except Exception as e:
            raise HTTPException(400, f"Invalid hero_image_base64: {e}")
    elif req.hero_image_url:
        # Remote images typically have valid SSL; allow override via WP_VERIFY_SSL for local sources
        verify_ssl = os.getenv("WP_VERIFY_SSL", "true").lower() not in ("0", "false", "no")
        r = requests.get(str(req.hero_image_url), timeout=20, verify=verify_ssl)
        r.raise_for_status()
        content = r.content
        filename = req.hero_image_filename or os.path.basename(req.hero_image_url.path)
        media_info = client.upload_media(filename, content)

    media_gid = media_info.get("globalId") if media_info else None

    # 3) Map categories/tags
    category_id = req.frontmatter.category_id
    tag_ids = req.frontmatter.tag_ids or []
    if not category_id or not tag_ids:
        term_map = client.list_terms_map()
        if not category_id:
            cat = term_map["categories"].get(req.frontmatter.category)
            if not cat:
                raise HTTPException(400, f"Unknown category name: {req.frontmatter.category}")
            category_id = cat["id"]
        if not tag_ids and req.frontmatter.tags:
            for tname in req.frontmatter.tags:
                t = term_map["tags"].get(tname)
                if t:
                    tag_ids.append(t["id"])

    # 4) Scheduling
    status = req.status.upper()
    date_gmt: Optional[str] = None
    if status == "FUTURE":
        site_tz = req.site_timezone or os.getenv("WP_SITE_TZ", "UTC")
        if not req.schedule_local:
            raise HTTPException(400, "schedule_local is required when status=FUTURE")
        date_gmt = to_gmt_str(req.schedule_local, site_tz)

    # 5) Create/Update post (idempotent on slug)
    mutation_res = client.create_or_update_post(
        front=req.frontmatter,
        html=html,
        seo=req.seo,
        media_global_id=media_gid,
        status=status,
        date_gmt=date_gmt,
        category_id=category_id,
        tag_ids=tag_ids or None,
    )
    post = mutation_res.get("post") if mutation_res else None

    # 6) Post-publish pings (sitemap + IndexNow)
    ping_results: Dict[str, bool] = {}
    site = wp_url
    ping_results.update(ping_sitemaps(site, os.getenv("WP_SITEMAP_URL"), verify=client.verify_ssl))
    idx_ok = False
    if os.getenv("INDEXNOW_KEY"):
        idx_ok = indexnow_submit(
            endpoint=os.getenv("INDEXNOW_ENDPOINT", "https://api.indexnow.org/indexnow"),
            key=os.getenv("INDEXNOW_KEY"),
            site=site,
            urls=[post["uri"] and f"{site.rstrip('/')}{post['uri']}" ] if post and post.get("uri") else [str(req.frontmatter.canonical)],
        )
    ping_results["indexnow"] = idx_ok

    return PublishResponse(status="ok", post=post, media=media_info, pinged=ping_results)

# ------------------------------
# Optional standalone app (so this file can run by itself for quick tests)
# ------------------------------

if __name__ == "__main__":
    app = FastAPI(title="WPGraphQL Publisher")
    app.include_router(router)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
