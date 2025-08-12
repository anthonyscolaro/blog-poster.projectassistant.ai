"""
Authentication router for Supabase integration
Handles login, registration, and password reset
"""
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging

from src.services.supabase_client import get_supabase_service
from src.services.temp_auth import get_temp_auth_service  # Fallback

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["authentication"])
templates = Jinja2Templates(directory="templates")
security = HTTPBearer(auto_error=False)


def get_auth_service():
    """Get the appropriate auth service (Supabase preferred, temp fallback)"""
    try:
        supabase_service = get_supabase_service()
        if supabase_service.client is not None:
            logger.info("Using Supabase authentication")
            return supabase_service
    except Exception as e:
        logger.warning(f"Supabase not available: {e}")
    
    logger.info("Using temporary authentication fallback")
    return get_temp_auth_service()


# ============= Template Routes =============

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: Optional[str] = None, success: Optional[str] = None):
    """Display login page"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": error,
        "success": success
    })


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, error: Optional[str] = None):
    """Display registration page"""
    return templates.TemplateResponse("register.html", {
        "request": request,
        "error": error
    })


@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(
    request: Request, 
    error: Optional[str] = None, 
    success: Optional[str] = None
):
    """Display forgot password page"""
    return templates.TemplateResponse("forgot-password.html", {
        "request": request,
        "error": error,
        "success": success
    })


# ============= Authentication Endpoints =============

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: Optional[str] = Form(None)
):
    """Handle login form submission"""
    try:
        auth_service = get_auth_service()
        result = await auth_service.sign_in(email, password)
        
        if result["success"]:
            # Set secure cookie with JWT token
            response = RedirectResponse("/dashboard", status_code=303)
            
            # Set token as httponly cookie for security
            max_age = 30 * 24 * 60 * 60 if remember else 24 * 60 * 60  # 30 days or 1 day
            response.set_cookie(
                "access_token",
                result["access_token"],
                httponly=True,
                secure=True,  # Use HTTPS in production
                samesite="lax",
                max_age=max_age
            )
            
            logger.info(f"User logged in successfully: {email}")
            return response
        else:
            # Return to login page with error
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": result.get("error", "Invalid credentials")
            }, status_code=400)
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "An error occurred. Please try again."
        }, status_code=500)


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    terms: Optional[str] = Form(None)
):
    """Handle registration form submission"""
    try:
        # Validate form data
        if password != confirm_password:
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "Passwords do not match"
            }, status_code=400)
        
        if not terms:
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "You must accept the terms of service"
            }, status_code=400)
        
        if len(password) < 8:
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "Password must be at least 8 characters long"
            }, status_code=400)
        
        # Create user with temp auth service
        auth_service = get_auth_service()
        result = await auth_service.sign_up(email, password)
        
        if result["success"]:
            logger.info(f"User registered successfully: {email}")
            # Redirect to login with success message
            return RedirectResponse(
                "/auth/login?success=Account created! Please check your email to verify.",
                status_code=303
            )
        else:
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": result.get("error", "Registration failed")
            }, status_code=400)
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "An error occurred. Please try again."
        }, status_code=500)


@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    email: str = Form(...)
):
    """Handle password reset form submission"""
    try:
        auth_service = get_temp_auth_service()
        
        # For temp auth, just return success (no email functionality yet)
        # In production, this would send an actual email
        
        logger.info(f"Password reset requested for: {email}")
        
        # Always show success to prevent email enumeration
        return templates.TemplateResponse("forgot-password.html", {
            "request": request,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        return templates.TemplateResponse("forgot-password.html", {
            "request": request,
            "error": "An error occurred. Please try again."
        }, status_code=500)


@router.get("/logout")
async def logout():
    """Handle logout"""
    try:
        auth_service = get_auth_service()
        await auth_service.sign_out()
        
        response = RedirectResponse("/auth/login?success=You have been logged out", status_code=303)
        response.delete_cookie("access_token")
        
        return response
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return RedirectResponse("/auth/login", status_code=303)


# ============= Authentication Dependency =============

async def get_current_user(
    request: Request, 
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Get current authenticated user
    Supports both Authorization header and cookie
    """
    token = None
    
    # Try Authorization header first
    if credentials:
        token = credentials.credentials
    
    # Fallback to cookie
    if not token:
        token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        auth_service = get_auth_service()
        user = await auth_service.get_user(token)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user
        
    except Exception as e:
        logger.error(f"Auth verification error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Get current user but don't require authentication
    Returns None if not authenticated
    """
    try:
        return await get_current_user(request, credentials)
    except HTTPException:
        return None


# ============= API Endpoints =============

@router.get("/me")
async def get_current_user_info(current_user=Depends(get_current_user)):
    """Get current user information"""
    return {
        "user": current_user,
        "authenticated": True
    }


@router.get("/check")
async def check_auth(current_user=Depends(get_current_user_optional)):
    """Check if user is authenticated"""
    return {
        "authenticated": current_user is not None,
        "user": current_user
    }