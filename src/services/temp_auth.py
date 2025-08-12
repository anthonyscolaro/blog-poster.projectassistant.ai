"""
Temporary authentication service for development
Uses PostgreSQL directly until Supabase auth is fully setup
"""
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import logging
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TempAuthService:
    """
    Simple authentication service for local development
    This is temporary until Supabase auth stack is fully working
    """
    
    def __init__(self):
        # Use the main database for users table
        self.database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5433/vectors')
        self.jwt_secret = os.getenv('JWT_SECRET', 'your-super-secret-jwt-token-with-at-least-32-characters-long')
        self.engine = create_engine(self.database_url)
        
        # Create users table if it doesn't exist
        self._create_users_table()
    
    def _create_users_table(self):
        """Create users table for temporary auth"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS temp_users (
                        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        full_name VARCHAR(255),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW(),
                        is_active BOOLEAN DEFAULT true,
                        usage_count INTEGER DEFAULT 0,
                        monthly_cost DECIMAL(10,2) DEFAULT 0.00
                    )
                """))
                conn.commit()
                logger.info("Temp users table ready")
        except Exception as e:
            logger.error(f"Error creating users table: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_hex = password_hash.split(':')
            password_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_check.hex() == hash_hex
        except (ValueError, AttributeError):
            return False
    
    def _create_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT token for user"""
        payload = {
            'user_id': str(user_data['id']),
            'email': user_data['email'],
            'exp': datetime.now(timezone.utc) + timedelta(hours=24),
            'iat': datetime.now(timezone.utc),
            'iss': 'blog-poster'
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    async def sign_up(self, email: str, password: str, full_name: str = None) -> Dict[str, Any]:
        """Register a new user"""
        try:
            if len(password) < 8:
                return {
                    "success": False,
                    "error": "Password must be at least 8 characters long"
                }
            
            password_hash = self._hash_password(password)
            
            with self.engine.connect() as conn:
                # Insert new user
                result = conn.execute(text("""
                    INSERT INTO temp_users (email, password_hash, full_name) 
                    VALUES (:email, :password_hash, :full_name)
                    RETURNING id, email, full_name, created_at
                """), {
                    'email': email,
                    'password_hash': password_hash,
                    'full_name': full_name or email.split('@')[0]
                })
                conn.commit()
                
                user_data = result.fetchone()._asdict()
                token = self._create_jwt_token(user_data)
                
                logger.info(f"User registered: {email}")
                return {
                    "success": True,
                    "user": user_data,
                    "access_token": token
                }
                
        except IntegrityError:
            return {
                "success": False,
                "error": "Email already exists"
            }
        except Exception as e:
            logger.error(f"Sign up failed: {e}")
            return {
                "success": False,
                "error": "Registration failed"
            }
    
    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in existing user"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT id, email, password_hash, full_name, is_active
                    FROM temp_users 
                    WHERE email = :email
                """), {'email': email})
                
                user_row = result.fetchone()
                if not user_row:
                    return {
                        "success": False,
                        "error": "Invalid credentials"
                    }
                
                user_data = user_row._asdict()
                
                if not user_data['is_active']:
                    return {
                        "success": False,
                        "error": "Account is disabled"
                    }
                
                if not self._verify_password(password, user_data['password_hash']):
                    return {
                        "success": False,
                        "error": "Invalid credentials"
                    }
                
                # Remove password hash from response
                del user_data['password_hash']
                
                token = self._create_jwt_token(user_data)
                
                logger.info(f"User signed in: {email}")
                return {
                    "success": True,
                    "user": user_data,
                    "access_token": token
                }
                
        except Exception as e:
            logger.error(f"Sign in failed: {e}")
            return {
                "success": False,
                "error": "Sign in failed"
            }
    
    async def get_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user from JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT id, email, full_name, created_at, usage_count, monthly_cost
                    FROM temp_users 
                    WHERE id = :user_id AND is_active = true
                """), {'user_id': user_id})
                
                user_row = result.fetchone()
                if user_row:
                    return user_row._asdict()
                
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
            logger.debug(f"Get user failed: {e}")
            
        return None
    
    async def sign_out(self) -> bool:
        """Sign out (client-side token removal)"""
        # For JWT, logout is handled client-side by removing the token
        return True


# Singleton instance
_temp_auth_service: Optional[TempAuthService] = None


def get_temp_auth_service() -> TempAuthService:
    """Get or create temporary auth service instance"""
    global _temp_auth_service
    if _temp_auth_service is None:
        _temp_auth_service = TempAuthService()
    return _temp_auth_service