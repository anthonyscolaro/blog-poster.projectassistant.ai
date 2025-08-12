"""
Competitor monitoring endpoints
"""
import logging
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException

from agents import CompetitorMonitoringAgent, CompetitorInsights
from src.services.competitor_manager import get_competitor_manager, CompetitorProfile

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/competitors", tags=["competitors"])

# Global agent instance (in production, use dependency injection)
competitor_agent = None

def get_competitor_agent():
    """Get or create competitor monitoring agent"""
    global competitor_agent
    if competitor_agent is None:
        competitor_agent = CompetitorMonitoringAgent()
    return competitor_agent


@router.post("/scan")
async def scan_competitors(force: bool = False):
    """
    Scan competitor websites for new content
    
    Args:
        force: Force scan even if recently scanned
    """
    agent = get_competitor_agent()
    try:
        content = await agent.scan_competitors(force=force)
        return {
            "status": "success",
            "content_pieces": len(content),
            "message": f"Scanned {len(content)} pieces of content"
        }
    except Exception as e:
        logger.error(f"Competitor scan failed: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.get("/insights")
async def get_competitor_insights():
    """Get comprehensive competitor analysis and insights"""
    agent = get_competitor_agent()
    try:
        insights = await agent.generate_insights()
        return insights.dict()
    except Exception as e:
        logger.error(f"Failed to generate insights: {str(e)}")
        raise HTTPException(500, f"Failed to generate insights: {str(e)}")


@router.get("/trends")
async def get_trending_topics():
    """Get current trending topics from competitors"""
    agent = get_competitor_agent()
    try:
        content = await agent.scan_competitors()
        trends = agent.analyze_trends(content)
        return {
            "trends": [t.dict() for t in trends],
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get trends: {str(e)}")
        raise HTTPException(500, f"Failed to get trends: {str(e)}")


@router.get("/gaps")
async def get_content_gaps():
    """Identify content gaps compared to competitors"""
    agent = get_competitor_agent()
    try:
        content = await agent.scan_competitors()
        gaps = agent.identify_content_gaps(content)
        return {
            "gaps": [g.dict() for g in gaps],
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to identify gaps: {str(e)}")
        raise HTTPException(500, f"Failed to identify gaps: {str(e)}")


# Competitor Management API endpoints
@router.get("/api")
async def get_competitors():
    """Get all competitors"""
    manager = get_competitor_manager()
    competitors = manager.get_all_competitors()
    return {"success": True, "competitors": [c.dict() for c in competitors]}


@router.get("/api/{competitor_id}")
async def get_competitor(competitor_id: str):
    """Get a specific competitor"""
    manager = get_competitor_manager()
    competitor = manager.get_competitor(competitor_id)
    if competitor:
        return competitor.dict()
    raise HTTPException(404, "Competitor not found")


@router.post("/api")
async def add_competitor(competitor_data: Dict[str, Any]):
    """Add a new competitor"""
    try:
        manager = get_competitor_manager()
        profile = CompetitorProfile(**competitor_data)
        success = manager.add_competitor(profile)
        return {"success": success, "message": "Competitor added successfully" if success else "Competitor already exists"}
    except Exception as e:
        logger.error(f"Failed to add competitor: {e}")
        return {"success": False, "message": str(e)}


@router.put("/api/{competitor_id}")
async def update_competitor(competitor_id: str, updates: Dict[str, Any]):
    """Update a competitor"""
    try:
        manager = get_competitor_manager()
        success = manager.update_competitor(competitor_id, updates)
        return {"success": success, "message": "Competitor updated successfully" if success else "Competitor not found"}
    except Exception as e:
        logger.error(f"Failed to update competitor: {e}")
        return {"success": False, "message": str(e)}


@router.delete("/api/{competitor_id}")
async def delete_competitor(competitor_id: str):
    """Delete a competitor"""
    try:
        manager = get_competitor_manager()
        success = manager.delete_competitor(competitor_id)
        return {"success": success, "message": "Competitor deleted successfully" if success else "Competitor not found"}
    except Exception as e:
        logger.error(f"Failed to delete competitor: {e}")
        return {"success": False, "message": str(e)}


@router.post("/api/{competitor_id}/toggle")
async def toggle_competitor_status(competitor_id: str):
    """Toggle competitor active/inactive status"""
    try:
        manager = get_competitor_manager()
        success = manager.toggle_competitor_status(competitor_id)
        if success:
            competitor = manager.get_competitor(competitor_id)
            return {"success": True, "is_active": competitor.is_active}
        return {"success": False, "message": "Competitor not found"}
    except Exception as e:
        logger.error(f"Failed to toggle competitor status: {e}")
        return {"success": False, "message": str(e)}


@router.post("/api/{competitor_id}/scan")
async def scan_competitor(competitor_id: str):
    """Trigger a scan for a specific competitor"""
    try:
        # This would trigger actual scanning in production
        manager = get_competitor_manager()
        competitor = manager.get_competitor(competitor_id)
        if not competitor:
            return {"success": False, "message": "Competitor not found"}
        
        # For now, mock the scan
        manager.update_scan_timestamp(competitor_id)
        return {"success": True, "articles_found": 5, "message": "Scan completed successfully"}
    except Exception as e:
        logger.error(f"Failed to scan competitor: {e}")
        return {"success": False, "message": str(e)}


@router.get("/api/{competitor_id}/insights")
async def get_competitor_insights_for_id(competitor_id: str):
    """Get insights for a specific competitor"""
    try:
        manager = get_competitor_manager()
        insights = manager.get_competitor_insights(competitor_id)
        if insights:
            return insights.dict()
        raise HTTPException(404, "Competitor insights not found")
    except Exception as e:
        logger.error(f"Failed to get competitor insights: {e}")
        raise HTTPException(500, str(e))


@router.get("/api/export")
async def export_competitors():
    """Export all competitors as JSON"""
    try:
        manager = get_competitor_manager()
        content = manager.export_competitors()
        return {"success": True, "content": content}
    except Exception as e:
        logger.error(f"Failed to export competitors: {e}")
        return {"success": False, "message": str(e)}


@router.post("/api/import")
async def import_competitors(data: Dict[str, str]):
    """Import competitors from JSON"""
    try:
        manager = get_competitor_manager()
        imported = manager.import_competitors(data["data"])
        return {"success": True, "imported": imported, "message": f"Imported {imported} competitors"}
    except Exception as e:
        logger.error(f"Failed to import competitors: {e}")
        return {"success": False, "message": str(e)}