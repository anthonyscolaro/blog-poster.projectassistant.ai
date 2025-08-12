"""
Dashboard web interface endpoints
"""
import os
import glob
import json as json_lib
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import markdown

from src.services.orchestration_manager import OrchestrationManager
from src.services.vector_search import VectorSearchManager
from src.services.pipeline_logger import pipeline_logger
from src.services.api_keys_manager import get_api_keys_manager
from src.routers.auth import get_current_user_optional, get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=["dashboard"])

# Setup templates
templates = Jinja2Templates(directory="templates")

# Add markdown filter for rendering content
def markdown_filter(text):
    """Convert markdown to HTML"""
    return markdown.markdown(text, extensions=['codehilite', 'fenced_code'])

templates.env.filters['markdown'] = markdown_filter

# Helper functions to get managers
def get_orchestration_manager():
    """Get orchestration manager instance"""
    try:
        return OrchestrationManager()
    except:
        return None

def get_vector_manager():
    """Get vector manager instance"""
    try:
        return VectorSearchManager()
    except:
        return None


@router.get("/", response_class=HTMLResponse)
async def root_handler(request: Request, current_user=Depends(get_current_user_optional)):
    """
    Root route handler - redirects to login or dashboard based on authentication
    """
    if current_user:
        # User is authenticated, redirect to dashboard
        return RedirectResponse("/dashboard", status_code=302)
    else:
        # User is not authenticated, redirect to login
        return RedirectResponse("/auth/login", status_code=302)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_home(request: Request, current_user=Depends(get_current_user)):
    """Main dashboard page - requires authentication"""
    try:
        # Get system status
        orchestration_status = get_orchestration_manager()
        vector_manager = get_vector_manager()
        
        # Get basic stats
        pipeline_stats = await orchestration_status.get_pipeline_stats() if orchestration_status else {}
        vector_stats = vector_manager.get_collection_stats() if vector_manager else {}
        
        context = {
            "request": request,
            "title": "Blog Poster Dashboard",
            "pipeline_stats": pipeline_stats,
            "vector_stats": vector_stats,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_user": current_user
        }
        
        return templates.TemplateResponse("dashboard.html", context)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/pipeline", response_class=HTMLResponse)
