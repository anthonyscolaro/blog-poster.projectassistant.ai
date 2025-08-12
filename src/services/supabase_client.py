"""
Supabase client for authentication and user data management
Works alongside existing Qdrant for vector storage
"""
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import httpx

from src.core.config import settings

logger = logging.getLogger(__name__)


class SupabaseService:
    """
    Handles Supabase authentication and user data
    while keeping Qdrant for vector operations
    """
    
    def __init__(self):
        """Initialize Supabase client"""
        # Use local or cloud Supabase based on environment
        self.url = os.getenv('SUPABASE_URL', 'http://localhost:8000')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not self.anon_key:
            logger.warning("Supabase keys not configured")
            self.client = None
            self.admin_client = None
        else:
            # Public client (for auth)
            self.client: Client = create_client(
                self.url, 
                self.anon_key,
                options=ClientOptions(
                    auto_refresh_token=True,
                    persist_session=True
                )
            )
            
            # Admin client (for server operations)
            self.admin_client: Client = create_client(
                self.url,
                self.service_key or self.anon_key
            )
    
    # ============= Authentication =============
    
    async def sign_up(self, email: str, password: str, full_name: str = None) -> Dict[str, Any]:
        """Register a new user"""
        try:
            sign_up_data = {
                "email": email,
                "password": password
            }
            
            if full_name:
                sign_up_data["options"] = {
                    "data": {
                        "full_name": full_name
                    }
                }
            
            response = self.client.auth.sign_up(sign_up_data)
            
            if response.user:
                # Create user profile
                await self.create_user_profile(response.user.id, email)
                
            return {
                "success": True,
                "user": response.user,
                "session": response.session
            }
        except Exception as e:
            logger.error(f"Sign up failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in existing user"""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "access_token": response.session.access_token if response.session else None
            }
        except Exception as e:
            logger.error(f"Sign in failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def sign_out(self) -> bool:
        """Sign out current user"""
        try:
            self.client.auth.sign_out()
            return True
        except Exception as e:
            logger.error(f"Sign out failed: {e}")
            return False
    
    async def get_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user from JWT token"""
        try:
            response = self.client.auth.get_user(token)
            return response.user if response else None
        except Exception as e:
            logger.error(f"Get user failed: {e}")
            return None
    
    # ============= User Profile Management =============
    
    async def create_user_profile(self, user_id: str, email: str) -> Dict[str, Any]:
        """Create user profile with default settings"""
        try:
            profile_data = {
                "id": user_id,
                "email": email,
                "api_key": self.generate_api_key(),
                "max_articles_per_month": 100,
                "max_cost_per_month": 50.0,
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = self.admin_client.table('profiles').insert(profile_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Create profile failed: {e}")
            return {}
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile data"""
        try:
            response = self.admin_client.table('profiles')\
                .select("*")\
                .eq('id', user_id)\
                .single()\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Get profile failed: {e}")
            return None
    
    # ============= Article Management (Metadata only) =============
    
    async def create_article_metadata(
        self, 
        user_id: str, 
        article_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Store article metadata in Supabase
        (Embeddings go to Qdrant)
        """
        try:
            metadata = {
                "user_id": user_id,
                "title": article_data.get("title"),
                "slug": article_data.get("slug"),
                "excerpt": article_data.get("excerpt"),
                "status": article_data.get("status", "draft"),
                "word_count": article_data.get("word_count", 0),
                "seo_score": article_data.get("seo_score"),
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = self.admin_client.table('articles').insert(metadata).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Create article metadata failed: {e}")
            return {}
    
    async def get_user_articles(
        self, 
        user_id: str, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get user's article metadata"""
        try:
            response = self.admin_client.table('articles')\
                .select("*")\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            logger.error(f"Get user articles failed: {e}")
            return []
    
    # ============= Usage Tracking =============
    
    async def track_usage(
        self, 
        user_id: str, 
        cost: float, 
        tokens: int
    ) -> bool:
        """Track API usage for billing"""
        try:
            usage_data = {
                "user_id": user_id,
                "cost": cost,
                "tokens": tokens,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.admin_client.table('usage').insert(usage_data).execute()
            
            # Check if user exceeded limits
            await self.check_usage_limits(user_id)
            
            return True
        except Exception as e:
            logger.error(f"Track usage failed: {e}")
            return False
    
    async def check_usage_limits(self, user_id: str) -> Dict[str, Any]:
        """Check if user exceeded their limits"""
        try:
            # Get user profile
            profile = await self.get_user_profile(user_id)
            if not profile:
                return {"within_limits": False, "reason": "No profile found"}
            
            # Get current month usage
            from datetime import datetime, timedelta
            start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)
            
            response = self.admin_client.table('usage')\
                .select("cost")\
                .eq('user_id', user_id)\
                .gte('timestamp', start_of_month.isoformat())\
                .execute()
            
            total_cost = sum(item['cost'] for item in response.data)
            max_cost = profile.get('max_cost_per_month', 50.0)
            
            return {
                "within_limits": total_cost < max_cost,
                "current_cost": total_cost,
                "max_cost": max_cost,
                "remaining": max_cost - total_cost
            }
        except Exception as e:
            logger.error(f"Check usage limits failed: {e}")
            return {"within_limits": False, "reason": str(e)}
    
    # ============= Helper Methods =============
    
    def generate_api_key(self) -> str:
        """Generate unique API key for user"""
        import secrets
        return f"bp_{secrets.token_urlsafe(32)}"
    
    async def setup_database_tables(self):
        """
        Create necessary tables in Supabase
        Run this once during setup
        """
        sql_commands = [
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id UUID REFERENCES auth.users PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                api_key TEXT UNIQUE,
                max_articles_per_month INTEGER DEFAULT 100,
                max_cost_per_month DECIMAL(10,2) DEFAULT 50.00,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS articles (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                user_id UUID REFERENCES profiles(id),
                title TEXT NOT NULL,
                slug TEXT NOT NULL,
                excerpt TEXT,
                status TEXT DEFAULT 'draft',
                word_count INTEGER DEFAULT 0,
                seo_score FLOAT,
                wp_post_id INTEGER,
                wp_url TEXT,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(user_id, slug)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS usage (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                user_id UUID REFERENCES profiles(id),
                cost DECIMAL(10,4),
                tokens INTEGER,
                timestamp TIMESTAMP DEFAULT NOW()
            );
            """,
            """
            -- Enable Row Level Security
            ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
            ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
            ALTER TABLE usage ENABLE ROW LEVEL SECURITY;
            """,
            """
            -- Create policies
            CREATE POLICY "Users can view own profile" ON profiles
                FOR SELECT USING (auth.uid() = id);
            
            CREATE POLICY "Users can update own profile" ON profiles
                FOR UPDATE USING (auth.uid() = id);
            
            CREATE POLICY "Users can view own articles" ON articles
                FOR ALL USING (auth.uid() = user_id);
            
            CREATE POLICY "Users can view own usage" ON usage
                FOR SELECT USING (auth.uid() = user_id);
            """
        ]
        
        print("📦 Setting up Supabase tables...")
        # Note: You'll need to run these in Supabase Studio SQL editor
        for sql in sql_commands:
            print(sql)
        print("\n✅ Copy and run these SQL commands in Supabase Studio!")


# Singleton instance
_supabase_service: Optional[SupabaseService] = None


def get_supabase_service() -> SupabaseService:
    """Get or create Supabase service instance"""
    global _supabase_service
    if _supabase_service is None:
        _supabase_service = SupabaseService()
    return _supabase_service