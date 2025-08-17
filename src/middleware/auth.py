"""
JWT Authentication Middleware for FastAPI
Validates Supabase JWT tokens and adds organization context
"""
import os
import logging
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError as JWTError
from supabase import create_client, Client
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Security scheme for Swagger UI
security = HTTPBearer(auto_error=False)


class JWTAuthMiddleware:
    """
    JWT authentication middleware for multi-tenant access control
    """
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', '')
        self.supabase_anon_key = os.getenv('SUPABASE_ANON_KEY', '')
        self.supabase_jwt_secret = os.getenv('SUPABASE_JWT_SECRET', '')
        
        if not all([self.supabase_url, self.supabase_anon_key]):
            logger.warning("Supabase credentials not configured - auth will be disabled")
            self.enabled = False
        else:
            self.enabled = True
            self.supabase: Client = create_client(self.supabase_url, self.supabase_anon_key)
    
    async def validate_token(self, credentials: Optional[HTTPAuthorizationCredentials]) -> Optional[Dict[str, Any]]:
        """
        Validate JWT token and return user claims
        """
        if not self.enabled:
            # Return mock user for development
            return {
                "sub": "dev-user-id",
                "email": "dev@example.com",
                "organization_id": "dev-org",
                "role": "admin"
            }
        
        if not credentials:
            return None
        
        try:
            # Decode and verify JWT
            payload = jwt.decode(
                credentials.credentials,
                self.supabase_jwt_secret,
                algorithms=["HS256"],
                audience="authenticated"
            )
            
            # Check expiration
            exp = payload.get('exp')
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired"
                )
            
            # Get user profile with organization
            user_id = payload.get('sub')
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token structure"
                )
            
            # Fetch user profile and organization from database
            user_data = await self._get_user_profile(user_id)
            
            return {
                "sub": user_id,
                "email": payload.get('email'),
                "organization_id": user_data.get('organization_id'),
                "role": user_data.get('role', 'viewer'),
                "permissions": self._get_role_permissions(user_data.get('role', 'viewer'))
            }
            
        except JWTError as e:
            logger.error(f"JWT validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
    
    async def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch user profile with organization from Supabase
        """
        try:
            # Updated to match frontend's expected query structure
            response = self.supabase.table('profiles').select(
                """
                *,
                organizations (*)
                """
            ).eq('id', user_id).single().execute()
            
            if response.data:
                profile = response.data
                return {
                    'organization_id': profile.get('organization_id'),
                    'role': profile.get('role', 'viewer'),
                    'full_name': profile.get('full_name'),
                    'organization': profile.get('organizations', {}),
                    'onboarding_completed': profile.get('onboarding_completed', False),
                    'two_factor_enabled': profile.get('two_factor_enabled', False)
                }
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
        
        return {'role': 'viewer', 'onboarding_completed': False}
    
    def _get_role_permissions(self, role: str) -> Dict[str, bool]:
        """
        Get permissions based on user role
        """
        permissions_map = {
            'owner': {
                'read': True,
                'write': True,
                'delete': True,
                'billing': True,
                'admin': True,
                'invite_users': True,
                'manage_organization': True
            },
            'admin': {
                'read': True,
                'write': True,
                'delete': True,
                'billing': False,
                'admin': True,
                'invite_users': True,
                'manage_organization': False
            },
            'editor': {
                'read': True,
                'write': True,
                'delete': False,
                'billing': False,
                'admin': False,
                'invite_users': False,
                'manage_organization': False
            },
            'viewer': {
                'read': True,
                'write': False,
                'delete': False,
                'billing': False,
                'admin': False,
                'invite_users': False,
                'manage_organization': False
            }
        }
        
        return permissions_map.get(role, permissions_map['viewer'])
    
    def require_permission(self, permission: str):
        """
        Decorator to require specific permission for an endpoint
        """
        def decorator(func):
            async def wrapper(request: Request, *args, **kwargs):
                user = getattr(request.state, 'user', None)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )
                
                permissions = user.get('permissions', {})
                if not permissions.get(permission, False):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permission '{permission}' required"
                    )
                
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    def require_role(self, min_role: str):
        """
        Decorator to require minimum role level
        """
        role_hierarchy = {
            'viewer': 0,
            'editor': 1,
            'admin': 2,
            'owner': 3
        }
        
        def decorator(func):
            async def wrapper(request: Request, *args, **kwargs):
                user = getattr(request.state, 'user', None)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )
                
                user_role = user.get('role', 'viewer')
                if role_hierarchy.get(user_role, 0) < role_hierarchy.get(min_role, 0):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Role '{min_role}' or higher required"
                    )
                
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator


# Global auth middleware instance
auth_middleware = JWTAuthMiddleware()


async def add_auth_to_request(request: Request, call_next):
    """
    Middleware to add authentication to request state
    """
    # Skip auth for health checks and public endpoints
    if request.url.path in ['/health', '/api/v1/health', '/docs', '/openapi.json']:
        return await call_next(request)
    
    # Extract token from header
    auth_header = request.headers.get('Authorization')
    credentials = None
    if auth_header and auth_header.startswith('Bearer '):
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=auth_header.split(' ')[1]
        )
    
    # Validate token and add user to request
    user_data = await auth_middleware.validate_token(credentials)
    request.state.user = user_data
    
    # Add organization context to all database queries
    if user_data and user_data.get('organization_id'):
        request.state.organization_id = user_data['organization_id']
    
    response = await call_next(request)
    return response