"""
Content-related services (fact checking, internal links, etc.)
"""
import logging
from typing import List, Optional, Dict, Any
from pydantic import HttpUrl
from ..models.core import InternalLinkCandidate

logger = logging.getLogger(__name__)


class FactCheckerService:
    """Replace with real retrieval (SERP + vectors) and citation filters."""

    async def search(self, q: str, jurisdiction: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for facts and legal citations
        
        Args:
            q: Query string
            jurisdiction: Legal jurisdiction (optional)
            
        Returns:
            Dictionary with facts, statutes, dates, sources
        """
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
        """
        Resolve internal link recommendations
        
        Args:
            section_summary: Summary of content section
            candidates: Available link candidates
            limit: Maximum number of links to return
            
        Returns:
            List of recommended links with URLs and titles
        """
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