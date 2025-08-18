"""
Response middleware to automatically wrap API responses in standard format
"""
import json
import logging
from typing import Any, Dict
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.models.responses import ApiResponse, ErrorResponse

logger = logging.getLogger(__name__)


class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    """
    Middleware to automatically wrap API responses in standard format
    Only applies to /api routes
    """
    
    async def dispatch(self, request: Request, call_next):
        # Only wrap API routes
        if not request.url.path.startswith('/api/'):
            return await call_next(request)
        
        # Skip for websocket connections
        if request.url.path.startswith('/api/v1/ws/'):
            return await call_next(request)
        
        try:
            # Process the request
            response = await call_next(request)
            
            # Only wrap successful JSON responses
            if response.status_code < 400 and response.headers.get('content-type', '').startswith('application/json'):
                # Read the response body
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                try:
                    # Parse the original response
                    original_data = json.loads(body.decode())
                    
                    # Check if already wrapped (avoid double wrapping)
                    if isinstance(original_data, dict) and 'success' in original_data and 'data' in original_data:
                        # Already in correct format
                        return Response(
                            content=body,
                            status_code=response.status_code,
                            headers=dict(response.headers),
                            media_type="application/json"
                        )
                    
                    # Wrap in standard format
                    wrapped_response = ApiResponse(
                        data=original_data,
                        message="Success",
                        success=True
                    )
                    
                    # Return wrapped response
                    return JSONResponse(
                        content=json.loads(wrapped_response.json(by_alias=True)),
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )
                    
                except json.JSONDecodeError:
                    # If not JSON, return as-is
                    return Response(
                        content=body,
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )
            
            # For error responses, ensure they follow error format
            elif response.status_code >= 400 and response.headers.get('content-type', '').startswith('application/json'):
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                try:
                    original_data = json.loads(body.decode())
                    
                    # Check if already in error format
                    if isinstance(original_data, dict) and 'success' in original_data:
                        return Response(
                            content=body,
                            status_code=response.status_code,
                            headers=dict(response.headers),
                            media_type="application/json"
                        )
                    
                    # Wrap in error format
                    error_response = ErrorResponse(
                        message=original_data.get('detail', 'An error occurred'),
                        errors=[original_data.get('detail', str(original_data))],
                        error_code=f"HTTP_{response.status_code}"
                    )
                    
                    return JSONResponse(
                        content=json.loads(error_response.json()),
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )
                    
                except json.JSONDecodeError:
                    return Response(
                        content=body,
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in response wrapper middleware: {e}")
            # Return error in standard format
            error_response = ErrorResponse(
                message="Internal server error",
                errors=[str(e)],
                error_code="INTERNAL_ERROR"
            )
            
            return JSONResponse(
                content=json.loads(error_response.json()),
                status_code=500
            )


def should_wrap_response(path: str) -> bool:
    """
    Determine if a path should have its response wrapped
    """
    # Don't wrap these paths
    skip_paths = [
        '/docs',
        '/openapi.json',
        '/redoc',
        '/health',
        '/favicon.ico',
        '/static'
    ]
    
    for skip_path in skip_paths:
        if path.startswith(skip_path):
            return False
    
    # Only wrap API routes
    return path.startswith('/api/')


class OrganizationContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add organization context to all database queries
    """
    
    async def dispatch(self, request: Request, call_next):
        # Get user from request state (set by auth middleware)
        user = getattr(request.state, 'user', None)
        
        if user and user.get('organization_id'):
            # Add organization context for database queries
            request.state.organization_id = user['organization_id']
            
            # Add to response headers for debugging
            response = await call_next(request)
            response.headers['X-Organization-ID'] = user['organization_id']
            return response
        
        return await call_next(request)