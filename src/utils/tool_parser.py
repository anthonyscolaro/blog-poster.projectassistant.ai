"""
Tool call parsing utilities
"""
import re
import json
from typing import List
from ..models.tools import ToolCall

# Tool call parsing patterns
TOOL_TAG_RE = re.compile(r"<tool\s+name=\"([^\"]+)\"([^>]*)/>")
ARG_RE = re.compile(r"(\w+)=\"([^\"]*)\"")


def parse_tool_calls(text: str) -> List[ToolCall]:
    """
    Parse tool calls from text containing <tool .../> tags
    
    Args:
        text: Text containing tool call tags
        
    Returns:
        List of parsed tool calls
    """
    calls: List[ToolCall] = []
    for m in TOOL_TAG_RE.finditer(text or ""):
        name = m.group(1)
        raw = m.group(2)
        args = {k: v for k, v in ARG_RE.findall(raw)}
        # decode JSON-ish args if present
        for k, v in list(args.items()):
            if v and (v.startswith("{") or v.startswith("[")):
                try:
                    args[k] = json.loads(v)
                except Exception:
                    pass
        calls.append(ToolCall(name=name, args=args))
    return calls