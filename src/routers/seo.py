"""
SEO lint and validation endpoints
"""
import re
import logging
from typing import Dict, Any, List
from fastapi import APIRouter

from ..models import LintRequest, LintResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/seo", tags=["seo"])


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


seo_lint = SeoLintService()


@router.post("/lint", response_model=LintResponse)
async def lint_endpoint(req: LintRequest):
    """Lint content for SEO compliance"""
    v = await seo_lint.lint(req.frontmatter, req.markdown)
    return LintResponse(violations=v)