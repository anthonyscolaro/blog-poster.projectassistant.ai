"""
Competitor Management Service
Handles storage, retrieval, and management of competitor websites and their data
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
import logging

logger = logging.getLogger(__name__)


class CompetitorProfile(BaseModel):
    """Profile for a competitor website"""
    id: str
    domain: str
    name: str
    description: Optional[str] = None
    
    # URLs to monitor
    blog_url: Optional[str] = None
    news_url: Optional[str] = None
    resources_url: Optional[str] = None
    
    # Monitoring settings
    is_active: bool = True
    scan_frequency_hours: int = 24
    last_scanned: Optional[datetime] = None
    
    # Metrics
    total_articles_found: int = 0
    trending_topics: List[str] = Field(default_factory=list)
    average_post_frequency: Optional[float] = None  # posts per week
    
    # Analysis
    content_focus: List[str] = Field(default_factory=list)  # Main topics they cover
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    
    # Metadata
    added_date: datetime = Field(default_factory=datetime.now)
    updated_date: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None


class CompetitorInsight(BaseModel):
    """Insights gathered from competitor analysis"""
    competitor_id: str
    competitor_name: str
    scan_date: datetime
    
    # Content metrics
    new_articles_count: int = 0
    total_articles_scanned: int = 0
    
    # Topics
    trending_topics: List[Dict[str, Any]] = Field(default_factory=list)
    content_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Performance
    estimated_traffic: Optional[int] = None
    engagement_score: Optional[float] = None
    
    # Content analysis
    average_word_count: int = 0
    posting_frequency: str = ""  # e.g., "3 posts/week"
    content_types: Dict[str, int] = Field(default_factory=dict)  # blog: 10, news: 5, etc.


class CompetitorManager:
    """
    Manages competitor profiles and their associated data
    """
    
    def __init__(self, storage_path: str = "data/competitors/profiles.json"):
        """
        Initialize the competitor manager
        
        Args:
            storage_path: Path to store competitor profiles
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Default competitors for ServiceDogUS
        self.default_competitors = [
            {
                "id": "servicedogcentral",
                "domain": "servicedogcentral.org",
                "name": "Service Dog Central",
                "description": "Comprehensive resource for service dog information",
                "blog_url": "https://servicedogcentral.org/content/blog",
                "is_active": True,
                "content_focus": ["training", "laws", "handler stories"]
            },
            {
                "id": "assistancedogs",
                "domain": "assistancedogsinternational.org",
                "name": "Assistance Dogs International",
                "description": "Global authority on assistance dog standards",
                "blog_url": "https://assistancedogsinternational.org/resources/",
                "is_active": True,
                "content_focus": ["standards", "certification", "international laws"]
            },
            {
                "id": "usserviceanimals",
                "domain": "usserviceanimals.org",
                "name": "US Service Animals",
                "description": "Registration and information service",
                "blog_url": "https://usserviceanimals.org/blog",
                "is_active": True,
                "content_focus": ["registration", "ESA", "travel"]
            },
            {
                "id": "nsarco",
                "domain": "nsarco.com",
                "name": "National Service Animal Registry",
                "description": "Service animal registration and resources",
                "blog_url": "https://nsarco.com/blog/",
                "is_active": True,
                "content_focus": ["registration", "laws", "rights"]
            },
            {
                "id": "iaadp",
                "domain": "iaadp.org",
                "name": "IAADP",
                "description": "International Association of Assistance Dog Partners",
                "blog_url": "https://iaadp.org/",
                "is_active": True,
                "content_focus": ["advocacy", "rights", "standards"]
            },
            {
                "id": "akc",
                "domain": "akc.org",
                "name": "American Kennel Club",
                "description": "Dog training and breed information",
                "blog_url": "https://akc.org/expert-advice/training/service-dog-training",
                "is_active": True,
                "content_focus": ["training", "breeds", "health"]
            },
            {
                "id": "pawsitivity",
                "domain": "pawsitivityservicedogs.com",
                "name": "Pawsitivity Service Dogs",
                "description": "Service dog training organization",
                "blog_url": "https://pawsitivityservicedogs.com/blog/",
                "is_active": True,
                "content_focus": ["training programs", "success stories", "autism"]
            },
            {
                "id": "4paws",
                "domain": "4pawsforability.org",
                "name": "4 Paws for Ability",
                "description": "Service dogs for children and veterans",
                "blog_url": "https://4pawsforability.org/blog/",
                "is_active": True,
                "content_focus": ["children", "veterans", "disabilities"]
            }
        ]
        
        # Load existing profiles
        self.profiles = self._load_profiles()
        
        # Initialize with defaults if empty
        if not self.profiles:
            self._initialize_defaults()
    
    def _load_profiles(self) -> Dict[str, CompetitorProfile]:
        """Load competitor profiles from storage"""
        if not self.storage_path.exists():
            return {}
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                
            profiles = {}
            for comp_id, comp_data in data.items():
                # Convert datetime strings back to datetime objects
                for date_field in ['last_scanned', 'added_date', 'updated_date']:
                    if date_field in comp_data and comp_data[date_field]:
                        comp_data[date_field] = datetime.fromisoformat(comp_data[date_field])
                
                profiles[comp_id] = CompetitorProfile(**comp_data)
            
            return profiles
        except Exception as e:
            logger.error(f"Failed to load competitor profiles: {e}")
            return {}
    
    def _save_profiles(self):
        """Save competitor profiles to storage"""
        try:
            data = {}
            for comp_id, profile in self.profiles.items():
                profile_dict = profile.dict()
                # Convert datetime objects to strings
                for date_field in ['last_scanned', 'added_date', 'updated_date']:
                    if profile_dict.get(date_field):
                        profile_dict[date_field] = profile_dict[date_field].isoformat()
                data[comp_id] = profile_dict
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.profiles)} competitor profiles")
        except Exception as e:
            logger.error(f"Failed to save competitor profiles: {e}")
    
    def _initialize_defaults(self):
        """Initialize with default competitors"""
        for comp_data in self.default_competitors:
            profile = CompetitorProfile(**comp_data)
            self.profiles[profile.id] = profile
        
        self._save_profiles()
        logger.info(f"Initialized {len(self.default_competitors)} default competitors")
    
    def get_all_competitors(self) -> List[CompetitorProfile]:
        """Get all competitor profiles"""
        return list(self.profiles.values())
    
    def get_active_competitors(self) -> List[CompetitorProfile]:
        """Get only active competitor profiles"""
        return [p for p in self.profiles.values() if p.is_active]
    
    def get_competitor(self, competitor_id: str) -> Optional[CompetitorProfile]:
        """Get a specific competitor profile"""
        return self.profiles.get(competitor_id)
    
    def add_competitor(self, profile: CompetitorProfile) -> bool:
        """Add a new competitor profile"""
        if profile.id in self.profiles:
            logger.warning(f"Competitor {profile.id} already exists")
            return False
        
        profile.added_date = datetime.now()
        profile.updated_date = datetime.now()
        self.profiles[profile.id] = profile
        self._save_profiles()
        
        logger.info(f"Added competitor: {profile.name}")
        return True
    
    def update_competitor(self, competitor_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing competitor profile"""
        if competitor_id not in self.profiles:
            logger.warning(f"Competitor {competitor_id} not found")
            return False
        
        profile = self.profiles[competitor_id]
        
        # Update fields
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.updated_date = datetime.now()
        self._save_profiles()
        
        logger.info(f"Updated competitor: {profile.name}")
        return True
    
    def delete_competitor(self, competitor_id: str) -> bool:
        """Delete a competitor profile"""
        if competitor_id not in self.profiles:
            logger.warning(f"Competitor {competitor_id} not found")
            return False
        
        del self.profiles[competitor_id]
        self._save_profiles()
        
        logger.info(f"Deleted competitor: {competitor_id}")
        return True
    
    def toggle_competitor_status(self, competitor_id: str) -> bool:
        """Toggle active/inactive status of a competitor"""
        if competitor_id not in self.profiles:
            return False
        
        profile = self.profiles[competitor_id]
        profile.is_active = not profile.is_active
        profile.updated_date = datetime.now()
        self._save_profiles()
        
        status = "activated" if profile.is_active else "deactivated"
        logger.info(f"Competitor {profile.name} {status}")
        return True
    
    def update_scan_timestamp(self, competitor_id: str):
        """Update the last scanned timestamp for a competitor"""
        if competitor_id in self.profiles:
            self.profiles[competitor_id].last_scanned = datetime.now()
            self._save_profiles()
    
    def get_competitor_insights(self, competitor_id: str) -> Optional[CompetitorInsight]:
        """Get the latest insights for a competitor"""
        # This would be enhanced to pull from actual scan data
        profile = self.profiles.get(competitor_id)
        if not profile:
            return None
        
        # For now, return mock insights
        return CompetitorInsight(
            competitor_id=competitor_id,
            competitor_name=profile.name,
            scan_date=profile.last_scanned or datetime.now(),
            new_articles_count=5,
            total_articles_scanned=profile.total_articles_found,
            trending_topics=[
                {"topic": t, "score": 85} for t in profile.trending_topics[:5]
            ],
            posting_frequency="3 posts/week",
            average_word_count=1500
        )
    
    def get_all_insights(self) -> List[CompetitorInsight]:
        """Get insights for all active competitors"""
        insights = []
        for profile in self.get_active_competitors():
            insight = self.get_competitor_insights(profile.id)
            if insight:
                insights.append(insight)
        return insights
    
    def get_domains_for_scanning(self) -> List[Dict[str, str]]:
        """Get list of domains and URLs for the scraper"""
        domains = []
        for profile in self.get_active_competitors():
            domain_info = {
                "id": profile.id,
                "domain": profile.domain,
                "name": profile.name,
                "urls": []
            }
            
            if profile.blog_url:
                domain_info["urls"].append(profile.blog_url)
            if profile.news_url:
                domain_info["urls"].append(profile.news_url)
            if profile.resources_url:
                domain_info["urls"].append(profile.resources_url)
            
            # If no specific URLs, use the domain
            if not domain_info["urls"]:
                domain_info["urls"].append(f"https://{profile.domain}")
            
            domains.append(domain_info)
        
        return domains
    
    def export_competitors(self) -> str:
        """Export competitors as JSON"""
        data = {}
        for comp_id, profile in self.profiles.items():
            profile_dict = profile.dict()
            # Convert datetime objects to strings
            for date_field in ['last_scanned', 'added_date', 'updated_date']:
                if profile_dict.get(date_field):
                    profile_dict[date_field] = profile_dict[date_field].isoformat()
            data[comp_id] = profile_dict
        
        return json.dumps(data, indent=2)
    
    def import_competitors(self, json_data: str) -> int:
        """Import competitors from JSON"""
        try:
            data = json.loads(json_data)
            imported = 0
            
            for comp_id, comp_data in data.items():
                # Convert datetime strings
                for date_field in ['last_scanned', 'added_date', 'updated_date']:
                    if date_field in comp_data and comp_data[date_field]:
                        comp_data[date_field] = datetime.fromisoformat(comp_data[date_field])
                
                profile = CompetitorProfile(**comp_data)
                if comp_id not in self.profiles:
                    self.profiles[comp_id] = profile
                    imported += 1
            
            self._save_profiles()
            logger.info(f"Imported {imported} competitors")
            return imported
        except Exception as e:
            logger.error(f"Failed to import competitors: {e}")
            return 0


# Global instance
_competitor_manager = None

def get_competitor_manager() -> CompetitorManager:
    """Get or create the global competitor manager"""
    global _competitor_manager
    if _competitor_manager is None:
        _competitor_manager = CompetitorManager()
    return _competitor_manager