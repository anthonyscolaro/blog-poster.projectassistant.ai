"""
Test suite for FastAPI endpoints
"""
import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from httpx import AsyncClient
from app import app


class TestHealthEndpoint:
    """Test health endpoint"""
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        with TestClient(app) as client:
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert "time" in data


class TestSEOLintEndpoint:
    """Test SEO linting endpoint"""
    
    def test_seo_lint_valid_content(self):
        """Test SEO linting with valid content"""
        with TestClient(app) as client:
            request_data = {
                "frontmatter": {
                    "meta_title": "Service Dog Training: Complete Guide for New Handlers",
                    "meta_desc": "Learn everything about service dog training with our comprehensive guide covering ADA requirements, training methods, and public access rights for handlers.",
                    "canonical": "https://example.com/service-dog-training"
                },
                "markdown": """# Service Dog Training Guide

This comprehensive guide covers service dog training essentials.

![Service dog in training](https://example.com/image.jpg "Service dog performing tasks")

## Training Requirements

Service dogs must be individually trained to perform specific tasks."""
            }
            
            response = client.post("/seo/lint", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "violations" in data
            assert isinstance(data["violations"], list)
    
    def test_seo_lint_invalid_content(self):
        """Test SEO linting with invalid content"""
        with TestClient(app) as client:
            request_data = {
                "frontmatter": {
                    "meta_title": "Too Short",  # Too short for SEO
                    "meta_desc": "Short",      # Too short for SEO
                    # Missing canonical
                },
                "markdown": """# Heading 1

# Another H1

![Missing alt text](image.jpg)"""  # Multiple H1s and missing alt text
            }
            
            response = client.post("/seo/lint", json=request_data)
            
            assert response.status_code == 200
            data = response.json()
            assert "violations" in data
            violations = data["violations"]
            
            # Should have multiple violations
            assert len(violations) > 0
            # Check for specific violations
            violations_text = " ".join(violations)
            assert "meta_title" in violations_text or "meta_desc" in violations_text


class TestWordPressPublishingEndpoint:
    """Test WordPress publishing endpoints"""
    
    @pytest.mark.asyncio
    async def test_wordpress_publish_success(self):
        """Test successful WordPress publishing"""
        # Mock the WordPress publisher
        mock_result = {
            "success": True,
            "post_id": 123,
            "edit_link": "https://test.com/wp-admin/post.php?post=123&action=edit",
            "view_link": "https://test.com/test-article"
        }
        
        with patch("wordpress_publisher.WordPressPublisher") as mock_publisher_class:
            mock_publisher = mock_publisher_class.return_value
            mock_publisher.test_connection = AsyncMock(return_value=True)
            mock_publisher.create_post = AsyncMock(return_value=mock_result)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(
                    "/publish/wp",
                    params={
                        "title": "Test Article",
                        "content": "<p>Test content</p>",
                        "status": "draft",
                        "slug": "test-article"
                    }
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert data["post_id"] == 123
    
    @pytest.mark.asyncio
    async def test_wordpress_connection_failure(self):
        """Test WordPress connection failure"""
        with patch("wordpress_publisher.WordPressPublisher") as mock_publisher_class:
            mock_publisher = mock_publisher_class.return_value
            mock_publisher.test_connection = AsyncMock(return_value=False)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(
                    "/publish/wp",
                    params={
                        "title": "Test Article",
                        "content": "<p>Test content</p>"
                    }
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is False
                assert "error" in data
    
    @pytest.mark.asyncio
    async def test_wordpress_test_endpoint(self):
        """Test WordPress connection test endpoint"""
        mock_categories = [{"id": 1, "name": "Service Dogs"}]
        mock_tags = [{"id": 1, "name": "ADA"}]
        
        with patch("wordpress_publisher.WordPressPublisher") as mock_publisher_class:
            mock_publisher = mock_publisher_class.return_value
            mock_publisher.test_connection = AsyncMock(return_value=True)
            mock_publisher.get_categories = AsyncMock(return_value=mock_categories)
            mock_publisher.get_tags = AsyncMock(return_value=mock_tags)
            mock_publisher.wordpress_url = "https://test.com"
            mock_publisher.auth_method = "basic"
            mock_publisher.is_local = False
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/wordpress/test")
                
                assert response.status_code == 200
                data = response.json()
                assert data["connected"] is True
                assert "categories" in data
                assert "tags" in data


class TestAgentRunEndpoint:
    """Test agent run endpoint"""
    
    @pytest.mark.asyncio
    async def test_agent_run_success(self):
        """Test successful agent run"""
        # Mock the agent response
        mock_article = Mock()
        mock_article.title = "Test Generated Article"
        mock_article.content_markdown = "# Test Article\n\nContent here..."
        mock_article.meta_title = "Test Meta Title"
        mock_article.meta_description = "Test meta description"
        mock_article.primary_keyword = "service dogs"
        mock_article.word_count = 1500
        mock_article.seo_score = 85.0
        mock_article.estimated_reading_time = 7
        mock_article.cost_tracking = Mock()
        mock_article.cost_tracking.cost = 0.45
        
        with patch("agents.ArticleGenerationAgent") as mock_agent_class:
            mock_agent = mock_agent_class.return_value
            mock_agent.generate_article = AsyncMock(return_value=mock_article)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                payload = {
                    "topic_rec": {
                        "topic_slug": "service-dog-training",
                        "primary_kw": "service dog training",
                        "secondary_kws": ["ADA", "tasks"],
                        "title_variants": ["Service Dog Training Guide"],
                        "rationale": "High demand topic"
                    },
                    "brand_style": {
                        "voice": "professional",
                        "audience": "dog handlers",
                        "tone": "informative"
                    },
                    "site_info": {
                        "site_url": "https://example.com",
                        "canonical_base": "https://example.com",
                        "category_map": {"training": 1}
                    },
                    "evidence": {
                        "facts": ["Service dogs are trained animals"],
                        "statutes": ["28 CFR §36.302"],
                        "sources": ["https://ada.gov"]
                    },
                    "constraints": {
                        "min_words": 1500,
                        "max_words": 2500
                    }
                }
                
                response = await client.post("/agent/run", json=payload)
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "output" in data
                assert "Test Generated Article" in data["output"]


class TestCompetitorEndpoints:
    """Test competitor monitoring endpoints"""
    
    @pytest.mark.asyncio
    async def test_competitors_scan(self):
        """Test competitor scanning endpoint"""
        with patch("agents.CompetitorMonitoringAgent") as mock_agent_class:
            mock_agent = mock_agent_class.return_value
            mock_content = [
                {"title": "Competitor Article 1", "url": "https://comp1.com/article1"},
                {"title": "Competitor Article 2", "url": "https://comp2.com/article2"}
            ]
            mock_agent.scan_competitors = AsyncMock(return_value=mock_content)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/competitors/scan")
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert data["content_pieces"] == 2
    
    @pytest.mark.asyncio
    async def test_competitors_insights(self):
        """Test competitor insights endpoint"""
        mock_insights = Mock()
        mock_insights.dict.return_value = {
            "trending_topics": [
                {"topic": "Service dog training", "score": 85.0}
            ],
            "content_gaps": [
                {"topic": "PTSD service dogs", "score": 90.0}
            ]
        }
        
        with patch("agents.CompetitorMonitoringAgent") as mock_agent_class:
            mock_agent = mock_agent_class.return_value
            mock_agent.generate_insights = AsyncMock(return_value=mock_insights)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/competitors/insights")
                
                assert response.status_code == 200
                data = response.json()
                assert "trending_topics" in data
                assert "content_gaps" in data


class TestTopicAnalysisEndpoints:
    """Test topic analysis endpoints"""
    
    @pytest.mark.asyncio
    async def test_topics_analyze(self):
        """Test topic analysis endpoint"""
        mock_report = Mock()
        mock_report.keywords_analyzed = ["service dogs", "training"]
        mock_report.content_gaps_found = 1
        mock_report.topics_recommended = 1
        mock_report.recommendations = [
            Mock(
                title="Service Dog Training Guide",
                slug="service-dog-training-guide",
                primary_keyword="service dog training",
                secondary_keywords=["ADA", "tasks"],
                content_type="guide",
                target_word_count=1500,
                priority_score=85.0,
                rationale="High demand",
                content_outline=["Intro", "Training", "Conclusion"]
            )
        ]
        mock_report.market_insights = {}
        mock_report.analyzed_at.isoformat.return_value = "2024-01-01T00:00:00"
        
        with patch("agents.topic_analysis_agent.TopicAnalysisAgent") as mock_agent_class:
            mock_agent = mock_agent_class.return_value
            mock_agent.analyze_topics = AsyncMock(return_value=mock_report)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(
                    "/topics/analyze",
                    json={
                        "keywords": ["service dogs"],
                        "max_recommendations": 5
                    }
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["keywords_analyzed"] == ["service dogs", "training"]
                assert len(data["recommendations"]) == 1


class TestVectorSearchEndpoints:
    """Test vector search endpoints"""
    
    @pytest.mark.asyncio
    async def test_vector_index_document(self):
        """Test document indexing"""
        with patch("vector_search.VectorSearchManager") as mock_manager_class:
            mock_manager = mock_manager_class.return_value
            mock_manager.index_document = AsyncMock(return_value=True)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                request_data = {
                    "content": "Test article content about service dogs",
                    "document_id": "test-article-123",
                    "title": "Test Article",
                    "url": "https://example.com/test-article",
                    "collection": "blog_articles"
                }
                
                response = await client.post("/vector/index", json=request_data)
                
                assert response.status_code == 200
                data = response.json()
                assert data["success"] is True
                assert "test-article-123" in data["message"]
    
    @pytest.mark.asyncio
    async def test_vector_search_documents(self):
        """Test document search"""
        mock_results = [
            Mock(
                document_title="Service Dog Guide",
                content="Content about service dogs...",
                document_url="https://example.com/guide",
                similarity_score=0.85
            )
        ]
        
        with patch("vector_search.VectorSearchManager") as mock_manager_class:
            mock_manager = mock_manager_class.return_value
            mock_manager.search = AsyncMock(return_value=mock_results)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                request_data = {
                    "query": "service dog training",
                    "limit": 5,
                    "collection": "blog_articles"
                }
                
                response = await client.post("/vector/search", json=request_data)
                
                assert response.status_code == 200
                data = response.json()
                assert data["query"] == "service dog training"
                assert len(data["results"]) == 1
                assert data["results"][0]["title"] == "Service Dog Guide"


class TestPipelineEndpoints:
    """Test orchestration pipeline endpoints"""
    
    @pytest.mark.asyncio
    async def test_pipeline_run_success(self):
        """Test successful pipeline execution"""
        mock_result = Mock()
        mock_result.status = "completed"
        mock_result.execution_time = 45.5
        mock_result.total_cost = 1.25
        mock_result.errors = []
        mock_result.warnings = []
        mock_result.article = Mock()
        mock_result.article.title = "Generated Article"
        mock_result.article.word_count = 1500
        mock_result.article.seo_score = 85.0
        mock_result.article.slug = "generated-article"
        mock_result.fact_check_report = None
        mock_result.wordpress_result = None
        
        with patch("orchestration_manager.OrchestrationManager") as mock_manager_class:
            mock_manager = mock_manager_class.return_value
            mock_manager.run_pipeline = AsyncMock(return_value=mock_result)
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                config = {
                    "topic": "Service dog training basics",
                    "enable_competitor_monitoring": True,
                    "enable_topic_analysis": True,
                    "enable_fact_checking": True,
                    "enable_wordpress_publishing": False
                }
                
                response = await client.post("/pipeline/run", json=config)
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "completed"
                assert data["execution_time"] == 45.5
                assert "article" in data
    
    @pytest.mark.asyncio
    async def test_pipeline_status(self):
        """Test pipeline status endpoint"""
        with patch("orchestration_manager.OrchestrationManager") as mock_manager_class:
            mock_manager = mock_manager_class.return_value
            mock_manager.get_pipeline_status.return_value = "article_generation"
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get("/pipeline/status")
                
                assert response.status_code == 200
                data = response.json()
                assert data["running"] is True
                assert data["status"] == "article_generation"


class TestDashboardEndpoints:
    """Test dashboard HTML endpoints"""
    
    def test_dashboard_home(self):
        """Test main dashboard page"""
        with TestClient(app) as client:
            response = client.get("/")
            
            # Should return HTML
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]
    
    def test_health_dashboard(self):
        """Test health dashboard page"""
        with TestClient(app) as client:
            response = client.get("/health-dashboard")
            
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]
    
    def test_pipeline_dashboard(self):
        """Test pipeline dashboard page"""
        with TestClient(app) as client:
            response = client.get("/pipeline")
            
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])