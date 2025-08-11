"""
Pipeline orchestration endpoints
"""
import os
import glob
import json as json_lib
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException

from src.services.orchestration_manager import (
    OrchestrationManager, 
    PipelineConfig, 
    PipelineResult,
    PipelineStatus
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pipeline", tags=["pipeline"])

# Global orchestration manager
orchestration_manager = None

def get_orchestration_manager():
    """Get or create orchestration manager"""
    global orchestration_manager
    if orchestration_manager is None:
        orchestration_manager = OrchestrationManager()
    return orchestration_manager


@router.post("/run")
async def run_full_pipeline(config: PipelineConfig):
    """
    Run the complete multi-agent blog generation pipeline
    
    This orchestrates all 5 agents in sequence:
    1. Competitor Monitoring
    2. Topic Analysis
    3. Article Generation
    4. Legal Fact Checking
    5. WordPress Publishing
    """
    manager = get_orchestration_manager()
    
    try:
        logger.info(f"Starting pipeline for topic: {config.topic or 'auto-determined'}")
        result = await manager.run_pipeline(config)
        
        # Generate a pipeline ID based on start time
        pipeline_id = f"pipeline_{result.started_at.strftime('%Y%m%d%H%M%S')}"
        
        # Convert to dict for response
        response = {
            "status": result.status,
            "execution_time": result.execution_time,
            "total_cost": result.total_cost,
            "errors": result.errors,
            "warnings": result.warnings,
            "pipeline_id": pipeline_id
        }
        
        # Add article details if generated
        if result.article:
            response["article"] = {
                "title": result.article.title,
                "word_count": result.article.word_count,
                "seo_score": result.article.seo_score,
                "slug": result.article.slug
            }
        
        # Add fact check summary if performed
        if result.fact_check_report:
            response["fact_check"] = {
                "accuracy_score": result.fact_check_report.overall_accuracy_score,
                "verified_claims": result.fact_check_report.verified_claims,
                "incorrect_claims": result.fact_check_report.incorrect_claims,
                "total_claims": result.fact_check_report.total_claims
            }
        
        # Add WordPress details if published
        if result.wordpress_result and result.wordpress_result.get("success"):
            response["wordpress"] = {
                "post_id": result.wordpress_result["post_id"],
                "edit_link": result.wordpress_result["edit_link"],
                "view_link": result.wordpress_result.get("view_link")
            }
        
        return response
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise HTTPException(500, f"Pipeline execution failed: {str(e)}")


@router.get("/status")
async def get_pipeline_status():
    """Get current pipeline execution status"""
    manager = get_orchestration_manager()
    status = manager.get_pipeline_status()
    
    if status:
        return {
            "running": True,
            "status": status,
            "message": f"Pipeline is currently in {status} stage"
        }
    else:
        return {
            "running": False,
            "status": None,
            "message": "No pipeline currently running"
        }


@router.get("/history")
async def get_pipeline_history(limit: int = 10):
    """Get recent pipeline execution history"""
    manager = get_orchestration_manager()
    history = manager.get_pipeline_history(limit)
    
    return {
        "executions": [
            {
                "status": h.status,
                "started_at": h.started_at.isoformat(),
                "completed_at": h.completed_at.isoformat() if h.completed_at else None,
                "execution_time": h.execution_time,
                "total_cost": h.total_cost,
                "errors": h.errors
            }
            for h in history
        ],
        "total": len(history)
    }


@router.get("/costs")
async def get_pipeline_costs():
    """Get cost summary for pipeline executions"""
    manager = get_orchestration_manager()
    return manager.get_cost_summary()


@router.get("/{pipeline_id}/details")
async def get_pipeline_details(pipeline_id: str):
    """Get detailed information about a specific pipeline run"""
    manager = get_orchestration_manager()
    
    # Find the pipeline in history
    for result in manager.pipeline_history:
        # Check if this pipeline matches the ID
        result_id = f"pipeline_{result.started_at.strftime('%Y%m%d%H%M%S')}"
        if result_id == pipeline_id or pipeline_id.startswith(result_id):
            return {
                "pipeline_id": pipeline_id,
                "status": result.status.value,
                "started_at": result.started_at.isoformat(),
                "completed_at": result.completed_at.isoformat() if result.completed_at else None,
                "execution_time": result.execution_time,
                "total_cost": result.total_cost,
                "primary_keyword": result.topic_recommendation.primary_keyword if result.topic_recommendation else None,
                "article": result.article.dict() if result.article else None,
                "topic_recommendation": result.topic_recommendation.dict() if result.topic_recommendation else None,
                "competitor_insights": result.competitor_insights if result.competitor_insights else None,
                "fact_check_report": result.fact_check_report.dict() if result.fact_check_report else None,
                "wordpress_result": result.wordpress_result if result.wordpress_result else None,
                "errors": result.errors,
                "warnings": result.warnings
            }
    
    # Check if it's a saved article file
    article_files = glob.glob(f"data/articles/*{pipeline_id}*.json")
    if article_files:
        with open(article_files[0], 'r') as f:
            article_data = json_lib.load(f)
            return {
                "pipeline_id": pipeline_id,
                "status": "completed",
                "started_at": article_data.get('generated_at'),
                "completed_at": article_data.get('generated_at'),
                "execution_time": 0,
                "total_cost": article_data.get('cost_tracking', {}).get('cost', 0),
                "primary_keyword": article_data.get('primary_keyword'),
                "article": article_data,
                "topic_recommendation": {
                    "title": article_data.get('title'),
                    "primary_keyword": article_data.get('primary_keyword'),
                    "secondary_keywords": article_data.get('secondary_keywords', [])
                },
                "competitor_insights": None,
                "fact_check_report": None,
                "wordpress_result": None,
                "errors": [],
                "warnings": []
            }
    
    raise HTTPException(404, f"Pipeline {pipeline_id} not found")