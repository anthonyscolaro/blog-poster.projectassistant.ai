"""
Article Generation Agent
Generates high-quality, SEO-optimized articles using LLMs
"""
import os
import json
import asyncio
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from pathlib import Path
import logging
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl
import anthropic
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

# Import WordPress conversion utility
from src.utils.markdown_to_wp_blocks import markdown_to_wp_blocks

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Available LLM providers"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class CostTracking(BaseModel):
    """Track costs for LLM API calls"""
    provider: LLMProvider
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    timestamp: datetime = Field(default_factory=datetime.now)


class SEORequirements(BaseModel):
    """SEO requirements for article generation"""
    primary_keyword: str
    secondary_keywords: List[str] = Field(default_factory=list)
    meta_title_length: int = 60
    meta_description_length: int = 155
    min_words: int = 1500
    max_words: int = 2500
    target_reading_level: int = 8  # Grade level
    internal_links_count: int = 3
    external_links_count: int = 2
    
    
class ArticleOutline(BaseModel):
    """Structure for article outline"""
    title: str
    meta_title: str
    meta_description: str
    introduction: str
    sections: List[Dict[str, Any]]  # List of {heading, points, keywords}
    conclusion_points: List[str]
    internal_link_opportunities: List[str]
    citations_needed: List[str]


class GeneratedArticle(BaseModel):
    """Complete generated article with metadata"""
    title: str
    slug: str
    meta_title: str
    meta_description: str
    content_markdown: str
    content_html: Optional[str] = None
    primary_keyword: str
    secondary_keywords: List[str]
    word_count: int
    reading_level: float
    internal_links: List[Dict[str, str]]  # {text, url}
    external_links: List[Dict[str, str]]  # {text, url}
    citations: List[str]
    featured_image_prompt: str
    category: str
    tags: List[str]
    estimated_reading_time: int  # minutes
    seo_score: float  # 0-100
    cost_tracking: Optional[CostTracking] = None
    generated_at: datetime = Field(default_factory=datetime.now)