async def pipeline_dashboard(request: Request):
    """Pipeline monitoring page"""
    try:
        orchestration_status = get_orchestration_manager()
        logger.info(f"Got orchestration manager: {orchestration_status is not None}")
        
        # Get pipeline history using the working API method instead of dashboard method
        pipeline_history_api = orchestration_status.get_pipeline_history(20) if orchestration_status else []
        active_pipelines = await orchestration_status.get_active_pipelines() if orchestration_status else []
        logger.info(f"Pipeline history API returned: {len(pipeline_history_api)} items")
        logger.info(f"Active pipelines: {len(active_pipelines)} items")
        
        # Convert API format to dashboard format
        pipeline_history = []
        for i, result in enumerate(pipeline_history_api):
            pipeline_id = f"pipeline_{result.started_at.strftime('%Y%m%d%H%M%S')}_{i}"
            
            # Extract the primary keyword
            primary_keyword = "Unknown"
            if result.topic_recommendation and hasattr(result.topic_recommendation, 'primary_keyword'):
                primary_keyword = result.topic_recommendation.primary_keyword
            elif result.topic_recommendation and hasattr(result.topic_recommendation, 'topic'):
                primary_keyword = result.topic_recommendation.topic
            
            # Calculate time ago
            now = datetime.now()
            diff = now - result.started_at
            if diff.days > 0:
                time_ago = f"{diff.days} days ago"
            elif diff.seconds > 3600:
                time_ago = f"{diff.seconds // 3600} hours ago"
            elif diff.seconds > 60:
                time_ago = f"{diff.seconds // 60} minutes ago"
            else:
                time_ago = "Just now"
            
            # Find the correct article ID by looking for matching article file
            article_id = None
            if result.article:
                # Extract timestamp from pipeline_id (format: pipeline_YYYYMMDDHHMISS_X)
                timestamp_part = pipeline_id.replace("pipeline_", "").split("_")[0]
                if len(timestamp_part) == 14:  # YYYYMMDDHHMISS
                    formatted_timestamp = f"{timestamp_part[:8]}_{timestamp_part[8:]}"
                    
                    # Look for article files with matching timestamp
                    article_files = glob.glob("data/articles/*.json")
                    for file_path in article_files:
                        if formatted_timestamp in file_path:
                            # Extract article slug from filename
                            filename = os.path.basename(file_path)
                            article_id = filename.replace('.json', '')
                            break
                
                # Fallback to pipeline_id if no matching file found
                if not article_id:
                    article_id = pipeline_id

            pipeline_history.append({
                "pipeline_id": pipeline_id,
                "primary_keyword": primary_keyword,
                "started_at": result.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "time_ago": time_ago,
                "duration": result.execution_time if result.execution_time else None,
                "status": result.status.value,
                "cost": result.total_cost,
                "article_generated": bool(result.article),
                "article_id": article_id
            })
        
        context = {
            "request": request,
            "title": "Pipeline Monitor",
            "pipeline_history": pipeline_history[:20],  # Last 20 runs
            "active_pipelines": active_pipelines,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("pipeline.html", context)
    except Exception as e:
        logger.error(f"Pipeline dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/pipeline/{pipeline_id}/view", response_class=HTMLResponse)
async def view_pipeline_details(request: Request, pipeline_id: str):
    """View detailed pipeline execution results"""
    try:
        # Import the get_pipeline_details function from pipeline router
        from .pipeline import get_pipeline_details
        
        # Get pipeline details from API
        details = await get_pipeline_details(pipeline_id)
        
        # Find the correct article ID by looking for matching article file
        article_id = pipeline_id  # Default fallback
        if details.get("article"):
            # Extract timestamp from pipeline_id (format: pipeline_YYYYMMDDHHMISS_X)
            timestamp_part = pipeline_id.replace("pipeline_", "").split("_")[0]
            if len(timestamp_part) == 14:  # YYYYMMDDHHMISS
                formatted_timestamp = f"{timestamp_part[:8]}_{timestamp_part[8:]}"
                
                # Look for article files with matching timestamp
                article_files = glob.glob("data/articles/*.json")
                for file_path in article_files:
                    if formatted_timestamp in file_path:
                        # Extract article slug from filename
                        filename = os.path.basename(file_path)
                        article_id = filename.replace('.json', '')
                        break

        # Format the data for the template
        pipeline = {
            "pipeline_id": details["pipeline_id"],
            "status": details["status"],
            "started_at": details["started_at"],
            "completed_at": details["completed_at"],
            "execution_time": details["execution_time"],
            "total_cost": details["total_cost"],
            "primary_keyword": details["primary_keyword"],
            "article_id": article_id,
            "article": details.get("article"),
            "topic_recommendation": details.get("topic_recommendation"),
            "competitor_insights": details.get("competitor_insights"),
            "fact_check_report": details.get("fact_check_report"),
            "wordpress_result": details.get("wordpress_result"),
            "errors": details.get("errors", []),
            "warnings": details.get("warnings", [])
        }
        
        context = {
            "request": request,
            "title": f"Pipeline Details - {pipeline_id}",
            "pipeline": pipeline
        }
        
        return templates.TemplateResponse("pipeline-details.html", context)
    except HTTPException as e:
        if e.status_code == 404:
            return templates.TemplateResponse("error.html", {"request": request, "error": f"Pipeline {pipeline_id} not found"})
        raise
    except Exception as e:
        logger.error(f"Pipeline details error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/articles", response_class=HTMLResponse)
async def articles_dashboard(request: Request):
    """Article management page"""
    try:
        # Get recent articles from cache/database
        articles = []
        article_files = glob.glob("data/articles/*.json")
        article_files.sort(key=os.path.getmtime, reverse=True)
        
        for file_path in article_files[:50]:  # Last 50 articles
            try:
                with open(file_path, 'r') as f:
                    article_data = json_lib.load(f)
                    article_data['file_path'] = file_path
                    article_data['created_at'] = datetime.fromtimestamp(os.path.getmtime(file_path))
                    articles.append(article_data)
            except Exception:
                continue
        
        context = {
            "request": request,
            "title": "Article Management",
            "articles": articles,
            "total_articles": len(articles),
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("articles.html", context)
    except Exception as e:
        logger.error(f"Articles dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/articles/{article_id}", response_class=HTMLResponse)
async def article_detail(request: Request, article_id: str):
    """Individual article detail page"""
    try:
        # Try to find the article file
        article_data = None
        
        # Look for article by ID in filenames
        article_files = glob.glob("data/articles/*.json")
        for file_path in article_files:
            filename = os.path.basename(file_path).replace('.json', '')
            # Try exact match first, then partial match
            if article_id == filename or article_id in file_path:
                try:
                    with open(file_path, 'r') as f:
                        article_data = json_lib.load(f)
                        article_data['file_path'] = file_path
                        article_data['created_at'] = datetime.fromtimestamp(os.path.getmtime(file_path))
                        break
                except Exception:
                    continue
        
        if not article_data:
            # If not found, check if it's a current pipeline
            if article_id == "current_pipeline":
                manager = get_orchestration_manager()
                if manager and manager.current_pipeline and manager.current_pipeline.article:
                    article = manager.current_pipeline.article
                    article_data = {
                        "title": article.title,
                        "content_markdown": article.content_markdown,
                        "meta_title": article.meta_title,
                        "meta_description": article.meta_description,
                        "word_count": article.word_count,
                        "seo_score": article.seo_score,
                        "primary_keyword": article.primary_keyword,
                        "slug": article.slug,
                        "created_at": datetime.now(),
                        "status": "In Progress"
                    }
                else:
                    raise HTTPException(404, "Article not found")
            else:
                raise HTTPException(404, "Article not found")
        
        context = {
            "request": request,
            "title": f"Article: {article_data.get('title', 'Unknown')}",
            "article": article_data,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("article-detail.html", context)
    except Exception as e:
        logger.error(f"Article detail error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/health-dashboard", response_class=HTMLResponse)
async def health_dashboard(request: Request):
    """System health monitoring page"""
    try:
        # Check service health
        health_data = {
            "services": {},
            "environment": {},
            "metrics": {}
        }
        
        # Check orchestration manager
        try:
            orchestration_status = get_orchestration_manager()
            health_data["services"]["orchestration"] = "healthy" if orchestration_status else "down"
        except:
            health_data["services"]["orchestration"] = "error"
        
        # Check vector database
        try:
            vector_manager = get_vector_manager()
            collections = vector_manager.get_collection_stats() if vector_manager else {}
            health_data["services"]["qdrant"] = "healthy" if collections else "down"
            health_data["metrics"]["collections"] = collections
        except Exception as e:
            logger.error(f"Qdrant health check error: {e}")
            health_data["services"]["qdrant"] = "error"
            health_data["metrics"]["collections"] = {}
        
        # Check WordPress connection
        try:
            from src.services.wordpress_publisher import WordPressPublisher
            wp_publisher = WordPressPublisher()
            wp_health = await wp_publisher.health_check()
            health_data["services"]["wordpress"] = wp_health["status"]
            health_data["metrics"]["wordpress"] = wp_health
        except Exception as e:
            logger.error(f"WordPress health check error: {e}")
            health_data["services"]["wordpress"] = "error"
        
        # Check Bright Data
        health_data["services"]["bright_data"] = "healthy" if os.getenv("BRIGHT_DATA_API_KEY") else "unknown"
        
        # Check Jina AI
        health_data["services"]["jina"] = "healthy" if os.getenv("JINA_API_KEY") else "unknown"
        
        # Environment info
        health_data["environment"] = {
            "anthropic_key": "✓" if os.getenv("ANTHROPIC_API_KEY") else "✗",
            "jina_key": "✓" if os.getenv("JINA_API_KEY") else "✗",
            "bright_data_key": "✓" if os.getenv("BRIGHT_DATA_API_KEY") else "✗",
            "wp_url": os.getenv("WORDPRESS_URL", "not set"),
            "wp_user": os.getenv("WP_USERNAME", "not set")
        }
        
        context = {
            "request": request,
            "title": "System Health",
            "health_data": health_data,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("health.html", context)
    except Exception as e:
        logger.error(f"Health dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/config", response_class=HTMLResponse)
async def config_dashboard(request: Request):
    """Configuration profiles management page"""
    try:
        context = {
            "request": request,
            "title": "Configuration Profiles",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("config-profiles.html", context)
    except Exception as e:
        logger.error(f"Config dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/instructions", response_class=HTMLResponse)
async def instructions_page(request: Request):
    """Instructions and user guide page"""
    try:
        context = {
            "request": request,
            "title": "Instructions & User Guide",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("instructions.html", context)
    except Exception as e:
        logger.error(f"Instructions page error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/features", response_class=HTMLResponse)
async def features_page(request: Request):
    """Features page showing all system capabilities"""
    try:
        context = {
            "request": request,
            "title": "Features",
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return templates.TemplateResponse("features.html", context)
    except Exception as e:
        logger.error(f"Features page error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/config/legacy", response_class=HTMLResponse)
async def legacy_config_dashboard(request: Request):
    """Legacy configuration management page"""
    try:
        # Get current configuration
        config_data = {
            "wordpress": {
                "url": os.getenv("WORDPRESS_URL", ""),
                "username": os.getenv("WP_USERNAME", ""),
                "auth_method": os.getenv("WP_AUTH_METHOD", "basic"),
                "verify_ssl": os.getenv("WP_VERIFY_SSL", "true")
            },
            "content": {
                "min_words": os.getenv("ARTICLE_MIN_WORDS", "1500"),
                "max_words": os.getenv("ARTICLE_MAX_WORDS", "2500"),
                "max_cost": os.getenv("MAX_COST_PER_ARTICLE", "15.00"),
                "monthly_budget": os.getenv("MAX_MONTHLY_COST", "500.00")
            },
            "agents": {
                "competitor_monitoring": os.getenv("ENABLE_COMPETITOR_MONITORING", "true") == "true",
                "topic_analysis": os.getenv("ENABLE_TOPIC_ANALYSIS", "true") == "true",
                "fact_checking": os.getenv("ENABLE_FACT_CHECKING", "true") == "true",
                "auto_publish": os.getenv("ENABLE_AUTO_PUBLISH", "false") == "true"
            }
        }
        
        context = {
            "request": request,
            "title": "Configuration",
            "config_data": config_data,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return templates.TemplateResponse("config.html", context)
    except Exception as e:
        logger.error(f"Config dashboard error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/competitors", response_class=HTMLResponse)
async def competitors_page(request: Request):
    """Competitor management page"""
    try:
        from src.services.competitor_manager import get_competitor_manager
        manager = get_competitor_manager()
        competitors = manager.get_all_competitors()
        
        # Calculate statistics
        total_competitors = len(competitors)
        active_competitors = len([c for c in competitors if c.is_active])
        total_articles_tracked = sum(c.total_articles_found for c in competitors)
        trending_topics_count = len(set(topic for c in competitors for topic in c.trending_topics))
        
        context = {
            "request": request,
            "title": "Competitor Management",
            "competitors": competitors,
            "total_competitors": total_competitors,
            "active_competitors": active_competitors,
            "total_articles_tracked": total_articles_tracked,
            "trending_topics_count": trending_topics_count
        }
        
        return templates.TemplateResponse("competitors.html", context)
    except Exception as e:
        logger.error(f"Competitors page error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@router.get("/profile-settings", response_class=HTMLResponse)
async def profile_settings_page(request: Request):
    """Profile settings page for managing API keys"""
    try:
        api_keys_manager = get_api_keys_manager()
        masked_keys = api_keys_manager.get_all_keys()
        
        context = {
            "request": request,
            "title": "Profile Settings",
            "api_keys": masked_keys
        }
        
        return templates.TemplateResponse("profile-settings.html", context)
    except Exception as e:
        logger.error(f"Profile settings error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


# WebSocket for Real-time Logs
@router.websocket("/ws/logs/{pipeline_id}")
async def websocket_logs(websocket: WebSocket, pipeline_id: str):
    """WebSocket endpoint for streaming pipeline logs"""
    try:
        await websocket.accept()
        logger.info(f"WebSocket connected for pipeline {pipeline_id}")
        
        # Add this connection to the pipeline logger
        pipeline_logger.add_connection(pipeline_id, websocket)
        
        # Send initial logs if any exist
        existing_logs = pipeline_logger.get_logs(pipeline_id, limit=100)
        if existing_logs:
            await websocket.send_json({
                "type": "initial",
                "logs": existing_logs
            })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for any message from client (heartbeat, etc.)
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_text("pong")
            except WebSocketDisconnect:
                logger.info(f"WebSocket client disconnected for pipeline {pipeline_id}")
                break
            except Exception as e:
                logger.error(f"WebSocket receive error for pipeline {pipeline_id}: {e}")
                break
                
    except Exception as e:
        logger.error(f"WebSocket handler error for pipeline {pipeline_id}: {e}")
        try:
            await websocket.close(code=1000)
        except:
            pass
    finally:
        # Remove connection when done
        try:
            pipeline_logger.remove_connection(pipeline_id, websocket)
        except Exception as e:
            logger.error(f"Error removing WebSocket connection: {e}")
        logger.info(f"WebSocket disconnected for pipeline {pipeline_id}")


@router.get("/logs/{pipeline_id}")
async def get_pipeline_logs(pipeline_id: str, limit: int = 100):
    """Get recent logs for a pipeline"""
    logs = pipeline_logger.get_logs(pipeline_id, limit=limit)
    return {
        "pipeline_id": pipeline_id,
        "logs": logs,
        "count": len(logs)
    }


@router.delete("/logs/{pipeline_id}")
async def clear_pipeline_logs(pipeline_id: str):
    """Clear logs for a pipeline"""
    pipeline_logger.clear_logs(pipeline_id)
    return {
        "success": True,
        "message": f"Logs cleared for pipeline {pipeline_id}"
    }