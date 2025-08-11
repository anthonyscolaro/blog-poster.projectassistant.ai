"""
Configuration Profile Management System

Handles CRUD operations for website-specific configuration profiles.
Each profile contains WordPress settings, content generation parameters,
agent configurations, and API keys for different websites/environments.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class WordPressConfig(BaseModel):
    """WordPress connection configuration"""
    url: str = Field(..., description="WordPress site URL")
    username: str = Field(..., description="WordPress username")
    password: str = Field(..., description="WordPress password or app password")
    auth_method: str = Field(default="basic", description="Authentication method")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificate")
    graphql_endpoint: str = Field(default="/graphql", description="GraphQL endpoint path")


class ContentConfig(BaseModel):
    """Content generation settings"""
    min_words: int = Field(default=1500, description="Minimum article word count")
    max_words: int = Field(default=2500, description="Maximum article word count")
    max_cost_per_article: float = Field(default=15.00, description="Maximum cost per article")
    monthly_budget: float = Field(default=500.00, description="Monthly budget limit")
    alert_threshold: float = Field(default=400.00, description="Cost alert threshold")


class AgentConfig(BaseModel):
    """AI agent configuration"""
    competitor_monitoring: bool = Field(default=True, description="Enable competitor monitoring")
    topic_analysis: bool = Field(default=True, description="Enable topic analysis")
    fact_checking: bool = Field(default=True, description="Enable legal fact checking")
    auto_publish: bool = Field(default=False, description="Enable auto publishing")
    require_human_approval: bool = Field(default=True, description="Require human approval")


class AdvancedConfig(BaseModel):
    """Advanced system settings"""
    log_level: str = Field(default="INFO", description="Logging level")
    max_workers: int = Field(default=4, description="Maximum concurrent workers")
    task_timeout: int = Field(default=300, description="Task timeout in seconds")
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    api_rate_limit: int = Field(default=60, description="API rate limit per minute")
    scraping_delay: float = Field(default=1.0, description="Delay between scraping requests")


class ConfigProfile(BaseModel):
    """Complete configuration profile for a website"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique profile ID")
    name: str = Field(..., description="Profile name (e.g., 'ServiceDogUS Production')")
    description: str = Field(default="", description="Profile description")
    website_url: str = Field(..., description="Target website URL")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=False, description="Currently active profile")
    
    # Configuration sections
    wordpress: WordPressConfig
    content: ContentConfig = Field(default_factory=ContentConfig)
    agents: AgentConfig = Field(default_factory=AgentConfig)
    advanced: AdvancedConfig = Field(default_factory=AdvancedConfig)
    
    # Environment-specific settings (stored separately for security)
    env_file: Optional[str] = Field(default=None, description="Associated .env file")


