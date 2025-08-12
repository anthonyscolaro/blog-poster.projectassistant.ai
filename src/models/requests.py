"""
Request and Response Pydantic models
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from .tools import ToolCall, ToolResult


class RunResponse(BaseModel):
    status: str
    output: Optional[str] = None
    tool_calls: List[ToolCall] = []
    tool_results: List[ToolResult] = []
    errors: List[str] = []


class LintRequest(BaseModel):
    frontmatter: Dict[str, Any]
    markdown: str


class LintResponse(BaseModel):
    violations: List[str]


class IndexDocumentRequest(BaseModel):
    content: str
    document_id: str
    title: str
    url: Optional[str] = None
    collection: str = "blog_articles"


class SearchDocumentsRequest(BaseModel):
    query: str
    limit: int = 5
    collection: str = "blog_articles"