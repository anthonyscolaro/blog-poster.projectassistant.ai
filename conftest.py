"""
Pytest configuration and shared fixtures for blog-poster test suite
"""
import asyncio
import os
import tempfile
from typing import Generator, AsyncGenerator
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Add project root to Python path
import sys
sys.path.insert(0, str(Path(__file__).parent))

# Import application modules
from app import app
from agents.article_generation_agent import ArticleGenerationAgent, SEORequirements
from agents.competitor_monitoring_agent import CompetitorMonitoringAgent
from agents.topic_analysis_agent import TopicAnalysisAgent
from agents.legal_fact_checker_agent import LegalFactCheckerAgent
from wordpress_publisher import WordPressPublisher
from vector_search import VectorSearchManager
from orchestration_manager import OrchestrationManager


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def test_env_vars() -> Generator[None, None, None]:
    """Set up test environment variables"""
    test_vars = {
        "ANTHROPIC_API_KEY": "test-anthropic-key",
        "OPENAI_API_KEY": "test-openai-key",
        "JINA_API_KEY": "test-jina-key",
        "WORDPRESS_URL": "https://test.example.com",
        "WP_USERNAME": "test_user",
        "WP_APP_PASSWORD": "test pass word 123",
        "WP_VERIFY_SSL": "false",
        "QDRANT_URL": "http://localhost:6333",
        "REDIS_URL": "redis://localhost:6379",
        "POSTGRES_URL": "postgresql://user:pass@localhost:5432/testdb"
    }
    
    with patch.dict(os.environ, test_vars):
        yield


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create test client for FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async test client for FastAPI app"""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
def seo_requirements() -> SEORequirements:
    """Standard SEO requirements for testing"""
    return SEORequirements(
        primary_keyword="service dog training",
        secondary_keywords=["ADA", "disability", "public access", "tasks"],
        min_words=1500,
        max_words=2500,
        internal_links_count=3,
        external_links_count=2
    )


@pytest.fixture
def mock_anthropic_response() -> str:
    """Mock Anthropic API response"""
    return """# Service Dog Training Guide

Service dog training is essential for handlers who need reliable assistance animals.

## Understanding ADA Requirements

The ADA requires that service dogs be individually trained to perform tasks.

## Training Process

1. Basic obedience training
2. Task-specific training  
3. Public access training

Service dogs must be trained to perform specific tasks that mitigate their handler's disability."""


@pytest.fixture
def mock_article_generation_agent(test_env_vars, temp_dir) -> ArticleGenerationAgent:
    """Create mocked article generation agent"""
    agent = ArticleGenerationAgent(
        anthropic_api_key="test-key",
        cache_dir=temp_dir
    )
    
    # Mock the LLM call
    async def mock_call_llm(*args, **kwargs):
        return """{"title": "Test Article", "meta_title": "Test Meta", "meta_description": "Test description", "introduction": "Test intro", "sections": [], "conclusion_points": [], "internal_link_opportunities": [], "citations_needed": []}"""
    
    agent._call_llm = AsyncMock(side_effect=mock_call_llm)
    return agent


@pytest.fixture
def mock_competitor_monitoring_agent(test_env_vars) -> CompetitorMonitoringAgent:
    """Create mocked competitor monitoring agent"""
    agent = CompetitorMonitoringAgent()
    
    # Mock scraping methods
    agent.scrape_competitor_content = AsyncMock(return_value=[
        {"title": "Competitor Article 1", "url": "https://example.com/1", "content": "Test content 1"},
        {"title": "Competitor Article 2", "url": "https://example.com/2", "content": "Test content 2"}
    ])
    
    return agent


@pytest.fixture
def mock_topic_analysis_agent(test_env_vars) -> TopicAnalysisAgent:
    """Create mocked topic analysis agent"""
    agent = TopicAnalysisAgent()
    
    # Mock analysis methods
    async def mock_analyze(*args, **kwargs):
        from agents.topic_analysis_agent import TopicAnalysisReport, TopicRecommendation
        from datetime import datetime
        
        return TopicAnalysisReport(
            keywords_analyzed=["service dog", "training"],
            content_gaps_found=1,
            topics_recommended=1,
            recommendations=[
                TopicRecommendation(
                    title="Service Dog Training Basics",
                    slug="service-dog-training-basics",
                    primary_keyword="service dog training",
                    secondary_keywords=["ADA", "tasks"],
                    content_type="guide",
                    target_word_count=1500,
                    priority_score=85.0,
                    rationale="High demand topic",
                    content_outline=["Introduction", "Training steps", "Conclusion"]
                )
            ],
            content_gaps=[],
            market_insights={},
            analyzed_at=datetime.now()
        )
    
    agent.analyze_topics = AsyncMock(side_effect=mock_analyze)
    return agent


