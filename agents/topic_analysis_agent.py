"""
Topic Analysis Agent - Identifies SEO opportunities and content gaps

This agent analyzes competitor content, search trends, and keyword opportunities
to recommend high-value topics for article generation.
"""
import os
import re
import json
import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict

from pydantic import BaseModel, Field
import httpx
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class KeywordData(BaseModel):
    """Data about a specific keyword"""
    keyword: str
    search_volume: Optional[int] = None
    difficulty: Optional[float] = None
    trend: Optional[str] = None  # "rising", "stable", "declining"
    intent: Optional[str] = None  # "informational", "transactional", "navigational"
    related_keywords: List[str] = Field(default_factory=list)


class ContentGap(BaseModel):
    """Identified content gap opportunity"""
    topic: str
    gap_type: str  # "missing", "outdated", "incomplete", "underserved"
    competitors_covering: List[str] = Field(default_factory=list)
    estimated_traffic_potential: Optional[int] = None
    difficulty_score: float = Field(ge=0.0, le=1.0)
    opportunity_score: float = Field(ge=0.0, le=1.0)
    rationale: str


class TopicRecommendation(BaseModel):
    """Recommended topic for content creation"""
    title: str
    slug: str
    primary_keyword: str
    secondary_keywords: List[str] = Field(default_factory=list)
    content_type: str  # "guide", "how-to", "listicle", "comparison", "faq"
    target_word_count: int
    estimated_difficulty: float = Field(ge=0.0, le=1.0)
    estimated_impact: float = Field(ge=0.0, le=1.0)
    priority_score: float = Field(ge=0.0, le=100.0)
    rationale: str
    competitor_examples: List[str] = Field(default_factory=list)
    content_outline: List[str] = Field(default_factory=list)


class TopicAnalysisReport(BaseModel):
    """Complete topic analysis report"""
    analyzed_at: datetime = Field(default_factory=datetime.now)
    keywords_analyzed: int
    content_gaps_found: int
    topics_recommended: int
    keyword_data: List[KeywordData]
    content_gaps: List[ContentGap]
    recommendations: List[TopicRecommendation]
    market_insights: Dict[str, Any] = Field(default_factory=dict)


