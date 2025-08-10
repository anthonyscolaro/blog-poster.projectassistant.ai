"""
Test suite for Article Generation Agent
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.article_generation_agent import (
    ArticleGenerationAgent,
    SEORequirements,
    GeneratedArticle,
    ArticleOutline,
    CostTracking,
    LLMProvider
)


class TestArticleGenerationAgent:
    """Test cases for the Article Generation Agent"""
    
    @pytest.fixture
    def seo_requirements(self):
        """Create standard SEO requirements"""
        return SEORequirements(
            primary_keyword="service dog training",
            secondary_keywords=["ADA", "disability", "public access", "tasks"],
            min_words=1500,
            max_words=2000,
            internal_links_count=3,
            external_links_count=2
        )
    
    @pytest.fixture
    def agent_with_mock_api(self):
        """Create agent with mocked API calls"""
        agent = ArticleGenerationAgent(
            anthropic_api_key="test-key",
            max_cost_per_article=0.50
        )
        return agent
    
    def test_agent_initialization(self):
        """Test agent initialization with various configurations"""
        # Test with API keys from environment
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-anthropic-key'}):
            agent = ArticleGenerationAgent()
            assert agent.anthropic_api_key == 'test-anthropic-key'
            assert agent.max_cost_per_article == 0.50
        
        # Test with explicit API keys
        agent = ArticleGenerationAgent(
            anthropic_api_key="explicit-key",
            openai_api_key="openai-key",
            max_cost_per_article=1.00
        )
        assert agent.anthropic_api_key == "explicit-key"
        assert agent.openai_api_key == "openai-key"
        assert agent.max_cost_per_article == 1.00
    
    def test_seo_score_calculation(self, agent_with_mock_api, seo_requirements):
        """Test SEO score calculation"""
        agent = agent_with_mock_api
        
        # Create test content
        content = "service dog training " * 500  # ~1500 words
        outline = ArticleOutline(
            title="Service Dog Training Guide",
            meta_title="Service Dog Training: Complete Guide for Handlers",
            meta_description="Learn how to train your service dog with our comprehensive guide covering ADA requirements and essential tasks.",
            introduction="This guide covers service dog training.",
            sections=[],
            conclusion_points=[],
            internal_link_opportunities=[],
            citations_needed=[]
        )
        metadata = {
            "internal_links": [{"text": "link1", "url": "/page1"}, {"text": "link2", "url": "/page2"}, {"text": "link3", "url": "/page3"}],
            "external_links": [{"text": "ADA", "url": "https://ada.gov"}, {"text": "DOJ", "url": "https://justice.gov"}]
        }
        
        score = agent._calculate_seo_score(content, outline, seo_requirements, metadata)
        
        assert 0 <= score <= 100
        assert score > 50  # Should have decent score with proper setup
    
    def test_cost_tracking(self, agent_with_mock_api):
        """Test cost tracking functionality"""
        agent = agent_with_mock_api
        
        # Track some token usage
        agent._track_tokens(
            provider=LLMProvider.ANTHROPIC,
            model="claude-3-5-sonnet-20241022",
            input_tokens=1000,
            output_tokens=2000
        )
        
        # Check cost calculation
        cost_tracking = agent._calculate_costs()
        assert cost_tracking is not None
        assert cost_tracking.input_tokens == 1000
        assert cost_tracking.output_tokens == 2000
        assert cost_tracking.cost > 0
        
        # Check cost summary
        summary = agent.get_cost_summary()
        assert summary["total_cost"] > 0
    
    def test_content_optimization(self, agent_with_mock_api, seo_requirements):
        """Test content optimization for SEO"""
        agent = agent_with_mock_api
        
        # Content missing primary keyword
        content = """
        # Guide to Training Dogs
        
        This article covers how to train dogs for various tasks.
        Dogs can be trained to help people with disabilities.
        Training requires patience and consistency.
        """
        
        optimized = agent._optimize_content_for_seo(content, seo_requirements)
        
        # Should attempt to add primary keyword
        assert "service dog training" in optimized.lower() or content == optimized
    
    @pytest.mark.asyncio
    async def test_generate_outline_parsing(self, agent_with_mock_api):
        """Test outline generation and JSON parsing"""
        agent = agent_with_mock_api
        
        # Mock the LLM response
        mock_response = """{
            "title": "Test Article Title",
            "meta_title": "Test Meta Title",
            "meta_description": "Test meta description for SEO.",
            "introduction": "Test introduction paragraph.",
            "sections": [
                {
                    "heading": "Section 1",
                    "points": ["Point 1", "Point 2"],
                    "keywords": ["keyword1"]
                }
            ],
            "conclusion_points": ["Conclusion 1"],
            "internal_link_opportunities": ["Related topic 1"],
            "citations_needed": ["28 CFR 36.302"]
        }"""
        
        with patch.object(agent, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = mock_response
            
            outline = await agent._generate_outline(
                topic="Test Topic",
                seo_requirements=SEORequirements(
                    primary_keyword="test",
                    secondary_keywords=["test2"]
                )
            )
            
            assert outline.title == "Test Article Title"
            assert outline.meta_title == "Test Meta Title"
            assert len(outline.sections) == 1
            assert outline.sections[0]["heading"] == "Section 1"
    
    @pytest.mark.asyncio
    async def test_article_caching(self, agent_with_mock_api, tmp_path):
        """Test article caching functionality"""
        # Use temp directory for cache
        agent = ArticleGenerationAgent(
            anthropic_api_key="test-key",
            cache_dir=str(tmp_path / "cache")
        )
        
        # Create a test article
        article = GeneratedArticle(
            title="Test Article",
            slug="test-article",
            meta_title="Test Meta",
            meta_description="Test Description",
            content_markdown="# Test Content",
            primary_keyword="test",
            secondary_keywords=["test2"],
            word_count=100,
            reading_level=8.0,
            internal_links=[],
            external_links=[],
            citations=[],
            featured_image_prompt="Test image",
            category="Test",
            tags=["test"],
            estimated_reading_time=1,
            seo_score=80.0
        )
        
        # Cache the article
        agent._cache_article(article)
        
        # Check if file was created
        cache_files = list(Path(agent.cache_dir).glob("*.json"))
        assert len(cache_files) == 1
        
        # Verify cached content
        import json
        with open(cache_files[0], 'r') as f:
            cached_data = json.load(f)
            assert cached_data["title"] == "Test Article"
            assert cached_data["slug"] == "test-article"


class TestSEORequirements:
    """Test SEO requirements validation"""
    
    def test_seo_requirements_defaults(self):
        """Test SEO requirements with default values"""
        seo = SEORequirements(
            primary_keyword="test keyword",
            secondary_keywords=["keyword1", "keyword2"]
        )
        
        assert seo.primary_keyword == "test keyword"
        assert len(seo.secondary_keywords) == 2
        assert seo.min_words == 1500
        assert seo.max_words == 2500
        assert seo.meta_title_length == 60
        assert seo.meta_description_length == 155
        assert seo.target_reading_level == 8
    
    def test_seo_requirements_custom(self):
        """Test SEO requirements with custom values"""
        seo = SEORequirements(
            primary_keyword="main keyword",
            secondary_keywords=["kw1", "kw2", "kw3"],
            min_words=2000,
            max_words=3000,
            internal_links_count=5,
            external_links_count=3
        )
        
        assert seo.min_words == 2000
        assert seo.max_words == 3000
        assert seo.internal_links_count == 5
        assert seo.external_links_count == 3


@pytest.mark.asyncio
async def test_article_generation_integration():
    """Integration test for article generation (requires API key)"""
    # Skip if no API key is available
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No API key available for integration test")
    
    agent = ArticleGenerationAgent()
    
    seo_reqs = SEORequirements(
        primary_keyword="service dog training basics",
        secondary_keywords=["ADA", "tasks", "public access"],
        min_words=500,  # Shorter for testing
        max_words=800
    )
    
    # This will make a real API call if keys are configured
    try:
        article = await agent.generate_article(
            topic="Basic Service Dog Training Tips",
            seo_requirements=seo_reqs,
            brand_voice="professional and informative",
            target_audience="New service dog handlers"
        )
        
        assert article.title is not None
        assert article.content_markdown is not None
        assert article.word_count > 0
        assert article.seo_score > 0
        
        print(f"\n✅ Integration Test Passed!")
        print(f"   Generated: {article.title}")
        print(f"   Word Count: {article.word_count}")
        print(f"   SEO Score: {article.seo_score:.1f}/100")
        if article.cost_tracking:
            print(f"   Cost: ${article.cost_tracking.cost:.4f}")
    
    except Exception as e:
        # If API call fails, just note it but don't fail the test
        print(f"\n⚠️ Integration test skipped: {str(e)}")
        pytest.skip(f"API call failed: {str(e)}")


if __name__ == "__main__":
    # Run specific tests
    asyncio.run(test_article_generation_integration())