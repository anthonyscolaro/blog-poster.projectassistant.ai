"""
Monitoring endpoints for agent health and system metrics
"""
import os
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Depends, HTTPException
import httpx
import asyncio

from src.models.responses import (
    ApiResponse,
    AgentStatusResponse,
    SystemMetricsResponse,
    create_response
)
from src.middleware.auth import auth_middleware
from src.database import get_db_session
from src.database.repositories import PipelineRepository, ArticleRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


# Agent configuration
AGENTS = [
    {
        "id": "competitor-monitoring",
        "name": "Competitor Monitoring Agent",
        "health_check": None,  # Will use internal check
        "critical": True
    },
    {
        "id": "topic-analysis",
        "name": "Topic Analysis Agent",
        "health_check": None,
        "critical": True
    },
    {
        "id": "article-generation",
        "name": "Article Generation Agent",
        "health_check": None,
        "critical": True
    },
    {
        "id": "legal-fact-checker",
        "name": "Legal Fact Checker Agent",
        "health_check": None,
        "critical": True
    },
    {
        "id": "wordpress-publisher",
        "name": "WordPress Publishing Agent",
        "health_check": None,
        "critical": False
    }
]


@router.get("/agents/status", response_model=ApiResponse[List[AgentStatusResponse]])
async def get_agents_status(request: Request):
    """
    Get health status of all agents
    """
    agent_statuses = []
    
    for agent in AGENTS:
        status = await check_agent_health(agent)
        agent_statuses.append(status)
    
    return create_response(
        data=agent_statuses,
        message="Agent health check completed"
    )


@router.get("/agents/{agent_id}/status", response_model=ApiResponse[AgentStatusResponse])
async def get_agent_status(agent_id: str, request: Request):
    """
    Get health status of a specific agent
    """
    agent = next((a for a in AGENTS if a['id'] == agent_id), None)
    
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    status = await check_agent_health(agent)
    
    return create_response(
        data=status,
        message=f"Health check for {agent['name']}"
    )


async def check_agent_health(agent: Dict) -> AgentStatusResponse:
    """
    Check health of a single agent
    """
    start_time = datetime.utcnow()
    
    try:
        # Check if agent has required dependencies
        status = "healthy"
        error_rate = 0.0
        
        # Check specific agent requirements
        if agent['id'] == 'competitor-monitoring':
            # Check Jina API key
            if not os.getenv('JINA_API_KEY'):
                status = "error"
                error_rate = 1.0
                
        elif agent['id'] == 'article-generation':
            # Check Claude/OpenAI API keys
            if not (os.getenv('ANTHROPIC_API_KEY') or os.getenv('OPENAI_API_KEY')):
                status = "error"
                error_rate = 1.0
                
        elif agent['id'] == 'wordpress-publisher':
            # Check WordPress configuration
            if not (os.getenv('WORDPRESS_URL') and os.getenv('WP_APP_PASSWORD')):
                status = "warning"
                error_rate = 0.5
        
        # Calculate response time
        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        return AgentStatusResponse(
            id=agent['id'],
            name=agent['name'],
            status=status,
            lastCheck=datetime.utcnow(),
            responseTime=response_time,
            errorRate=error_rate
        )
        
    except Exception as e:
        logger.error(f"Error checking agent {agent['id']}: {e}")
        
        return AgentStatusResponse(
            id=agent['id'],
            name=agent['name'],
            status="offline",
            lastCheck=datetime.utcnow(),
            responseTime=0,
            errorRate=1.0
        )


@router.get("/metrics", response_model=ApiResponse[SystemMetricsResponse])
async def get_system_metrics(request: Request):
    """
    Get system-wide metrics and statistics
    """
    try:
        with get_db_session() as db:
            pipeline_repo = PipelineRepository(db)
            article_repo = ArticleRepository(db)
            
            # Get statistics from the last 30 days
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            # Get pipeline statistics
            all_pipelines = pipeline_repo.get_all()
            recent_pipelines = [
                p for p in all_pipelines 
                if p.started_at and p.started_at >= thirty_days_ago
            ]
            
            # Calculate success rate
            completed_pipelines = [p for p in recent_pipelines if p.status == 'completed']
            success_rate = (
                len(completed_pipelines) / len(recent_pipelines) * 100 
                if recent_pipelines else 0
            )
            
            # Calculate average processing time
            processing_times = [
                p.execution_time_seconds 
                for p in completed_pipelines 
                if p.execution_time_seconds
            ]
            avg_processing_time = (
                sum(processing_times) / len(processing_times) 
                if processing_times else 0
            )
            
            # Get active pipelines
            active_pipelines = pipeline_repo.get_active()
            
            # Calculate monthly spend
            monthly_costs = [
                float(p.total_cost or 0) 
                for p in recent_pipelines
            ]
            monthly_spend = sum(monthly_costs)
            
            # Get article statistics
            article_stats = article_repo.get_stats()
            
            # Estimate API usage (mock for now)
            api_usage = estimate_api_usage(recent_pipelines)
            
            metrics = SystemMetricsResponse(
                totalArticles=article_stats.get('total', 0),
                successRate=round(success_rate, 2),
                avgProcessingTime=round(avg_processing_time, 2),
                activePipelines=len(active_pipelines),
                monthlySpend=round(monthly_spend, 2),
                apiUsage=api_usage
            )
            
            return create_response(
                data=metrics,
                message="System metrics retrieved successfully"
            )
            
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        
        # Return default metrics on error
        return create_response(
            data=SystemMetricsResponse(
                totalArticles=0,
                successRate=0,
                avgProcessingTime=0,
                activePipelines=0,
                monthlySpend=0,
                apiUsage={}
            ),
            message="Unable to retrieve complete metrics"
        )


