"""
FastAPI application for Blog Poster - Modular Architecture

This is the main application file that orchestrates Claude 3.5 Sonnet with:
- Verifiable slot completion via <tool .../> tags
- Internal link resolver
- SEO lint checker
- Strong Pydantic contracts for inputs/outputs

Run:
  uvicorn app:app --reload --port 8088

Env (example):
  ANTHROPIC_API_KEY=...
  VECTOR_BACKEND=qdrant|convex|memory
  QDRANT_URL=http://localhost:6333
"""
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import all routers
from src.routers import (
    health_router,
    articles_router, 
    wordpress_router,
    competitors_router,
    topics_router,
    pipeline_router,
    vector_router,
    seo_router,
    dashboard_router,
    profile_router
)

# ------------------------------
# FastAPI App Setup
# ------------------------------
app = FastAPI(title="Blog Poster Dashboard", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all routers
app.include_router(health_router)
app.include_router(articles_router)
app.include_router(wordpress_router)
app.include_router(competitors_router)
app.include_router(topics_router)
app.include_router(pipeline_router)
app.include_router(vector_router)
app.include_router(seo_router)
app.include_router(profile_router)
app.include_router(dashboard_router)  # Include dashboard router last (handles root routes)

# Include external routers if available
try:
    # Include the WordPress publishing router providing /publish/wp
    from fast_api_tool_shim_pydantic_schemas_for_article_generation_agent_updated import (
        router as external_publish_router,
    )
    app.include_router(external_publish_router)
    logger.info("Included external WordPress publish router")
except Exception as e:
    logger.info(f"External WordPress router not available: {e}")

try:
    # Include configuration profile management API
    from src.config.config_api import router as config_router
    app.include_router(config_router)
    logger.info("Included config router")
except Exception as e:
    logger.info(f"Config router not available: {e}")

# ------------------------------
# Cleanup on shutdown
# ------------------------------
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down Blog Poster application")
    # Add any cleanup logic here

# ------------------------------
# Dev harness
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8088, reload=True)