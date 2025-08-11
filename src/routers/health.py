"""
Health and basic system endpoints
"""
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> Dict[str, Any]:
    """Simple health endpoint for container checks."""
    return {"status": "ok", "time": datetime.utcnow().isoformat()}