def estimate_api_usage(pipelines: List) -> Dict[str, int]:
    """
    Estimate API usage based on pipeline executions
    """
    # Rough estimates per pipeline
    usage_per_pipeline = {
        'anthropic': 5000,  # tokens
        'jina': 2,  # requests
        'openai': 0,  # tokens (if used as fallback)
    }
    
    pipeline_count = len(pipelines)
    
    return {
        'anthropic': usage_per_pipeline['anthropic'] * pipeline_count,
        'jina': usage_per_pipeline['jina'] * pipeline_count,
        'openai': usage_per_pipeline['openai'] * pipeline_count,
    }


@router.get("/health/dependencies")
@auth_middleware.require_permission('read')
async def check_dependencies(request: Request):
    """
    Check health of all external dependencies
    """
    dependencies = {
        'database': await check_database_health(),
        'qdrant': await check_qdrant_health(),
        'redis': await check_redis_health(),
        'supabase': await check_supabase_health(),
        'anthropic': check_api_key_health('ANTHROPIC_API_KEY'),
        'jina': check_api_key_health('JINA_API_KEY'),
        'wordpress': await check_wordpress_health(),
    }
    
    all_healthy = all(dep['status'] == 'healthy' for dep in dependencies.values())
    
    return create_response(
        data={
            'overall_status': 'healthy' if all_healthy else 'degraded',
            'dependencies': dependencies
        },
        message="Dependency health check completed"
    )


async def check_database_health() -> Dict:
    """Check PostgreSQL database health"""
    try:
        with get_db_session() as db:
            # Simple query to check connection
            db.execute("SELECT 1")
            return {'status': 'healthy', 'message': 'Database connection successful'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


async def check_qdrant_health() -> Dict:
    """Check Qdrant vector database health"""
    try:
        qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{qdrant_url}/health")
            if response.status_code == 200:
                return {'status': 'healthy', 'message': 'Qdrant is operational'}
            else:
                return {'status': 'warning', 'message': f'Qdrant returned status {response.status_code}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


async def check_redis_health() -> Dict:
    """Check Redis health"""
    try:
        import redis
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            decode_responses=True
        )
        r.ping()
        return {'status': 'healthy', 'message': 'Redis is operational'}
    except Exception as e:
        return {'status': 'warning', 'message': 'Redis not configured or unavailable'}


async def check_supabase_health() -> Dict:
    """Check Supabase health"""
    try:
        supabase_url = os.getenv('SUPABASE_URL')
        if not supabase_url:
            return {'status': 'warning', 'message': 'Supabase not configured'}
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{supabase_url}/rest/v1/")
            if response.status_code < 500:
                return {'status': 'healthy', 'message': 'Supabase is operational'}
            else:
                return {'status': 'error', 'message': f'Supabase returned status {response.status_code}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


async def check_wordpress_health() -> Dict:
    """Check WordPress connection health"""
    try:
        wp_url = os.getenv('WORDPRESS_URL')
        if not wp_url:
            return {'status': 'warning', 'message': 'WordPress not configured'}
        
        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            response = await client.get(f"{wp_url}/wp-json/wp/v2/posts?per_page=1")
            if response.status_code in [200, 401]:  # 401 is ok, means auth required
                return {'status': 'healthy', 'message': 'WordPress API is accessible'}
            else:
                return {'status': 'warning', 'message': f'WordPress returned status {response.status_code}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def check_api_key_health(env_var: str) -> Dict:
    """Check if API key is configured"""
    if os.getenv(env_var):
        return {'status': 'healthy', 'message': f'{env_var} is configured'}
    else:
        return {'status': 'warning', 'message': f'{env_var} not configured'}