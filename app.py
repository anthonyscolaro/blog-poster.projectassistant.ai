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
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database on startup (required)
from src.database import init_database
try:
    init_database()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"FATAL: Database initialization failed: {e}")
    logger.error("Cannot start application without database connection")
    logger.error("Please ensure DATABASE_URL is set and PostgreSQL is running")
    sys.exit(1)

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
from src.routers.auth import router as auth_router

# ------------------------------
# FastAPI App Setup
# ------------------------------
app = FastAPI(title="Blog Poster Dashboard", version="2.0.0")

# Add CORS middleware - SECURITY: Restrict origins
ALLOWED_ORIGINS = [
    "https://servicedogus.com",
    "https://staging-wp.servicedogus.org", 
    "http://localhost:8084",  # Local WordPress
    "http://localhost:3000",  # Local development
    "http://localhost:8088",  # Local API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # FIXED: No more wildcards!
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

# Create directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all routers
app.include_router(auth_router)  # Authentication routes
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
# Startup and Shutdown Events
# ------------------------------
@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    logger.info("Starting Blog Poster application")
    
    # Verify database connection
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        logger.error("FATAL: DATABASE_URL environment variable not set")
        logger.error("Cannot start application without database connection")
        sys.exit(1)
    
    logger.info(f"Using PostgreSQL database: {db_url.split('@')[1] if '@' in db_url else 'configured'}")
    
    # Test database connection
    try:
        from src.database import test_connection
        if not test_connection():
            logger.error("FATAL: Database connection test failed")
            sys.exit(1)
        logger.info("Database connection verified")
    except Exception as e:
        logger.error(f"FATAL: Database connection test failed: {e}")
        sys.exit(1)

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down Blog Poster application")
    
    # Close database connections
    try:
        from src.database import engine
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.warning(f"Error closing database: {e}")

# ------------------------------
# Dev harness
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8088, reload=True)