"""
WebSocket endpoints for real-time updates
Publishes updates to Supabase for real-time subscriptions
"""
import logging
import json
import asyncio
from typing import Dict, Set, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from supabase import create_client, Client
from datetime import datetime
import os

from src.services.pipeline_logger import pipeline_logger

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["WebSocket"])

# Track active connections per pipeline
active_connections: Dict[str, Set[WebSocket]] = {}

# Security for WebSocket authentication
security = HTTPBearer(auto_error=False)

# Initialize Supabase client for publishing updates
supabase_client: Optional[Client] = None
if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_SERVICE_KEY'):
    supabase_client = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_SERVICE_KEY')  # Use service key for backend operations
    )
    logger.info("Supabase client initialized for real-time updates")
else:
    logger.warning("Supabase credentials not configured - real-time updates disabled")


async def verify_ws_token(token: str) -> Dict:
    """
    Verify WebSocket connection token
    """
    try:
        # Get JWT secret from environment
        jwt_secret = os.getenv('SUPABASE_JWT_SECRET', '')
        
        if not jwt_secret:
            # Development mode - return mock user
            return {
                "sub": "dev-user-id",
                "organization_id": "dev-org"
            }
        
        # Decode JWT
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=["HS256"],
            audience="authenticated"
        )
        
        return {
            "sub": payload.get('sub'),
            "organization_id": payload.get('organization_id', 'default')
        }
        
    except JWTError as e:
        logger.error(f"WebSocket JWT validation error: {e}")
        return None


@router.websocket("/pipeline/{pipeline_id}")
async def pipeline_websocket(
    websocket: WebSocket,
    pipeline_id: str,
    token: str = Query(None)  # Token passed as query param for WebSocket
):
    """
    WebSocket endpoint for real-time pipeline updates
    
    Connect with: ws://localhost:8088/api/v1/ws/pipeline/{pipeline_id}?token={jwt_token}
    """
    # Verify authentication
    user_data = None
    if token:
        user_data = await verify_ws_token(token)
    
    if not user_data:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    # Accept connection
    await websocket.accept()
    
    # Add to active connections
    if pipeline_id not in active_connections:
        active_connections[pipeline_id] = set()
    active_connections[pipeline_id].add(websocket)
    
    # Register with pipeline logger
    pipeline_logger.add_connection(pipeline_id, websocket)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "pipeline_id": pipeline_id,
            "message": f"Connected to pipeline {pipeline_id}"
        })
        
        # Send current logs if any exist
        existing_logs = pipeline_logger.get_logs(pipeline_id, limit=50)
        if existing_logs:
            await websocket.send_json({
                "type": "history",
                "logs": existing_logs
            })
        
        # Keep connection alive and handle incoming messages
        while True:
            # Wait for any message from client (ping/pong or commands)
            data = await websocket.receive_text()
            
            # Handle ping/pong for connection keepalive
            if data == "ping":
                await websocket.send_text("pong")
            
            # Handle other commands if needed
            elif data.startswith("{"):
                try:
                    message = json.loads(data)
                    await handle_client_message(websocket, pipeline_id, message, user_data)
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid JSON message"
                    })
                    
    except WebSocketDisconnect:
        # Clean up on disconnect
        if pipeline_id in active_connections:
            active_connections[pipeline_id].discard(websocket)
            if not active_connections[pipeline_id]:
                del active_connections[pipeline_id]
        
        # Remove from pipeline logger
        pipeline_logger.remove_connection(pipeline_id, websocket)
        
        logger.info(f"WebSocket disconnected for pipeline {pipeline_id}")
        
    except Exception as e:
        logger.error(f"WebSocket error for pipeline {pipeline_id}: {e}")
        await websocket.close(code=4000, reason=str(e))
        
        # Clean up
        if pipeline_id in active_connections:
            active_connections[pipeline_id].discard(websocket)
        pipeline_logger.remove_connection(pipeline_id, websocket)


async def handle_client_message(
    websocket: WebSocket,
    pipeline_id: str,
    message: Dict,
    user_data: Dict
):
    """
    Handle messages from WebSocket client
    """
    msg_type = message.get('type')
    
    if msg_type == 'pause':
        # Handle pause request
        await websocket.send_json({
            "type": "control",
            "action": "pause",
            "status": "acknowledged",
            "message": "Pipeline pause requested"
        })
        # TODO: Implement actual pipeline pause logic
        
    elif msg_type == 'resume':
        # Handle resume request
        await websocket.send_json({
            "type": "control",
            "action": "resume",
            "status": "acknowledged",
            "message": "Pipeline resume requested"
        })
        # TODO: Implement actual pipeline resume logic
        
    elif msg_type == 'cancel':
        # Handle cancel request
        await websocket.send_json({
            "type": "control",
            "action": "cancel",
            "status": "acknowledged",
            "message": "Pipeline cancellation requested"
        })
        # TODO: Implement actual pipeline cancellation logic
        
    elif msg_type == 'get_status':
        # Send current pipeline status
        # TODO: Get actual status from pipeline manager
        await websocket.send_json({
            "type": "status",
            "pipeline_id": pipeline_id,
            "status": "running",
            "progress": 0.5,
            "current_agent": "Article Generation Agent"
        })
        
    else:
        # Unknown message type
        await websocket.send_json({
            "type": "error",
            "message": f"Unknown message type: {msg_type}"
        })