@pytest.fixture
def mock_legal_fact_checker_agent(test_env_vars) -> LegalFactCheckerAgent:
    """Create mocked legal fact checker agent"""
    agent = LegalFactCheckerAgent()
    
    # Mock fact checking methods
    async def mock_verify(*args, **kwargs):
        from agents.legal_fact_checker_agent import FactCheckReport
        from datetime import datetime
        
        return FactCheckReport(
            article_title="Test Article",
            total_claims=5,
            verified_claims=4,
            incorrect_claims=0,
            unverified_claims=1,
            claim_details=[],
            legal_citations_found=["28 CFR §36.302"],
            overall_accuracy_score=80.0,
            recommendations=[],
            checked_at=datetime.now()
        )
    
    agent.verify_legal_claims = AsyncMock(side_effect=mock_verify)
    return agent


@pytest.fixture
def mock_wordpress_publisher(test_env_vars) -> WordPressPublisher:
    """Create mocked WordPress publisher"""
    publisher = WordPressPublisher()
    
    # Mock publishing methods
    publisher.test_connection = AsyncMock(return_value=True)
    publisher.create_post = AsyncMock(return_value={
        "success": True,
        "post_id": 123,
        "edit_link": "https://test.example.com/wp-admin/post.php?post=123&action=edit",
        "view_link": "https://test.example.com/test-article"
    })
    publisher.get_categories = AsyncMock(return_value=[
        {"id": 1, "name": "Service Dogs"},
        {"id": 2, "name": "Training"}
    ])
    publisher.get_tags = AsyncMock(return_value=[
        {"id": 1, "name": "ADA"},
        {"id": 2, "name": "Training"}
    ])
    
    return publisher


@pytest.fixture
def mock_vector_search_manager(test_env_vars) -> VectorSearchManager:
    """Create mocked vector search manager"""
    manager = VectorSearchManager()
    
    # Mock vector operations
    manager.index_document = AsyncMock(return_value=True)
    manager.search = AsyncMock(return_value=[])
    manager.check_duplicate = AsyncMock(return_value=None)
    manager.get_internal_links = AsyncMock(return_value=[])
    manager.get_collection_stats = Mock(return_value={"documents": 0, "size": "0MB"})
    
    return manager


@pytest.fixture
def mock_orchestration_manager(
    mock_article_generation_agent,
    mock_competitor_monitoring_agent, 
    mock_topic_analysis_agent,
    mock_legal_fact_checker_agent,
    mock_wordpress_publisher
) -> OrchestrationManager:
    """Create mocked orchestration manager"""
    manager = OrchestrationManager()
    
    # Inject mocked agents
    manager.competitor_agent = mock_competitor_monitoring_agent
    manager.topic_agent = mock_topic_analysis_agent
    manager.article_agent = mock_article_generation_agent
    manager.fact_checker_agent = mock_legal_fact_checker_agent
    manager.wordpress_publisher = mock_wordpress_publisher
    
    return manager


@pytest.fixture(autouse=True)
def mock_external_services():
    """Auto-mock external service calls"""
    with patch('httpx.AsyncClient') as mock_client:
        # Mock successful HTTP responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_response.text = "Mock response content"
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response)
        
        yield


@pytest.fixture
def sample_article_data() -> dict:
    """Sample article data for testing"""
    return {
        "title": "Complete Guide to Service Dog Training",
        "content": "# Service Dog Training\n\nThis is a comprehensive guide to training service dogs...",
        "status": "draft",
        "slug": "service-dog-training-guide",
        "categories": [1],
        "tags": [1, 2],
        "meta_title": "Service Dog Training: Complete Guide",
        "meta_description": "Learn everything about service dog training with our comprehensive guide covering ADA requirements and training methods."
    }


@pytest.fixture
def sample_seo_content() -> dict:
    """Sample content for SEO testing"""
    return {
        "frontmatter": {
            "meta_title": "Test Article Title That Fits Within Limits",
            "meta_desc": "This is a meta description that fits within the SEO limits and provides good information about the article content for search engines.",
            "canonical": "https://example.com/test-article"
        },
        "markdown": """# Test Article Title

This is the main content of the article. It contains the primary keyword service dog training multiple times throughout the content.

## Section 1

More content about service dog training and ADA requirements.

![Service dog in training](https://example.com/image.jpg "Service dog performing tasks")

## Section 2

Additional information about training methods and public access rights.

The article continues with valuable information for readers."""
    }


# Test data generators
def generate_test_article(word_count: int = 1500) -> str:
    """Generate test article content with specified word count"""
    words = ["service", "dog", "training", "ADA", "disability", "tasks", "handler", "public", "access", "rights"]
    content = "# Test Article\n\n"
    
    current_count = 0
    while current_count < word_count:
        sentence = " ".join(words[:5]) + ". "
        content += sentence
        current_count += len(sentence.split())
        words = words[1:] + words[:1]  # Rotate words
    
    return content


def generate_mock_competitor_content(count: int = 5) -> list:
    """Generate mock competitor content for testing"""
    return [
        {
            "title": f"Competitor Article {i+1}",
            "url": f"https://competitor{i+1}.com/article",
            "content": f"This is competitor content {i+1} about service dogs and training.",
            "scraped_at": "2024-01-01T00:00:00Z"
        }
        for i in range(count)
    ]


# Async test helpers
def run_async_test(coro):
    """Helper to run async tests"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


# Test markers
pytestmark = pytest.mark.asyncio