"""
Anthropic (Claude) client wrapper
"""
import os
import json
import logging
from typing import Optional, Dict, Any, List
from ..models.tools import ToolResult

logger = logging.getLogger(__name__)

try:
    import anthropic  # type: ignore
except ImportError:  # allow file to run without SDK installed
    anthropic = None


class ClaudeClient:
    """Client wrapper for Anthropic's Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        # Only create client if we have a valid API key (not placeholder)
        if anthropic and self.api_key and not self.api_key.startswith("your-"):
            self.client = anthropic.Client(api_key=self.api_key)
        else:
            self.client = None

    async def complete(self, system_prompt: str, user_json: Dict[str, Any]) -> str:
        """
        Complete a prompt with Claude
        
        Args:
            system_prompt: System prompt
            user_json: User message content as JSON
            
        Returns:
            Generated response text
        """
        if not self.client:
            # Demo: return a fake tool call to show the shim working
            return '<tool name="fact_check.search" q="service dog ADA two questions DOJ" jurisdiction="US"/>'
        
        msg = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": json.dumps(user_json, default=str)}],
        )
        return msg.content[0].text  # type: ignore

    async def continue_with_tool_result(self, history: List[Dict[str, str]], tool_result: ToolResult) -> str:
        """
        Continue conversation with tool result
        
        Args:
            history: Previous conversation messages
            tool_result: Tool execution result
            
        Returns:
            Generated response text
        """
        if not self.client:
            # Demo: after tool result, pretend Claude returns a finished Markdown doc
            return (
                "---\n"
                "title: Example\nslug: example\ncategory: ADA Compliance\n"
                "tags: [service dogs]\nmeta_title: Example Title That Fits\n"
                "meta_desc: This is a meta description with the right length for SEO checks.\n"
                "canonical: https://example.com/example\n"
                "schema_jsonld: {}\nhero_image_prompt: Service dog in restaurant\n"
                "internal_link_targets: []\n"
                "citations: [https://www.ada.gov/resources/service-animals-2010-requirements/]\n---\n\n"
                "# Example\n\nBody...\n"
            )
        
        # When using real SDK, append tool result as a user message the model expects
        msg = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=5000,
            messages=history + [
                {"role": "user", "content": json.dumps({"tool_result": tool_result.model_dump()}, default=str)}
            ],
        )
        return msg.content[0].text  # type: ignore