@router.websocket("/notifications")
async def notifications_websocket(
    websocket: WebSocket,
    token: str = Query(None)
):
    """
    WebSocket endpoint for general notifications
    
    Connect with: ws://localhost:8088/api/v1/ws/notifications?token={jwt_token}
    """
    # Verify authentication
    user_data = None
    if token:
        user_data = await verify_ws_token(token)
    
    if not user_data:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    # Accept connection
    await websocket.accept()
    
    organization_id = user_data.get('organization_id')
    user_id = user_data.get('sub')
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "message": "Connected to notifications stream"
        })
        
        # Keep connection alive
        while True:
            # Wait for ping or other messages
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        logger.info(f"Notifications WebSocket disconnected for user {user_id}")
        
    except Exception as e:
        logger.error(f"Notifications WebSocket error: {e}")
        await websocket.close(code=4000, reason=str(e))


# Helper function to broadcast to all connections
async def broadcast_to_pipeline(pipeline_id: str, message: Dict):
    """
    Broadcast a message to all WebSocket connections for a pipeline
    Also publishes to Supabase for real-time subscriptions
    """
    # Publish to Supabase first (primary method)
    if message.get("type") == "execution_update":
        await publish_pipeline_update(pipeline_id, message.get("data", {}))
    elif message.get("type") == "log":
        await publish_pipeline_log(
            pipeline_id,
            message.get("agent", "system"),
            message.get("level", "info"),
            message.get("message", ""),
            message.get("metadata", {})
        )
    
    # Backward compatibility: broadcast to WebSocket connections
    if pipeline_id in active_connections:
        disconnected = []
        
        for websocket in active_connections[pipeline_id]:
            try:
                await websocket.send_json(message)
            except:
                disconnected.append(websocket)
        
        # Clean up disconnected sockets
        for ws in disconnected:
            active_connections[pipeline_id].discard(ws)


# Supabase publishing functions
async def publish_pipeline_update(execution_id: str, data: Dict):
    """
    Publish pipeline execution update to Supabase
    """
    if not supabase_client:
        logger.debug("Supabase client not configured, skipping publish")
        return
    
    try:
        # Update the pipeline execution record
        data['updated_at'] = datetime.utcnow().isoformat()
        
        result = await asyncio.to_thread(
            lambda: supabase_client.table('pipeline_executions')
            .update(data)
            .eq('id', execution_id)
            .execute()
        )
        
        logger.info(f"Published pipeline update to Supabase: {execution_id}")
        
    except Exception as e:
        logger.error(f"Error publishing to Supabase: {e}")


async def publish_pipeline_log(
    execution_id: str,
    agent_name: str,
    level: str,
    message: str,
    metadata: Dict = None
):
    """
    Publish pipeline log entry to Supabase
    """
    if not supabase_client:
        logger.debug("Supabase client not configured, skipping log publish")
        return
    
    try:
        log_entry = {
            "execution_id": execution_id,
            "agent_name": agent_name,
            "level": level,
            "message": message,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = await asyncio.to_thread(
            lambda: supabase_client.table('pipeline_logs')
            .insert(log_entry)
            .execute()
        )
        
        logger.debug(f"Published log to Supabase: {agent_name} - {message[:50]}")
        
    except Exception as e:
        logger.error(f"Error publishing log to Supabase: {e}")


async def update_pipeline_status(
    execution_id: str,
    status: str,
    current_agent: str = None,
    error_message: str = None
):
    """
    Update pipeline execution status using Supabase RPC function
    """
    if not supabase_client:
        logger.debug("Supabase client not configured, skipping status update")
        return
    
    try:
        params = {
            'p_execution_id': execution_id,
            'p_status': status
        }
        
        if current_agent:
            params['p_current_agent'] = current_agent
        if error_message:
            params['p_error_message'] = error_message
        
        result = await asyncio.to_thread(
            lambda: supabase_client.rpc('update_pipeline_status', params).execute()
        )
        
        logger.info(f"Updated pipeline status in Supabase: {execution_id} -> {status}")
        
    except Exception as e:
        logger.error(f"Error updating pipeline status: {e}")


async def complete_pipeline_agent(
    execution_id: str,
    agent_name: str,
    cost: float = 0
):
    """
    Mark an agent as completed using Supabase RPC function
    """
    if not supabase_client:
        logger.debug("Supabase client not configured, skipping agent completion")
        return
    
    try:
        result = await asyncio.to_thread(
            lambda: supabase_client.rpc('complete_pipeline_agent', {
                'p_execution_id': execution_id,
                'p_agent_name': agent_name,
                'p_cost': cost
            }).execute()
        )
        
        logger.info(f"Marked agent as completed in Supabase: {agent_name} (cost: ${cost})")
        
    except Exception as e:
        logger.error(f"Error completing agent: {e}")