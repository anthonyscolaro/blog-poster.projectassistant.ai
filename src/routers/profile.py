"""
Profile settings and API keys management endpoints
"""
import logging
from typing import Dict, Optional
from fastapi import APIRouter

logger = logging.getLogger(__name__)

# Database-backed API keys manager only (no fallback)
from src.services.api_keys_manager_db import get_api_keys_manager_db as get_api_keys_manager

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.post("/api-keys")
async def save_api_keys(keys: Dict[str, Optional[str]]):
    """Save API keys securely"""
    try:
        api_keys_manager = get_api_keys_manager()
        
        # Only update non-null values
        update_dict = {k: v for k, v in keys.items() if v}
        
        if update_dict:
            api_keys_manager.update_keys(**update_dict)
        
        return {
            "success": True,
            "message": "API keys saved successfully",
            "updated_keys": list(update_dict.keys())
        }
    except Exception as e:
        logger.error(f"Failed to save API keys: {e}")
        return {"success": False, "message": str(e)}


@router.get("/test-key/{key_name}")
async def test_api_key(key_name: str):
    """Test if an API key is valid"""
    try:
        api_keys_manager = get_api_keys_manager()
        
        # Get the key value
        key_value = api_keys_manager.get_key(key_name)
        if not key_value:
            return {"success": False, "message": "Key not configured"}
        
        # Validate format first
        if not api_keys_manager.validate_key(key_name, key_value):
            return {"success": False, "message": "Invalid key format"}
        
        # Test the key asynchronously
        result = await api_keys_manager._test_api_key_async(key_name, key_value)
        return result
    except Exception as e:
        logger.error(f"Failed to test API key {key_name}: {e}")
        return {"success": False, "message": str(e)}


@router.delete("/clear-key/{key_name}")
async def clear_api_key(key_name: str):
    """Clear a specific API key"""
    try:
        api_keys_manager = get_api_keys_manager()
        api_keys_manager.clear_key(key_name)
        return {"success": True, "message": f"{key_name} cleared successfully"}
    except Exception as e:
        logger.error(f"Failed to clear API key {key_name}: {e}")
        return {"success": False, "message": str(e)}


@router.get("/export-env")
async def export_env_keys():
    """Export API keys in .env format"""
    try:
        api_keys_manager = get_api_keys_manager()
        env_content = api_keys_manager.export_for_env()
        return {"success": True, "content": env_content}
    except Exception as e:
        logger.error(f"Failed to export env keys: {e}")
        return {"success": False, "message": str(e)}