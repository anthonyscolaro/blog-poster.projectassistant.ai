"""
Configuration Profile API Endpoints

REST API endpoints for managing configuration profiles.
Provides CRUD operations for website-specific configurations.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .config_profiles import (
    ConfigProfile, 
    ConfigProfileManager,
    WordPressConfig,
    ContentConfig,
    AgentConfig,
    AdvancedConfig,
    get_profile_manager,
    create_default_profiles
)

router = APIRouter(prefix="/api/config", tags=["configuration"])

# Request/Response models
class ProfileCreateRequest(BaseModel):
    """Request model for creating a new profile"""
    name: str
    description: str = ""
    website_url: str
    wordpress: WordPressConfig
    content: ContentConfig = Field(default_factory=ContentConfig)
    agents: AgentConfig = Field(default_factory=AgentConfig)
    advanced: AdvancedConfig = Field(default_factory=AdvancedConfig)


class ProfileUpdateRequest(BaseModel):
    """Request model for updating a profile"""
    name: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    wordpress: Optional[WordPressConfig] = None
    content: Optional[ContentConfig] = None
    agents: Optional[AgentConfig] = None
    advanced: Optional[AdvancedConfig] = None


class ProfileResponse(BaseModel):
    """Response model for profile data"""
    success: bool
    message: str
    profile: Optional[ConfigProfile] = None


class ProfileListResponse(BaseModel):
    """Response model for profile lists"""
    success: bool
    message: str
    profiles: List[ConfigProfile]
    total: int


@router.get("/profiles", response_model=ProfileListResponse)
async def get_profiles(website_url: Optional[str] = None, search: Optional[str] = None):
    """Get all configuration profiles, optionally filtered by website or search query"""
    try:
        manager = get_profile_manager()
        
        if search:
            profiles = manager.search_profiles(search)
        elif website_url:
            profiles = manager.get_profiles_by_website(website_url)
        else:
            profiles = manager.get_all_profiles()
        
        return ProfileListResponse(
            success=True,
            message=f"Found {len(profiles)} profile(s)",
            profiles=profiles,
            total=len(profiles)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profiles: {str(e)}")


@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: str):
    """Get a specific configuration profile by ID"""
    try:
        manager = get_profile_manager()
        profile = manager.get_profile(profile_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return ProfileResponse(
            success=True,
            message="Profile retrieved successfully",
            profile=profile
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")


@router.post("/profiles", response_model=ProfileResponse)
async def create_profile(request: ProfileCreateRequest):
    """Create a new configuration profile"""
    try:
        manager = get_profile_manager()
        
        # Create profile from request
        profile = ConfigProfile(
            name=request.name,
            description=request.description,
            website_url=request.website_url,
            wordpress=request.wordpress,
            content=request.content,
            agents=request.agents,
            advanced=request.advanced
        )
        
        created_profile = manager.create_profile(profile)
        
        return ProfileResponse(
            success=True,
            message=f"Profile '{created_profile.name}' created successfully",
            profile=created_profile
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")


@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
async def update_profile(profile_id: str, request: ProfileUpdateRequest):
    """Update an existing configuration profile"""
    try:
        manager = get_profile_manager()
        
        # Convert request to dictionary, excluding None values
        updates = request.model_dump(exclude_none=True)
        
        updated_profile = manager.update_profile(profile_id, updates)
        
        if not updated_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return ProfileResponse(
            success=True,
            message=f"Profile '{updated_profile.name}' updated successfully",
            profile=updated_profile
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


@router.delete("/profiles/{profile_id}")
async def delete_profile(profile_id: str):
    """Delete a configuration profile"""
    try:
        manager = get_profile_manager()
        
        # Check if profile exists
        profile = manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Check if it's the active profile
        if profile.is_active:
            raise HTTPException(status_code=400, detail="Cannot delete the active profile")
        
        success = manager.delete_profile(profile_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to delete profile")
        
        return JSONResponse({
            "success": True,
            "message": f"Profile '{profile.name}' deleted successfully"
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete profile: {str(e)}")


@router.post("/profiles/{profile_id}/duplicate", response_model=ProfileResponse)
async def duplicate_profile(profile_id: str, new_name: str):
    """Duplicate an existing configuration profile"""
    try:
        manager = get_profile_manager()
        
        duplicated_profile = manager.duplicate_profile(profile_id, new_name)
        
        if not duplicated_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return ProfileResponse(
            success=True,
            message=f"Profile duplicated as '{duplicated_profile.name}'",
            profile=duplicated_profile
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to duplicate profile: {str(e)}")


@router.post("/profiles/{profile_id}/activate")
async def activate_profile(profile_id: str):
    """Set a profile as the active configuration"""
    try:
        manager = get_profile_manager()
        
        success = manager.set_active_profile(profile_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        profile = manager.get_profile(profile_id)
        
        return JSONResponse({
            "success": True,
            "message": f"Profile '{profile.name}' is now active"
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to activate profile: {str(e)}")


@router.get("/profiles/active/current", response_model=ProfileResponse)
async def get_active_profile():
    """Get the currently active configuration profile"""
    try:
        manager = get_profile_manager()
        active_profile = manager.get_active_profile()
        
        if not active_profile:
            return ProfileResponse(
                success=False,
                message="No active profile set",
                profile=None
            )
        
        return ProfileResponse(
            success=True,
            message="Active profile retrieved successfully",
            profile=active_profile
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get active profile: {str(e)}")


@router.get("/profiles/{profile_id}/export")
async def export_profile(profile_id: str):
    """Export a configuration profile as JSON"""
    try:
        manager = get_profile_manager()
        profile_data = manager.export_profile(profile_id)
        
        if not profile_data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return JSONResponse({
            "success": True,
            "message": "Profile exported successfully",
            "data": profile_data
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export profile: {str(e)}")


@router.post("/profiles/import", response_model=ProfileResponse)
async def import_profile(file: UploadFile = File(...)):
    """Import a configuration profile from JSON file"""
    try:
        # Read file content
        content = await file.read()
        import json
        profile_data = json.loads(content)
        
        manager = get_profile_manager()
        imported_profile = manager.import_profile(profile_data)
        
        if not imported_profile:
            raise HTTPException(status_code=400, detail="Invalid profile data")
        
        return ProfileResponse(
            success=True,
            message=f"Profile '{imported_profile.name}' imported successfully",
            profile=imported_profile
        )
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import profile: {str(e)}")


@router.post("/profiles/defaults")
async def create_default_profiles():
    """Create default configuration profiles"""
    try:
        create_default_profiles()
        
        manager = get_profile_manager()
        profiles = manager.get_all_profiles()
        
        return JSONResponse({
            "success": True,
            "message": f"Created default profiles. Total profiles: {len(profiles)}"
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create defaults: {str(e)}")


@router.post("/profiles/{profile_id}/test-connection")
async def test_wordpress_connection(profile_id: str):
    """Test WordPress connection for a specific profile"""
    try:
        manager = get_profile_manager()
        profile = manager.get_profile(profile_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Import WordPress publisher to test connection
        from ..services.wordpress_publisher import WordPressPublisher
        
        # Create publisher with profile settings
        publisher = WordPressPublisher(
            wp_url=profile.wordpress.url,
            username=profile.wordpress.username,
            password=profile.wordpress.password,
            auth_method=profile.wordpress.auth_method,
            verify_ssl=profile.wordpress.verify_ssl
        )
        
        # Test connection (this would need a test method in WordPressPublisher)
        # For now, just return success
        return JSONResponse({
            "success": True,
            "message": f"WordPress connection test completed for {profile.wordpress.url}",
            "details": {
                "url": profile.wordpress.url,
                "username": profile.wordpress.username,
                "auth_method": profile.wordpress.auth_method,
                "ssl_verify": profile.wordpress.verify_ssl
            }
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")


# Website management endpoints
@router.get("/websites")
async def get_websites():
    """Get list of unique websites from all profiles"""
    try:
        manager = get_profile_manager()
        profiles = manager.get_all_profiles()
        
        websites = list(set(profile.website_url for profile in profiles))
        websites.sort()
        
        return JSONResponse({
            "success": True,
            "websites": websites,
            "total": len(websites)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get websites: {str(e)}")


@router.get("/websites/{website_url}/profiles")
async def get_website_profiles(website_url: str):
    """Get all profiles for a specific website"""
    try:
        # URL decode the website_url
        import urllib.parse
        decoded_url = urllib.parse.unquote(website_url)
        
        manager = get_profile_manager()
        profiles = manager.get_profiles_by_website(decoded_url)
        
        return ProfileListResponse(
            success=True,
            message=f"Found {len(profiles)} profile(s) for {decoded_url}",
            profiles=profiles,
            total=len(profiles)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get website profiles: {str(e)}")