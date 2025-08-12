"""
Tool-related Pydantic models
"""
from typing import Dict, Any
from pydantic import BaseModel


class ToolCall(BaseModel):
    name: str
    args: Dict[str, Any] = {}


class ToolResult(BaseModel):
    name: str
    payload: Dict[str, Any]