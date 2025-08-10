"""
FastAPI tool shim that orchestrates Claude 3.5 Sonnet with:
- Verifiable slot completion via <tool .../> tags
- Internal link resolver
- SEO lint checker
- Strong Pydantic contracts for inputs/outputs

This file is self-contained for a demo. Replace stubbed services (fact checker, links, vector search) with real implementations.

Run:
  uvicorn app:app --reload --port 8088

Env (example):
  ANTHROPIC_API_KEY=...
  VECTOR_BACKEND=qdrant|convex|memory
  QDRANT_URL=http://localhost:6333
"""
from __future__ import annotations

import os
import re
import json
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field, validator

# ------------------------------
# Pydantic Contracts
# ------------------------------

class InternalLinkCandidate(BaseModel):
    url: HttpUrl
    title: str
    embedding_id: Optional[str] = None
    brief_summary: Optional[str] = None

class TopicRec(BaseModel):
    topic_slug: str
    primary_kw: str
    secondary_kws: List[str] = []
    title_variants: List[str] = []
    rationale: Optional[str] = None
    supporting_urls: List[HttpUrl] = []
    score_breakdown: Dict[str, float] = {}
    risk_flags: List[str] = []

class BrandStyle(BaseModel):
    voice: str = "clear, empathetic"
    audience: str = "general public"
    tone: str = "confident"
    reading_grade_target: int = 8
    banned_phrases: List[str] = []

class SiteInfo(BaseModel):
    site_url: HttpUrl
    canonical_base: HttpUrl
    category_map: Dict[str, int]
    internal_link_candidates: List[InternalLinkCandidate] = []

class SerpItem(BaseModel):
    url: HttpUrl
    title: str
    h1: Optional[str] = None
    h2s: List[str] = []
    meta_desc: Optional[str] = None

class CompetitorChunk(BaseModel):
    url: HttpUrl
    text: str
    chunk_id: str

class Evidence(BaseModel):
    facts: List[str] = []
    statutes: List[str] = []  # e.g., "28 CFR §36.302(c)"
    dates: List[str] = []     # human-readable dates or ISO
    sources: List[HttpUrl] = []
    serp_snapshot: List[SerpItem] = []
    competitor_chunks: List[CompetitorChunk] = []

class Constraints(BaseModel):
    min_words: int = 1500
    max_words: int = 2500
    image_policy: str = "stock_or_generated_ok"
    require_disclaimer: bool = True
    disallow_competitor_links: bool = True

class InputsEnvelope(BaseModel):
    topic_rec: TopicRec
    brand_style: BrandStyle
    site_info: SiteInfo
    evidence: Evidence
    constraints: Constraints

class ArticleDraft(BaseModel):
    title: str
    slug: str
    category: str
    tags: List[str]
    meta_title: str
    meta_desc: str
    canonical: HttpUrl
    schema_jsonld: Dict[str, Any]
    hero_image_prompt: str
    internal_link_targets: List[HttpUrl]
    citations: List[HttpUrl]
    markdown: str

# Tool call parsing
class ToolCall(BaseModel):
    name: str
    args: Dict[str, Any] = {}

class ToolResult(BaseModel):
    name: str
    payload: Dict[str, Any]

# ------------------------------
# Simple tool tag parser
# ------------------------------
TOOL_TAG_RE = re.compile(r"<tool\s+name=\"([^\"]+)\"([^>]*)/>")
ARG_RE = re.compile(r"(\w+)=\"([^\"]*)\"")


def parse_tool_calls(text: str) -> List[ToolCall]:
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


# ------------------------------
# Stubbed Services (replace with real)
# ------------------------------

