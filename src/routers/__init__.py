"""
FastAPI routers for the Blog Poster application
"""
from .health import router as health_router
from .articles import router as articles_router
from .wordpress import router as wordpress_router
from .competitors import router as competitors_router
from .topics import router as topics_router
from .pipeline import router as pipeline_router
from .vector import router as vector_router
from .seo import router as seo_router
from .dashboard import router as dashboard_router
from .profile import router as profile_router

__all__ = [
    "health_router",
    "articles_router",
    "wordpress_router",
    "competitors_router", 
    "topics_router",
    "pipeline_router",
    "vector_router",
    "seo_router",
    "dashboard_router",
    "profile_router"
]