class ArticleGenerationAgent:
    """
    Agent responsible for generating high-quality, SEO-optimized articles
    """
    
    # Cost per 1M tokens (as of 2024)
    PRICING = {
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        "gpt-4-turbo-preview": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50}
    }
    
    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        default_provider: LLMProvider = LLMProvider.ANTHROPIC,
        model_override: Optional[str] = None,
        max_cost_per_article: float = 0.50,
        cache_dir: str = "data/articles"
    ):
        """
        Initialize the article generation agent
        
        Args:
            anthropic_api_key: Anthropic API key
            openai_api_key: OpenAI API key
            default_provider: Default LLM provider to use
            model_override: Override default model selection
            max_cost_per_article: Maximum cost allowed per article
            cache_dir: Directory to cache generated articles
        """
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.default_provider = default_provider
        self.max_cost_per_article = max_cost_per_article
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize clients
        self.anthropic_client = None
        self.openai_client = None
        
        if self.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            logger.info("Anthropic client initialized")
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.openai_client = openai
            logger.info("OpenAI client initialized")
        
        # Model selection
        if model_override:
            self.model = model_override
        else:
            if default_provider == LLMProvider.ANTHROPIC:
                self.model = "claude-3-5-sonnet-20241022"  # Best for content
            else:
                self.model = "gpt-4-turbo-preview"
        
        # Track total costs
        self.total_cost = 0.0
        self.cost_history = []
    
    async def generate_article(
        self,
        topic: str,
        seo_requirements: SEORequirements,
        brand_voice: str = "professional and informative",
        target_audience: str = "general public interested in service dogs",
        additional_context: Optional[str] = None,
        competitor_insights: Optional[Dict[str, Any]] = None
    ) -> GeneratedArticle:
        """
        Generate a complete SEO-optimized article
        
        Args:
            topic: Main topic to write about
            seo_requirements: SEO requirements and constraints
            brand_voice: Brand voice and tone
            target_audience: Target audience description
            additional_context: Any additional context or requirements
            competitor_insights: Insights from competitor analysis
        
        Returns:
            GeneratedArticle with content and metadata
        """
        try:
            # Step 1: Generate article outline
            outline = await self._generate_outline(
                topic, seo_requirements, competitor_insights
            )
            
            # Step 2: Generate full article content
            content = await self._generate_content(
                outline, seo_requirements, brand_voice, target_audience
            )
            
            # Step 3: Generate SEO metadata
            metadata = await self._generate_metadata(
                content, seo_requirements, topic
            )
            
            # Step 4: Convert Markdown to WordPress HTML
            content_html = self._convert_to_wordpress_html(content)
            
            # Step 5: Calculate costs
            cost_tracking = self._calculate_costs()
            
            # Check cost limit
            if cost_tracking.cost > self.max_cost_per_article:
                logger.warning(f"Article generation exceeded cost limit: ${cost_tracking.cost:.2f}")
            
            # Step 6: Validate word count and retry if needed
            word_count = len(content.split())
            if word_count < seo_requirements.min_words:
                logger.warning(f"Article is too short ({word_count} words, minimum {seo_requirements.min_words}). Attempting to expand...")
                try:
                    content = await self._expand_content(content, seo_requirements, word_count)
                    content_html = self._convert_to_wordpress_html(content)
                    logger.info(f"Expanded article to {len(content.split())} words")
                except Exception as e:
                    logger.error(f"Failed to expand content: {e}")
                    # Continue with original content but log the issue
            
            # Step 7: Create final article
            article = self._assemble_article(
                content, content_html, metadata, outline, seo_requirements, cost_tracking
            )
            
            # Step 8: Cache the article
            self._cache_article(article)
            
            return article
            
        except Exception as e:
            logger.error(f"Failed to generate article: {str(e)}")
            raise
    
    async def _generate_outline(
        self,
        topic: str,
        seo_requirements: SEORequirements,
        competitor_insights: Optional[Dict[str, Any]] = None
    ) -> ArticleOutline:
        """Generate article outline"""
        
        prompt = f"""You are an expert content strategist specializing in SEO-optimized articles about service dogs and ADA compliance.

Create a detailed outline for an article about: {topic}

SEO Requirements:
- Primary keyword: {seo_requirements.primary_keyword}
- Secondary keywords: {', '.join(seo_requirements.secondary_keywords)}
- Target length: {seo_requirements.min_words}-{seo_requirements.max_words} words (MUST meet minimum {seo_requirements.min_words} words)
- Internal links needed: {seo_requirements.internal_links_count}

{f"Competitor Insights: {json.dumps(competitor_insights, indent=2)}" if competitor_insights else ""}

Provide a comprehensive outline that will result in a {seo_requirements.min_words}+ word article:
1. Compelling title (under 60 characters)
2. Meta title (SEO-optimized, under 60 characters)
3. Meta description (compelling, under 155 characters)
4. Introduction paragraph (hook the reader)
5. Main sections (6-8 detailed sections with multiple subpoints each to reach {seo_requirements.min_words} words)
6. Conclusion points
7. Internal link opportunities (topics to link to)
8. Citations needed (laws, regulations, studies)

CRITICAL: Design the outline to support {seo_requirements.min_words}-{seo_requirements.max_words} words. Include enough sections and subpoints.

Format as JSON with this structure:
{{
    "title": "...",
    "meta_title": "...",
    "meta_description": "...",
    "introduction": "...",
    "sections": [
        {{
            "heading": "...",
            "points": ["...", "..."],
            "keywords": ["..."]
        }}
    ],
    "conclusion_points": ["...", "..."],
    "internal_link_opportunities": ["...", "..."],
    "citations_needed": ["...", "..."]
}}"""

        response = await self._call_llm(prompt, max_tokens=2000)
        
        # Parse JSON response
        try:
            outline_data = json.loads(response)
            return ArticleOutline(**outline_data)
        except json.JSONDecodeError:
            # Fallback: extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                outline_data = json.loads(json_match.group())
                return ArticleOutline(**outline_data)
            else:
                # Create basic outline if parsing fails
                return ArticleOutline(
                    title=topic,
                    meta_title=topic[:60],
                    meta_description=f"Learn about {topic} for service dogs",
                    introduction=f"This article covers {topic}",
                    sections=[{"heading": "Overview", "points": [topic], "keywords": [seo_requirements.primary_keyword]}],
                    conclusion_points=["Summary"],
                    internal_link_opportunities=[],
                    citations_needed=[]
                )
    
    async def _generate_content(
        self,
        outline: ArticleOutline,
        seo_requirements: SEORequirements,
        brand_voice: str,
        target_audience: str
    ) -> str:
        """Generate full article content based on outline"""
        
        prompt = f"""You are an expert content writer specializing in service dogs and ADA compliance.

Write a comprehensive article based on this outline:

Title: {outline.title}
Meta Description: {outline.meta_description}

Introduction: {outline.introduction}

Sections:
{json.dumps(outline.sections, indent=2)}

Conclusion Points:
{json.dumps(outline.conclusion_points, indent=2)}

Requirements:
- Brand voice: {brand_voice}
- Target audience: {target_audience}
- Length: MUST be {seo_requirements.min_words}-{seo_requirements.max_words} words (CRITICAL: minimum {seo_requirements.min_words} words required)
- Primary keyword "{seo_requirements.primary_keyword}" should appear naturally 3-5 times
- Include these secondary keywords naturally: {', '.join(seo_requirements.secondary_keywords)}
- Write at a {seo_requirements.target_reading_level}th grade reading level
- Include specific examples and actionable advice
- Be factually accurate about ADA laws and service dog regulations
- Use markdown formatting with proper headings (##, ###)
- Include a clear call-to-action
- Make it engaging and valuable for readers
- Focus on creating content that will convert well to WordPress blocks
- Use standard markdown syntax (no complex HTML or special formatting)

IMPORTANT: 
- Be specific about ADA requirements (28 CFR Part 36)
- Distinguish clearly between service dogs and emotional support animals
- Include the two questions businesses can ask
- Mention that registration/certification is NOT required by ADA
- Be empathetic to both handlers and business owners
- DO NOT add any completion markers like "[End of Article]", "[END]", or similar
- DO NOT include disclaimers about being an AI assistant
- End naturally with a strong conclusion or call-to-action

Write the complete article now:"""

        content = await self._call_llm(prompt, max_tokens=4000)
        
        # Post-process content
        content = self._optimize_content_for_seo(content, seo_requirements)
        
        return content
    
    async def _generate_metadata(
        self,
        content: str,
        seo_requirements: SEORequirements,
        topic: str
    ) -> Dict[str, Any]:
        """Generate SEO metadata for the article"""
        
        prompt = f"""Based on this article content, generate SEO metadata:

{content[:2000]}...

Generate:
1. URL slug (lowercase, hyphens, no special characters)
2. Featured image prompt (detailed description for image generation)
3. Category (one of: ADA Compliance, Training, Laws & Rights, Health & Wellness, Travel & Access)
4. Tags (5-8 relevant tags)
5. Estimated reading time (based on ~200 words per minute)
6. 3 internal link suggestions with anchor text
7. 2 external link suggestions with anchor text (authoritative sources only)

Format as JSON:
{{
    "slug": "...",
    "featured_image_prompt": "...",
    "category": "...",
    "tags": ["...", "..."],
    "estimated_reading_time": X,
    "internal_links": [
        {{"text": "...", "url": "/..."}},
    ],
    "external_links": [
        {{"text": "...", "url": "https://..."}}
    ]
}}"""

        response = await self._call_llm(prompt, max_tokens=1000)
        
        try:
            metadata = json.loads(response)
        except json.JSONDecodeError:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                metadata = json.loads(json_match.group())
            else:
                # Fallback metadata
                metadata = {
                    "slug": topic.lower().replace(" ", "-")[:50],
                    "featured_image_prompt": f"Service dog helping handler with {topic}",
                    "category": "ADA Compliance",
                    "tags": ["service dogs", "ADA", topic.lower()],
                    "estimated_reading_time": len(content.split()) // 200,
                    "internal_links": [],
                    "external_links": []
                }
        
        return metadata
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _call_llm(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        Call LLM API with retry logic
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation
        
        Returns:
            Generated text response
        """
        # Try primary provider first
        provider = self.default_provider
        
        try:
            if provider == LLMProvider.ANTHROPIC and self.anthropic_client:
                return await self._call_anthropic(prompt, max_tokens, temperature)
            elif provider == LLMProvider.OPENAI and self.openai_client:
                return await self._call_openai(prompt, max_tokens, temperature)
            else:
                # Fallback to other provider
                if self.anthropic_client:
                    return await self._call_anthropic(prompt, max_tokens, temperature)
                elif self.openai_client:
                    return await self._call_openai(prompt, max_tokens, temperature)
                else:
                    raise Exception("No LLM provider configured")
                    
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            # Try fallback provider
            if provider == LLMProvider.ANTHROPIC and self.openai_client:
                logger.info("Falling back to OpenAI")
                return await self._call_openai(prompt, max_tokens, temperature)
            elif provider == LLMProvider.OPENAI and self.anthropic_client:
                logger.info("Falling back to Anthropic")
                return await self._call_anthropic(prompt, max_tokens, temperature)
            else:
                raise
    
    async def _call_anthropic(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Call Anthropic Claude API"""
        
        message = self.anthropic_client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Track tokens for cost calculation
        self._track_tokens(
            LLMProvider.ANTHROPIC,
            self.model,
            message.usage.input_tokens if hasattr(message, 'usage') else len(prompt) // 4,
            message.usage.output_tokens if hasattr(message, 'usage') else len(message.content[0].text) // 4
        )
        
        return message.content[0].text
    
    async def _call_openai(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Call OpenAI API"""
        
        # Use async version for better performance
        response = await asyncio.to_thread(
            self.openai_client.chat.completions.create,
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert content writer specializing in service dogs and ADA compliance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Track tokens for cost calculation
        self._track_tokens(
            LLMProvider.OPENAI,
            self.model,
            response.usage.prompt_tokens,
            response.usage.completion_tokens
        )
        
        return response.choices[0].message.content
    
    def _track_tokens(
        self,
        provider: LLMProvider,
        model: str,
        input_tokens: int,
        output_tokens: int
    ):
        """Track token usage for cost calculation"""
        if model in self.PRICING:
            input_cost = (input_tokens / 1_000_000) * self.PRICING[model]["input"]
            output_cost = (output_tokens / 1_000_000) * self.PRICING[model]["output"]
            total_cost = input_cost + output_cost
            
            self.total_cost += total_cost
            
            tracking = CostTracking(
                provider=provider,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=total_cost
            )
            
            self.cost_history.append(tracking)
            
            logger.info(f"API call cost: ${total_cost:.4f} (Total: ${self.total_cost:.4f})")
    
    def _calculate_costs(self) -> Optional[CostTracking]:
        """Calculate total costs for the current article"""
        if not self.cost_history:
            return None
        
        # Sum up all costs for this article
        total_input = sum(c.input_tokens for c in self.cost_history)
        total_output = sum(c.output_tokens for c in self.cost_history)
        total_cost = sum(c.cost for c in self.cost_history)
        
        return CostTracking(
            provider=self.cost_history[-1].provider,
            model=self.cost_history[-1].model,
            input_tokens=total_input,
            output_tokens=total_output,
            cost=total_cost
        )
    
    def _optimize_content_for_seo(
        self,
        content: str,
        seo_requirements: SEORequirements
    ) -> str:
        """Optimize content for SEO requirements and clean up AI artifacts"""
        
        # First, clean up common AI artifacts and unwanted text
        content = self._clean_ai_artifacts(content)
        
        # Count keyword occurrences
        primary_count = content.lower().count(seo_requirements.primary_keyword.lower())
        
        # If primary keyword is underused, add it naturally
        if primary_count < 3:
            # Add to introduction if not present
            if seo_requirements.primary_keyword.lower() not in content[:500].lower():
                content = content.replace(
                    "# ",
                    f"# {seo_requirements.primary_keyword.title()} - ",
                    1
                )
        
        # Ensure secondary keywords are present
        for keyword in seo_requirements.secondary_keywords[:3]:
            if keyword.lower() not in content.lower():
                # Try to add naturally in a relevant context
                logger.info(f"Adding missing keyword: {keyword}")
        
        return content
    
    def _clean_ai_artifacts(self, content: str) -> str:
        """
        Remove common AI-generated artifacts and unwanted text patterns
        
        Args:
            content: Raw content from LLM
        
        Returns:
            Cleaned content ready for publication
        """
        import re
        
        # List of patterns to remove (case-insensitive)
        unwanted_patterns = [
            r'\[End of Article\]',
            r'\[END\]',
            r'\[/Article\]',
            r'</article>',
            r'---\s*End\s*---',
            r'Article complete\.?',
            r'Content complete\.?',
            r'Generation complete\.?',
            r'\*\*\[End of content\]\*\*',
            r'That concludes the article\.?',
            r'This completes the article\.?',
            r'---End of Content---',
            r'Advertisement:.*$',  # Remove any ad-like content
            r'Disclaimer:.*(?=\n#|\n\n|$)',  # Remove generic disclaimers (keep legal ones)
            r'\bAI Assistant:.*$',  # Remove AI assistant signatures
            r'\bAssistant:.*$',     # Remove assistant signatures
        ]
        
        # Clean each pattern
        for pattern in unwanted_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.MULTILINE)
        
        # Clean up excessive whitespace
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Multiple empty lines to double
        content = re.sub(r'^\s+|\s+$', '', content)  # Trim start/end whitespace
        
        # Remove trailing periods or markers that might be completion artifacts
        content = re.sub(r'\.\.\.$', '', content.strip())
        content = re.sub(r'\*{3,}$', '', content.strip())  # Remove trailing asterisks
        content = re.sub(r'-{3,}$', '', content.strip())   # Remove trailing dashes
        
        # Log if we cleaned anything
        if len(content.strip()) != len(content):
            logger.info("Cleaned AI artifacts from generated content")
        
        return content.strip()
    
    async def _expand_content(self, content: str, seo_requirements: SEORequirements, current_word_count: int) -> str:
        """
        Expand content to meet minimum word count requirements
        
        Args:
            content: Current article content
            seo_requirements: SEO requirements including min_words
            current_word_count: Current word count
        
        Returns:
            Expanded content meeting word count requirements
        """
        words_needed = seo_requirements.min_words - current_word_count
        
        expansion_prompt = f"""The following article is too short ({current_word_count} words) and needs to be expanded to at least {seo_requirements.min_words} words (add approximately {words_needed} words).

CURRENT ARTICLE:
{content}

Please expand this article by:
1. Adding more detailed explanations to existing sections
2. Including additional relevant examples and case studies
3. Adding practical tips and actionable advice
4. Expanding on legal requirements and compliance details
5. Including more comprehensive background information

Requirements:
- Maintain the same tone and style
- Keep all existing content and structure
- Add approximately {words_needed} more words
- Focus on value-added content, not filler
- Maintain SEO keyword density for "{seo_requirements.primary_keyword}"
- Use the same markdown formatting

Return the complete expanded article:"""

        try:
            if self.anthropic_client:
                response = await self.anthropic_client.messages.create(
                    model=self.model_name,
                    max_tokens=4000,
                    temperature=0.7,
                    messages=[{"role": "user", "content": expansion_prompt}]
                )
                expanded_content = response.content[0].text
            else:
                response = await self.openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": expansion_prompt}],
                    max_tokens=4000,
                    temperature=0.7
                )
                expanded_content = response.choices[0].message.content
            
            # Clean the expanded content
            expanded_content = self._clean_ai_artifacts(expanded_content)
            
            # Verify the expansion worked
            new_word_count = len(expanded_content.split())
            if new_word_count >= seo_requirements.min_words:
                logger.info(f"Successfully expanded article from {current_word_count} to {new_word_count} words")
                return expanded_content
            else:
                logger.warning(f"Expansion insufficient: {new_word_count} words, still below {seo_requirements.min_words}")
                return content  # Return original if expansion didn't work
                
        except Exception as e:
            logger.error(f"Failed to expand content: {e}")
            return content  # Return original content on failure
    
    def _convert_to_wordpress_html(self, markdown_content: str) -> str:
        """
        Convert Markdown content to WordPress block HTML
        
        Args:
            markdown_content: The raw markdown content from LLM
        
        Returns:
            WordPress block-formatted HTML
        """
        try:
            # Convert Markdown to WordPress blocks
            _, wp_html = markdown_to_wp_blocks(markdown_content, parse_frontmatter=False)
            logger.info("Successfully converted Markdown to WordPress HTML")
            return wp_html
        except Exception as e:
            logger.error(f"Failed to convert Markdown to WordPress HTML: {e}")
            # Fallback to raw markdown if conversion fails
            return markdown_content
    
    def _assemble_article(
        self,
        content: str,
        content_html: str,
        metadata: Dict[str, Any],
        outline: ArticleOutline,
        seo_requirements: SEORequirements,
        cost_tracking: Optional[CostTracking]
    ) -> GeneratedArticle:
        """Assemble the final article with all metadata"""
        
        # Calculate word count and reading metrics
        word_count = len(content.split())
        
        # Simple readability calculation (would use textstat in production)
        avg_sentence_length = len(content.split('.')) / max(1, content.count('.'))
        reading_level = min(12, max(6, avg_sentence_length / 2))
        
        # Calculate SEO score (simplified)
        seo_score = self._calculate_seo_score(
            content, outline, seo_requirements, metadata
        )
        
        return GeneratedArticle(
            title=outline.title,
            slug=metadata.get("slug", outline.title.lower().replace(" ", "-")[:50]),
            meta_title=outline.meta_title,
            meta_description=outline.meta_description,
            content_markdown=content,
            content_html=content_html,
            primary_keyword=seo_requirements.primary_keyword,
            secondary_keywords=seo_requirements.secondary_keywords,
            word_count=word_count,
            reading_level=reading_level,
            internal_links=metadata.get("internal_links", []),
            external_links=metadata.get("external_links", []),
            citations=outline.citations_needed,
            featured_image_prompt=metadata.get("featured_image_prompt", ""),
            category=metadata.get("category", "ADA Compliance"),
            tags=metadata.get("tags", []),
            estimated_reading_time=metadata.get("estimated_reading_time", word_count // 200),
            seo_score=seo_score,
            cost_tracking=cost_tracking
        )
    
    def _calculate_seo_score(
        self,
        content: str,
        outline: ArticleOutline,
        seo_requirements: SEORequirements,
        metadata: Dict[str, Any]
    ) -> float:
        """Calculate SEO score for the article"""
        score = 0.0
        max_score = 100.0
        
        # Title length (15 points)
        if len(outline.meta_title) <= 60:
            score += 15
        elif len(outline.meta_title) <= 70:
            score += 10
        
        # Meta description length (15 points)
        if 120 <= len(outline.meta_description) <= 155:
            score += 15
        elif 100 <= len(outline.meta_description) <= 170:
            score += 10
        
        # Word count (20 points)
        word_count = len(content.split())
        if seo_requirements.min_words <= word_count <= seo_requirements.max_words:
            score += 20
        elif word_count >= seo_requirements.min_words * 0.8:
            score += 15
        
        # Keyword usage (20 points)
        primary_count = content.lower().count(seo_requirements.primary_keyword.lower())
        if 3 <= primary_count <= 7:
            score += 20
        elif 2 <= primary_count <= 10:
            score += 15
        
        # Secondary keywords (10 points)
        secondary_found = sum(
            1 for kw in seo_requirements.secondary_keywords
            if kw.lower() in content.lower()
        )
        score += min(10, secondary_found * 2)
        
        # Internal links (10 points)
        if len(metadata.get("internal_links", [])) >= seo_requirements.internal_links_count:
            score += 10
        
        # External links (5 points)
        if len(metadata.get("external_links", [])) >= seo_requirements.external_links_count:
            score += 5
        
        # Headings structure (5 points)
        if "##" in content and "###" in content:
            score += 5
        
        return min(100.0, score)
    
    def _cache_article(self, article: GeneratedArticle):
        """Cache generated article to disk"""
        
        filename = f"{article.slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.cache_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(article.dict(), f, indent=2, default=str)
        
        logger.info(f"Article cached: {filepath}")
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get summary of costs"""
        return {
            "total_cost": self.total_cost,
            "articles_generated": len(set(c.timestamp.date() for c in self.cost_history)),
            "average_cost_per_article": self.total_cost / max(1, len(self.cost_history)),
            "provider_breakdown": {
                LLMProvider.ANTHROPIC: sum(c.cost for c in self.cost_history if c.provider == LLMProvider.ANTHROPIC),
                LLMProvider.OPENAI: sum(c.cost for c in self.cost_history if c.provider == LLMProvider.OPENAI)
            }
        }


# Example usage
async def main():
    """Example of using the article generation agent"""
    
    # Initialize agent
    agent = ArticleGenerationAgent(
        max_cost_per_article=0.50
    )
    
    # Define SEO requirements
    seo_reqs = SEORequirements(
        primary_keyword="service dog requirements",
        secondary_keywords=["ADA", "certification", "training", "public access"],
        min_words=1500,
        max_words=2000
    )
    
    # Generate article
    article = await agent.generate_article(
        topic="Service Dog Requirements Under the ADA: What You Need to Know",
        seo_requirements=seo_reqs,
        brand_voice="professional, empathetic, and informative",
        target_audience="Service dog handlers and business owners",
        additional_context="Focus on the two questions businesses can ask and common misconceptions"
    )
    
    print(f"Generated article: {article.title}")
    print(f"Word count: {article.word_count}")
    print(f"SEO score: {article.seo_score:.1f}/100")
    print(f"Cost: ${article.cost_tracking.cost:.4f}" if article.cost_tracking else "Cost tracking not available")
    print(f"\nFirst 500 characters of content:")
    print(article.content_markdown[:500])
    
    # Get cost summary
    print(f"\nCost Summary:")
    print(json.dumps(agent.get_cost_summary(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())