class ConfigProfileManager:
    """Manages CRUD operations for configuration profiles"""
    
    def __init__(self, storage_path: str = "config/profiles.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.profiles: Dict[str, ConfigProfile] = {}
        self.load_profiles()
    
    def load_profiles(self) -> None:
        """Load profiles from storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.profiles = {
                        profile_id: ConfigProfile(**profile_data)
                        for profile_id, profile_data in data.items()
                    }
            except Exception as e:
                print(f"Error loading profiles: {e}")
                self.profiles = {}
    
    def save_profiles(self) -> None:
        """Save profiles to storage"""
        try:
            data = {
                profile_id: profile.model_dump()
                for profile_id, profile in self.profiles.items()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving profiles: {e}")
    
    def create_profile(self, profile: ConfigProfile) -> ConfigProfile:
        """Create a new configuration profile"""
        # Ensure unique name
        existing_names = [p.name for p in self.profiles.values()]
        original_name = profile.name
        counter = 1
        while profile.name in existing_names:
            profile.name = f"{original_name} ({counter})"
            counter += 1
        
        profile.updated_at = datetime.now()
        self.profiles[profile.id] = profile
        self.save_profiles()
        return profile
    
    def get_profile(self, profile_id: str) -> Optional[ConfigProfile]:
        """Get a profile by ID"""
        return self.profiles.get(profile_id)
    
    def get_all_profiles(self) -> List[ConfigProfile]:
        """Get all profiles"""
        return list(self.profiles.values())
    
    def get_profiles_by_website(self, website_url: str) -> List[ConfigProfile]:
        """Get all profiles for a specific website"""
        return [
            profile for profile in self.profiles.values()
            if profile.website_url == website_url
        ]
    
    def update_profile(self, profile_id: str, updates: Dict[str, Any]) -> Optional[ConfigProfile]:
        """Update an existing profile"""
        if profile_id not in self.profiles:
            return None
        
        profile = self.profiles[profile_id]
        
        # Update fields
        for field, value in updates.items():
            if hasattr(profile, field):
                setattr(profile, field, value)
        
        profile.updated_at = datetime.now()
        self.save_profiles()
        return profile
    
    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile"""
        if profile_id in self.profiles:
            # Don't delete if it's the active profile
            if self.profiles[profile_id].is_active:
                return False
            
            del self.profiles[profile_id]
            self.save_profiles()
            return True
        return False
    
    def duplicate_profile(self, profile_id: str, new_name: str) -> Optional[ConfigProfile]:
        """Duplicate an existing profile with a new name"""
        if profile_id not in self.profiles:
            return None
        
        original = self.profiles[profile_id]
        
        # Create a copy
        new_profile = ConfigProfile(
            name=new_name,
            description=f"Copy of {original.name}",
            website_url=original.website_url,
            wordpress=original.wordpress.model_copy(),
            content=original.content.model_copy(),
            agents=original.agents.model_copy(),
            advanced=original.advanced.model_copy(),
            is_active=False
        )
        
        return self.create_profile(new_profile)
    
    def get_active_profile(self) -> Optional[ConfigProfile]:
        """Get the currently active profile"""
        for profile in self.profiles.values():
            if profile.is_active:
                return profile
        return None
    
    def set_active_profile(self, profile_id: str) -> bool:
        """Set a profile as active (and deactivate others)"""
        if profile_id not in self.profiles:
            return False
        
        # Deactivate all profiles
        for profile in self.profiles.values():
            profile.is_active = False
        
        # Activate the selected profile
        self.profiles[profile_id].is_active = True
        self.save_profiles()
        return True
    
    def export_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Export a profile as JSON"""
        if profile_id not in self.profiles:
            return None
        
        profile = self.profiles[profile_id]
        return profile.model_dump()
    
    def import_profile(self, profile_data: Dict[str, Any]) -> Optional[ConfigProfile]:
        """Import a profile from JSON"""
        try:
            # Remove ID to create a new one
            profile_data.pop('id', None)
            profile_data.pop('created_at', None)
            profile_data.pop('updated_at', None)
            profile_data['is_active'] = False
            
            profile = ConfigProfile(**profile_data)
            return self.create_profile(profile)
        except Exception as e:
            print(f"Error importing profile: {e}")
            return None
    
    def search_profiles(self, query: str) -> List[ConfigProfile]:
        """Search profiles by name, description, or website URL"""
        query = query.lower()
        results = []
        
        for profile in self.profiles.values():
            if (query in profile.name.lower() or 
                query in profile.description.lower() or 
                query in profile.website_url.lower()):
                results.append(profile)
        
        return results


# Global instance
profile_manager = ConfigProfileManager()


def get_profile_manager() -> ConfigProfileManager:
    """Get the global profile manager instance"""
    return profile_manager


def create_default_profiles():
    """Create default profiles for common setups"""
    manager = get_profile_manager()
    
    # Local development profile
    if not any(p.name == "Local Development" for p in manager.get_all_profiles()):
        local_profile = ConfigProfile(
            name="Local Development",
            description="Local WordPress development environment",
            website_url="http://localhost:8084",
            wordpress=WordPressConfig(
                url="http://localhost:8084",
                username="admin",
                password="admin123",
                auth_method="basic",
                verify_ssl=False
            ),
            env_file=".env.local"
        )
        manager.create_profile(local_profile)
    
    # Production profile template
    if not any(p.name == "Production Template" for p in manager.get_all_profiles()):
        prod_profile = ConfigProfile(
            name="Production Template",
            description="Template for production WordPress sites",
            website_url="https://example.com",
            wordpress=WordPressConfig(
                url="https://example.com",
                username="your-username",
                password="your-app-password",
                auth_method="application",
                verify_ssl=True
            ),
            content=ContentConfig(
                min_words=2000,
                max_words=3000,
                auto_publish=False,
                require_human_approval=True
            ),
            env_file=".env.prod"
        )
        manager.create_profile(prod_profile)


if __name__ == "__main__":
    # Create default profiles for testing
    create_default_profiles()
    
    manager = get_profile_manager()
    profiles = manager.get_all_profiles()
    
    print(f"Created {len(profiles)} default profiles:")
    for profile in profiles:
        print(f"- {profile.name}: {profile.website_url}")