"""
Pipeline Logger Service
Manages real-time logging for pipeline execution with WebSocket streaming
"""
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import logging
from collections import deque

logger = logging.getLogger(__name__)


class LogLevel(str, Enum):
    """Log levels for pipeline messages"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    METRIC = "metric"  # For metrics like keywords, competitors, etc.


class LogEntry:
    """Represents a single log entry"""
    
    def __init__(
        self,
        level: LogLevel,
        message: str,
        agent: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        self.level = level
        self.message = message
        self.agent = agent
        self.data = data or {}
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "level": self.level,
            "message": self.message,
            "agent": self.agent,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }


class PipelineLogger:
    """Manages pipeline execution logs with streaming capability"""
    
    def __init__(self, max_logs: int = 1000):
        self.logs: Dict[str, deque] = {}  # Pipeline ID -> logs
        self.max_logs = max_logs
        self.active_connections: Dict[str, List[Any]] = {}  # Pipeline ID -> WebSocket connections
        self._lock = asyncio.Lock()
    
    async def log(
        self,
        pipeline_id: str,
        level: LogLevel,
        message: str,
        agent: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ):
        """Add a log entry and broadcast to connected clients"""
        async with self._lock:
            # Create log entry
            entry = LogEntry(level, message, agent, data)
            
            # Initialize deque if needed
            if pipeline_id not in self.logs:
                self.logs[pipeline_id] = deque(maxlen=self.max_logs)
            
            # Add to logs
            self.logs[pipeline_id].append(entry)
            
            # Broadcast to connected WebSocket clients
            if pipeline_id in self.active_connections:
                await self._broadcast(pipeline_id, entry)
            
            # Also log to standard logger
            log_msg = f"[{agent or 'SYSTEM'}] {message}"
            if data:
                log_msg += f" | Data: {json.dumps(data, default=str)}"
            
            if level == LogLevel.ERROR:
                logger.error(log_msg)
            elif level == LogLevel.WARNING:
                logger.warning(log_msg)
            elif level == LogLevel.DEBUG:
                logger.debug(log_msg)
            else:
                logger.info(log_msg)
    
    async def _broadcast(self, pipeline_id: str, entry: LogEntry):
        """Broadcast log entry to all connected WebSocket clients"""
        if pipeline_id not in self.active_connections:
            return
        
        message = json.dumps(entry.to_dict(), default=str)
        dead_connections = []
        
        for connection in self.active_connections[pipeline_id]:
            try:
                await connection.send_text(message)
            except Exception:
                dead_connections.append(connection)
        
        # Remove dead connections
        for conn in dead_connections:
            self.active_connections[pipeline_id].remove(conn)
    
    def add_connection(self, pipeline_id: str, websocket):
        """Add a WebSocket connection for a pipeline"""
        if pipeline_id not in self.active_connections:
            self.active_connections[pipeline_id] = []
        self.active_connections[pipeline_id].append(websocket)
    
    def remove_connection(self, pipeline_id: str, websocket):
        """Remove a WebSocket connection"""
        if pipeline_id in self.active_connections:
            if websocket in self.active_connections[pipeline_id]:
                self.active_connections[pipeline_id].remove(websocket)
            if not self.active_connections[pipeline_id]:
                del self.active_connections[pipeline_id]
    
    def get_logs(self, pipeline_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get logs for a pipeline"""
        if pipeline_id not in self.logs:
            return []
        
        logs = list(self.logs[pipeline_id])
        if limit:
            logs = logs[-limit:]
        
        return [log.to_dict() for log in logs]
    
    def clear_logs(self, pipeline_id: str):
        """Clear logs for a pipeline"""
        if pipeline_id in self.logs:
            del self.logs[pipeline_id]
    
    # Convenience methods for different log levels
    async def debug(self, pipeline_id: str, message: str, agent: Optional[str] = None, **data):
        await self.log(pipeline_id, LogLevel.DEBUG, message, agent, data)
    
    async def info(self, pipeline_id: str, message: str, agent: Optional[str] = None, **data):
        await self.log(pipeline_id, LogLevel.INFO, message, agent, data)
    
    async def warning(self, pipeline_id: str, message: str, agent: Optional[str] = None, **data):
        await self.log(pipeline_id, LogLevel.WARNING, message, agent, data)
    
    async def error(self, pipeline_id: str, message: str, agent: Optional[str] = None, **data):
        await self.log(pipeline_id, LogLevel.ERROR, message, agent, data)
    
    async def success(self, pipeline_id: str, message: str, agent: Optional[str] = None, **data):
        await self.log(pipeline_id, LogLevel.SUCCESS, message, agent, data)
    
    async def metric(self, pipeline_id: str, message: str, agent: Optional[str] = None, **data):
        """Log metrics like competitors, keywords, etc."""
        await self.log(pipeline_id, LogLevel.METRIC, message, agent, data)


# Global pipeline logger instance
pipeline_logger = PipelineLogger()