class FactCheckerService:
    """Replace with real retrieval (SERP + vectors) and citation filters."""

    async def search(self, q: str, jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        # Demo payload: return authoritative ADA sources when query hints ADA
        results = {
            "facts": [
                "The ADA does not require service dog registration or certification.",
                "Businesses may ask only two questions to determine if the dog is a service animal." 
            ],
            "statutes": ["28 CFR §36.302(c)", "28 CFR §35.136"],
            "dates": ["2010-07-23"],
            "sources": [
                "https://www.ada.gov/resources/service-animals-2010-requirements/",
                "https://www.ecfr.gov/current/title-28/part-36/section-36.302",
                "https://www.ada.gov/resources/service-animals-faqs/"
            ],
        }
        return results


class InternalLinkService:
    """Resolve internal links from provided candidates. In production, back this with vectors."""

    async def resolve(self, section_summary: str, candidates: List[InternalLinkCandidate], limit: int = 3) -> List[Dict[str, Any]]:
        # naive scoring by token overlap; replace with ANN/vector search
        tokens = set(section_summary.lower().split())
        scored = []
        for c in candidates:
            score = sum(1 for t in tokens if t in (c.title or '').lower())
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = [
            {"url": str(c.url), "title": c.title}
            for score, c in scored[:limit] if score > 0
        ]
        return top


class SeoLintService:
    """Basic lints. Expand as needed."""

    async def lint(self, frontmatter: Dict[str, Any], markdown: str) -> List[str]:
        errs: List[str] = []
        title = frontmatter.get("meta_title", "")
        meta = frontmatter.get("meta_desc", "")
        if not (45 <= len(title) <= 60):
            errs.append(f"meta_title length {len(title)} out of 45–60")
        if not (140 <= len(meta) <= 160):
            errs.append(f"meta_desc length {len(meta)} out of 140–160")
        # H1 count
        h1s = re.findall(r"^#\s+.+$", markdown, flags=re.MULTILINE)
        if len(h1s) != 1:
            errs.append(f"expected exactly 1 H1, found {len(h1s)}")
        # Image alt check: ![alt](url)
        for m in re.finditer(r"!\[(.*?)\]\((.*?)\)", markdown):
            if not m.group(1).strip():
                errs.append("image missing alt text")
        # Canonical present
        if not frontmatter.get("canonical"):
            errs.append("canonical missing")
        return errs


fact_checker = FactCheckerService()
linker = InternalLinkService()
seo_lint = SeoLintService()

# ------------------------------
# Anthropic (Claude) client wrapper
# ------------------------------
try:
    import anthropic  # type: ignore
except ImportError:  # allow file to run without SDK installed
    anthropic = None


class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        # Only create client if we have a valid API key (not placeholder)
        if anthropic and self.api_key and not self.api_key.startswith("your-"):
            self.client = anthropic.Client(api_key=self.api_key)
        else:
            self.client = None

    async def complete(self, system_prompt: str, user_json: Dict[str, Any]) -> str:
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


claude = ClaudeClient()

# ------------------------------
# FastAPI App
# ------------------------------
app = FastAPI(title="Article Agent Tool Shim")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    # Include the WordPress publishing router providing /publish/wp
    from fast_api_tool_shim_pydantic_schemas_for_article_generation_agent_updated import (
        router as publish_router,
    )
    app.include_router(publish_router)
except Exception:
    # Router is optional; the app can run without it if dependencies are missing
    publish_router = None  # type: ignore


@app.get("/health")
async def health() -> Dict[str, Any]:
    """Simple health endpoint for container checks."""
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


class RunResponse(BaseModel):
    status: str
    output: Optional[str] = None
    tool_calls: List[ToolCall] = []
    tool_results: List[ToolResult] = []
    errors: List[str] = []


@app.post("/agent/run", response_model=RunResponse)
async def run_agent(payload: InputsEnvelope):
    """Kick off a single-shot generation. If the model asks for tools, resolve them, feed back, and return the final Markdown."""
    # 1) Load system prompt from file or environment
    system_prompt_file = os.getenv("SYSTEM_PROMPT_FILE")
    if system_prompt_file and os.path.exists(system_prompt_file):
        with open(system_prompt_file, 'r') as f:
            system_prompt = f.read()
    else:
        system_prompt = os.getenv("SYSTEM_PROMPT", "(inject the system prompt from your initial.md here)")
    first = await claude.complete(system_prompt, user_json=payload.dict())

    tool_calls = parse_tool_calls(first)
    tool_results: List[ToolResult] = []

    if not tool_calls:
        # return what we got (ideally the full Markdown)
        return RunResponse(status="ok", output=first)

    # 2) Resolve tools (sequentially for simplicity)
    for call in tool_calls:
        if call.name == "fact_check.search":
            q = call.args.get("q", "")
            jurisdiction = call.args.get("jurisdiction")
            data = await fact_checker.search(q=q, jurisdiction=jurisdiction)
            tool_results.append(ToolResult(name=call.name, payload=data))
        elif call.name == "links.resolve":
            section = call.args.get("section", "")
            top = await linker.resolve(section_summary=section, candidates=payload.site_info.internal_link_candidates)
            tool_results.append(ToolResult(name=call.name, payload={"links": top}))
        elif call.name == "seo.lint":
            # Expect frontmatter + markdown in args (JSON-encoded strings)
            fm = call.args.get("frontmatter")
            md = call.args.get("markdown", "")
            if isinstance(fm, str):
                try:
                    fm = json.loads(fm)
                except Exception:
                    fm = {}
            errs = await seo_lint.lint(frontmatter=fm or {}, markdown=md or "")
            tool_results.append(ToolResult(name=call.name, payload={"violations": errs}))
        else:
            raise HTTPException(400, f"Unknown tool: {call.name}")

    # 3) Feed result(s) back to Claude and get the final output
    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(payload.dict(), default=str)},
        {"role": "assistant", "content": first},
    ]

    # In a real chain, you might feed results one-by-one and loop until no <tool/> tags remain.
    # For demo, bundle them.
    final_text = await claude.continue_with_tool_result(history, tool_result=ToolResult(name="batch", payload={"results": [tr.dict() for tr in tool_results]}))

    # Optional: run one last SEO lint here and, if violations, you could loop back for fixes

    return RunResponse(status="ok", output=final_text, tool_calls=tool_calls, tool_results=tool_results)


# ------------------------------
# Optional: simple endpoint to lint a draft post-hoc
# ------------------------------
class LintRequest(BaseModel):
    frontmatter: Dict[str, Any]
    markdown: str

class LintResponse(BaseModel):
    violations: List[str]

@app.post("/seo/lint", response_model=LintResponse)
async def lint_endpoint(req: LintRequest):
    v = await seo_lint.lint(req.frontmatter, req.markdown)
    return LintResponse(violations=v)


# ------------------------------
# Dev harness
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8088, reload=True)