class TopicAnalysisAgent:
    """
    Agent responsible for analyzing topics and identifying content opportunities
    """
    
    # Service dog related seed keywords for the niche
    SEED_KEYWORDS = [
        "service dog", "service animal", "ADA service dog",
        "psychiatric service dog", "PTSD service dog", "anxiety service dog",
        "autism service dog", "diabetic alert dog", "seizure alert dog",
        "service dog training", "service dog certification", "service dog registration",
        "service dog laws", "service dog rights", "service dog requirements",
        "emotional support animal", "ESA vs service dog", "therapy dog",
        "service dog vest", "service dog supplies", "service dog commands",
        "how to get a service dog", "service dog cost", "service dog breeds"
    ]
    
    # Common question patterns for FAQ content
    QUESTION_PATTERNS = [
        "how to", "what is", "can you", "do I need", "where can",
        "when should", "why do", "is it legal", "how much does",
        "what are the requirements", "who qualifies", "how long does"
    ]
    
    def __init__(self, anthropic_api_key: Optional[str] = None):
        """
        Initialize the Topic Analysis Agent
        
        Args:
            anthropic_api_key: Anthropic API key for AI-powered analysis
        """
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_client = None
        
        if self.anthropic_api_key and not self.anthropic_api_key.startswith("your-"):
            try:
                self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
                logger.info("Anthropic client initialized for topic analysis")
            except Exception as e:
                logger.warning(f"Could not initialize Anthropic client: {e}")
        
        # Cache for analysis results
        self.cache_dir = Path("data/topic_analysis")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Analysis history
        self.analysis_history: List[TopicAnalysisReport] = []
    
    async def analyze_topics(
        self,
        competitor_content: Optional[List[Dict[str, Any]]] = None,
        target_keywords: Optional[List[str]] = None,
        existing_content: Optional[List[str]] = None,
        max_recommendations: int = 10
    ) -> TopicAnalysisReport:
        """
        Perform comprehensive topic analysis
        
        Args:
            competitor_content: List of competitor articles
            target_keywords: Specific keywords to analyze
            existing_content: List of existing article titles to avoid duplication
            max_recommendations: Maximum number of topic recommendations
            
        Returns:
            TopicAnalysisReport with recommendations
        """
        # Use seed keywords if none provided
        if not target_keywords:
            target_keywords = self.SEED_KEYWORDS[:10]
        
        # Analyze keywords
        keyword_data = await self._analyze_keywords(target_keywords)
        
        # Identify content gaps
        content_gaps = await self._identify_content_gaps(
            competitor_content or [],
            existing_content or [],
            keyword_data
        )
        
        # Generate topic recommendations
        recommendations = await self._generate_recommendations(
            keyword_data,
            content_gaps,
            max_recommendations
        )
        
        # Compile market insights
        market_insights = self._compile_market_insights(
            keyword_data,
            content_gaps,
            competitor_content or []
        )
        
        # Create report
        report = TopicAnalysisReport(
            keywords_analyzed=len(keyword_data),
            content_gaps_found=len(content_gaps),
            topics_recommended=len(recommendations),
            keyword_data=keyword_data,
            content_gaps=content_gaps,
            recommendations=recommendations,
            market_insights=market_insights
        )
        
        # Cache the report
        self._cache_report(report)
        self.analysis_history.append(report)
        
        return report
    
    async def _analyze_keywords(self, keywords: List[str]) -> List[KeywordData]:
        """Analyze keywords for SEO potential"""
        keyword_data = []
        
        for keyword in keywords:
            # Simulate keyword analysis (in production, use SEO APIs)
            data = KeywordData(
                keyword=keyword,
                search_volume=self._estimate_search_volume(keyword),
                difficulty=self._estimate_difficulty(keyword),
                trend=self._determine_trend(keyword),
                intent=self._determine_intent(keyword),
                related_keywords=self._find_related_keywords(keyword)
            )
            keyword_data.append(data)
        
        return keyword_data
    
    def _estimate_search_volume(self, keyword: str) -> int:
        """Estimate search volume based on keyword characteristics"""
        # Simple heuristic based on keyword length and specificity
        base_volume = 10000
        
        # Adjust for keyword length (longer = more specific = lower volume)
        words = keyword.split()
        length_factor = 1.0 / (len(words) ** 0.5)
        
        # Adjust for specificity
        if "how to" in keyword.lower():
            specificity_factor = 0.7
        elif any(word in keyword.lower() for word in ["requirements", "laws", "cost"]):
            specificity_factor = 0.8
        else:
            specificity_factor = 1.0
        
        # Popular terms get a boost
        if "service dog" in keyword.lower():
            popularity_factor = 1.5
        elif "ADA" in keyword.upper():
            popularity_factor = 1.3
        else:
            popularity_factor = 1.0
        
        volume = int(base_volume * length_factor * specificity_factor * popularity_factor)
        return max(100, min(50000, volume))  # Cap between 100 and 50k
    
    def _estimate_difficulty(self, keyword: str) -> float:
        """Estimate keyword difficulty (0-1, higher is harder)"""
        # Factors that increase difficulty
        difficulty = 0.3  # Base difficulty
        
        # High-competition terms
        if any(term in keyword.lower() for term in ["service dog", "ada", "certification"]):
            difficulty += 0.3
        
        # Legal/medical terms are harder
        if any(term in keyword.lower() for term in ["laws", "requirements", "rights"]):
            difficulty += 0.2
        
        # Longer keywords are generally easier
        words = keyword.split()
        if len(words) > 3:
            difficulty -= 0.1
        
        # Questions are easier to rank for
        if keyword.lower().startswith(("how", "what", "can", "do")):
            difficulty -= 0.15
        
        return max(0.1, min(0.95, difficulty))
    
    def _determine_trend(self, keyword: str) -> str:
        """Determine if keyword trend is rising, stable, or declining"""
        # Simulate trend analysis
        trending_topics = ["PTSD service dog", "autism service dog", "psychiatric service dog"]
        declining_topics = ["service dog certification", "register service dog"]
        
        if any(topic in keyword.lower() for topic in trending_topics):
            return "rising"
        elif any(topic in keyword.lower() for topic in declining_topics):
            return "declining"
        else:
            return "stable"
    
    def _determine_intent(self, keyword: str) -> str:
        """Determine search intent"""
        keyword_lower = keyword.lower()
        
        # Transactional intent
        if any(term in keyword_lower for term in ["buy", "cost", "price", "cheap", "best"]):
            return "transactional"
        
        # Navigational intent
        if any(term in keyword_lower for term in ["ada.gov", "website", "login", "portal"]):
            return "navigational"
        
        # Informational intent (default for most service dog queries)
        return "informational"
    
    def _find_related_keywords(self, keyword: str) -> List[str]:
        """Find related keywords"""
        related = []
        base_keyword = keyword.lower()
        
        # Add question variations
        if not base_keyword.startswith(("how", "what", "can", "do")):
            related.append(f"how to {base_keyword}")
            related.append(f"what is {base_keyword}")
        
        # Add location variations
        if "service dog" in base_keyword and "laws" not in base_keyword:
            related.append(f"{keyword} laws")
            related.append(f"{keyword} requirements")
        
        # Add comparison variations
        if "service dog" in base_keyword:
            related.append(base_keyword.replace("service dog", "emotional support animal"))
        
        return related[:5]  # Limit to 5 related keywords
    
    async def _identify_content_gaps(
        self,
        competitor_content: List[Dict[str, Any]],
        existing_content: List[str],
        keyword_data: List[KeywordData]
    ) -> List[ContentGap]:
        """Identify content gaps and opportunities"""
        gaps = []
        
        # Extract topics from competitor content
        competitor_topics = set()
        for content in competitor_content:
            if "title" in content:
                competitor_topics.add(content["title"].lower())
        
        # Convert existing content to lowercase for comparison
        existing_topics = set(title.lower() for title in existing_content)
        
        # Check each keyword for gaps
        for kw_data in keyword_data:
            keyword = kw_data.keyword.lower()
            
            # Check if we're missing this topic entirely
            if not any(keyword in title for title in existing_topics):
                # Check if competitors are covering it
                competitors_covering = [
                    title for title in competitor_topics
                    if keyword in title
                ]
                
                if competitors_covering or kw_data.search_volume > 1000:
                    gap = ContentGap(
                        topic=kw_data.keyword,
                        gap_type="missing" if competitors_covering else "underserved",
                        competitors_covering=competitors_covering[:3],
                        estimated_traffic_potential=kw_data.search_volume,
                        difficulty_score=kw_data.difficulty or 0.5,
                        opportunity_score=self._calculate_opportunity_score(kw_data, len(competitors_covering)),
                        rationale=f"High search volume topic not covered in existing content"
                    )
                    gaps.append(gap)
        
        # Sort by opportunity score
        gaps.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        return gaps[:20]  # Return top 20 gaps
    
    def _calculate_opportunity_score(self, keyword_data: KeywordData, competitor_count: int) -> float:
        """Calculate opportunity score for a content gap"""
        # Factors for opportunity score
        volume_factor = min(1.0, (keyword_data.search_volume or 1000) / 5000)
        difficulty_factor = 1.0 - (keyword_data.difficulty or 0.5)
        competition_factor = 1.0 - (min(5, competitor_count) / 5)
        trend_factor = 1.0 if keyword_data.trend == "rising" else 0.8 if keyword_data.trend == "stable" else 0.6
        
        # Weighted average
        score = (
            volume_factor * 0.3 +
            difficulty_factor * 0.3 +
            competition_factor * 0.2 +
            trend_factor * 0.2
        )
        
        return round(score, 2)
    
    async def _generate_recommendations(
        self,
        keyword_data: List[KeywordData],
        content_gaps: List[ContentGap],
        max_recommendations: int
    ) -> List[TopicRecommendation]:
        """Generate specific topic recommendations"""
        recommendations = []
        
        # Prioritize high-opportunity gaps
        priority_gaps = content_gaps[:max_recommendations * 2]
        
        for gap in priority_gaps:
            # Find matching keyword data
            kw_match = next((kw for kw in keyword_data if kw.keyword.lower() == gap.topic.lower()), None)
            
            if kw_match:
                # Generate recommendation
                rec = self._create_recommendation(gap, kw_match)
                recommendations.append(rec)
                
                if len(recommendations) >= max_recommendations:
                    break
        
        # If we need more recommendations, create from high-value keywords
        if len(recommendations) < max_recommendations:
            for kw_data in keyword_data:
                if kw_data.search_volume > 2000 and kw_data.difficulty < 0.7:
                    # Create recommendation from keyword
                    rec = self._create_recommendation_from_keyword(kw_data)
                    recommendations.append(rec)
                    
                    if len(recommendations) >= max_recommendations:
                        break
        
        # Sort by priority score
        recommendations.sort(key=lambda x: x.priority_score, reverse=True)
        
        return recommendations
    
    def _create_recommendation(self, gap: ContentGap, keyword_data: KeywordData) -> TopicRecommendation:
        """Create a topic recommendation from a content gap"""
        # Determine content type based on keyword
        content_type = self._determine_content_type(keyword_data.keyword)
        
        # Generate title
        title = self._generate_title(keyword_data.keyword, content_type)
        
        # Create slug
        slug = re.sub(r'[^a-z0-9-]', '', title.lower().replace(' ', '-'))
        
        # Determine word count based on competition and difficulty
        word_count = self._determine_word_count(keyword_data.difficulty or 0.5, content_type)
        
        # Calculate priority score
        priority = (gap.opportunity_score * 50) + ((1 - keyword_data.difficulty) * 30) + 20
        
        # Generate outline
        outline = self._generate_outline(keyword_data.keyword, content_type)
        
        return TopicRecommendation(
            title=title,
            slug=slug,
            primary_keyword=keyword_data.keyword,
            secondary_keywords=keyword_data.related_keywords[:5],
            content_type=content_type,
            target_word_count=word_count,
            estimated_difficulty=keyword_data.difficulty or 0.5,
            estimated_impact=gap.opportunity_score,
            priority_score=min(100, priority),
            rationale=gap.rationale,
            competitor_examples=gap.competitors_covering[:3],
            content_outline=outline
        )
    
    def _create_recommendation_from_keyword(self, keyword_data: KeywordData) -> TopicRecommendation:
        """Create a topic recommendation directly from keyword data"""
        content_type = self._determine_content_type(keyword_data.keyword)
        title = self._generate_title(keyword_data.keyword, content_type)
        slug = re.sub(r'[^a-z0-9-]', '', title.lower().replace(' ', '-'))
        word_count = self._determine_word_count(keyword_data.difficulty or 0.5, content_type)
        
        # Calculate impact based on search volume and trend
        impact = min(1.0, (keyword_data.search_volume or 1000) / 10000)
        if keyword_data.trend == "rising":
            impact *= 1.2
        
        priority = (impact * 40) + ((1 - keyword_data.difficulty) * 40) + 20
        
        return TopicRecommendation(
            title=title,
            slug=slug,
            primary_keyword=keyword_data.keyword,
            secondary_keywords=keyword_data.related_keywords[:5],
            content_type=content_type,
            target_word_count=word_count,
            estimated_difficulty=keyword_data.difficulty or 0.5,
            estimated_impact=impact,
            priority_score=min(100, priority),
            rationale=f"High search volume keyword with {keyword_data.trend} trend",
            competitor_examples=[],
            content_outline=self._generate_outline(keyword_data.keyword, content_type)
        )
    
    def _determine_content_type(self, keyword: str) -> str:
        """Determine the best content type for a keyword"""
        keyword_lower = keyword.lower()
        
        if keyword_lower.startswith("how to"):
            return "how-to"
        elif "vs" in keyword_lower or "versus" in keyword_lower or "difference" in keyword_lower:
            return "comparison"
        elif any(q in keyword_lower for q in ["what", "why", "when", "where", "can"]):
            return "faq"
        elif "best" in keyword_lower or "top" in keyword_lower:
            return "listicle"
        else:
            return "guide"
    
    def _generate_title(self, keyword: str, content_type: str) -> str:
        """Generate an SEO-optimized title"""
        keyword_title = keyword.title()
        
        templates = {
            "how-to": f"{keyword_title}: Step-by-Step Guide",
            "guide": f"{keyword_title}: Complete Guide for 2025",
            "listicle": f"10 Best {keyword_title} Tips You Need to Know",
            "comparison": f"{keyword_title}: Key Differences Explained",
            "faq": f"{keyword_title}: Your Questions Answered"
        }
        
        return templates.get(content_type, f"{keyword_title}: Everything You Need to Know")
    
    def _determine_word_count(self, difficulty: float, content_type: str) -> int:
        """Determine target word count based on difficulty and content type"""
        base_counts = {
            "how-to": 1500,
            "guide": 2000,
            "listicle": 1200,
            "comparison": 1800,
            "faq": 1500
        }
        
        base = base_counts.get(content_type, 1500)
        
        # Higher difficulty requires more comprehensive content
        if difficulty > 0.7:
            base = int(base * 1.3)
        elif difficulty > 0.5:
            base = int(base * 1.15)
        
        return base
    
    def _generate_outline(self, keyword: str, content_type: str) -> List[str]:
        """Generate a basic content outline"""
        keyword_title = keyword.title()
        
        outlines = {
            "how-to": [
                f"Introduction to {keyword_title}",
                "Prerequisites and Requirements",
                "Step-by-Step Instructions",
                "Common Mistakes to Avoid",
                "Tips for Success",
                "Frequently Asked Questions",
                "Conclusion and Next Steps"
            ],
            "guide": [
                f"What is {keyword_title}?",
                "Why It Matters",
                "Key Components",
                "How It Works",
                "Benefits and Advantages",
                "Common Challenges",
                "Best Practices",
                "Resources and Further Reading"
            ],
            "listicle": [
                "Introduction",
                "Quick Overview",
                "The List (10 items)",
                "How to Choose",
                "Expert Tips",
                "Conclusion"
            ],
            "comparison": [
                "Introduction",
                "Overview of Options",
                "Key Differences",
                "Pros and Cons",
                "Use Cases",
                "Making the Right Choice",
                "Conclusion"
            ],
            "faq": [
                "Introduction",
                "Most Common Questions",
                "Legal Questions",
                "Practical Questions",
                "Cost-Related Questions",
                "Additional Resources",
                "Conclusion"
            ]
        }
        
        return outlines.get(content_type, outlines["guide"])
    
    def _compile_market_insights(
        self,
        keyword_data: List[KeywordData],
        content_gaps: List[ContentGap],
        competitor_content: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compile market insights from analysis"""
        # Trending topics
        trending = [kw.keyword for kw in keyword_data if kw.trend == "rising"]
        
        # High opportunity keywords
        high_opportunity = [
            kw.keyword for kw in keyword_data
            if kw.search_volume > 3000 and kw.difficulty < 0.6
        ]
        
        # Content type distribution
        content_types = defaultdict(int)
        for content in competitor_content:
            if "type" in content:
                content_types[content["type"]] += 1
        
        # Average metrics
        avg_volume = sum(kw.search_volume or 0 for kw in keyword_data) / max(1, len(keyword_data))
        avg_difficulty = sum(kw.difficulty or 0.5 for kw in keyword_data) / max(1, len(keyword_data))
        
        return {
            "trending_topics": trending[:5],
            "high_opportunity_keywords": high_opportunity[:5],
            "content_type_distribution": dict(content_types),
            "average_search_volume": int(avg_volume),
            "average_difficulty": round(avg_difficulty, 2),
            "total_gaps_identified": len(content_gaps),
            "competitor_content_analyzed": len(competitor_content)
        }
    
    def _cache_report(self, report: TopicAnalysisReport):
        """Cache the analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_file = self.cache_dir / f"analysis_{timestamp}.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(report.dict(), f, indent=2, default=str)
            logger.info(f"Cached topic analysis report: {cache_file}")
        except Exception as e:
            logger.error(f"Failed to cache report: {e}")
    
    async def get_quick_recommendations(
        self,
        count: int = 5,
        focus: Optional[str] = None
    ) -> List[TopicRecommendation]:
        """
        Get quick topic recommendations without full analysis
        
        Args:
            count: Number of recommendations
            focus: Optional focus area (e.g., "PTSD", "training", "laws")
            
        Returns:
            List of topic recommendations
        """
        # Filter seed keywords based on focus
        if focus:
            keywords = [kw for kw in self.SEED_KEYWORDS if focus.lower() in kw.lower()]
        else:
            keywords = self.SEED_KEYWORDS
        
        # Analyze subset of keywords
        keyword_data = await self._analyze_keywords(keywords[:count * 2])
        
        # Generate recommendations
        recommendations = []
        for kw_data in keyword_data:
            if len(recommendations) >= count:
                break
            
            rec = self._create_recommendation_from_keyword(kw_data)
            recommendations.append(rec)
        
        return recommendations
    
    def get_analysis_history(self, limit: int = 10) -> List[TopicAnalysisReport]:
        """Get recent analysis history"""
        return self.analysis_history[-limit:]


# Example usage
async def main():
    """Example of using the Topic Analysis Agent"""
    agent = TopicAnalysisAgent()
    
    # Perform full analysis
    print("🔍 Performing topic analysis...")
    report = await agent.analyze_topics(
        target_keywords=[
            "PTSD service dog",
            "autism service dog", 
            "service dog training",
            "service dog laws California",
            "how to get a service dog"
        ]
    )
    
    print(f"\n📊 Analysis Complete!")
    print(f"Keywords Analyzed: {report.keywords_analyzed}")
    print(f"Content Gaps Found: {report.content_gaps_found}")
    print(f"Topics Recommended: {report.topics_recommended}")
    
    print(f"\n🎯 Top 3 Recommendations:")
    for i, rec in enumerate(report.recommendations[:3], 1):
        print(f"\n{i}. {rec.title}")
        print(f"   Priority Score: {rec.priority_score:.1f}/100")
        print(f"   Primary Keyword: {rec.primary_keyword}")
        print(f"   Content Type: {rec.content_type}")
        print(f"   Target Words: {rec.target_word_count}")
        print(f"   Rationale: {rec.rationale}")
    
    print(f"\n💡 Market Insights:")
    for key, value in report.market_insights.items():
        print(f"   {key}: {value}")
    
    # Get quick recommendations
    print(f"\n⚡ Quick Recommendations (PTSD focus):")
    quick_recs = await agent.get_quick_recommendations(count=3, focus="PTSD")
    for rec in quick_recs:
        print(f"   - {rec.title} (Priority: {rec.priority_score:.1f})")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())