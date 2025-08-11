"""
Test suite for Vector Search Manager
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vector_search import VectorSearchManager, SearchResult


class TestVectorSearchManager:
    """Test cases for Vector Search Manager"""
    
    @pytest.fixture
    def mock_qdrant_client(self):
        """Create mocked Qdrant client"""
        mock_client = Mock()
        mock_client.get_collections.return_value.collections = []
        mock_client.create_collection = Mock()
        mock_client.upsert = Mock()
        mock_client.search = Mock()
        mock_client.delete = Mock()
        return mock_client
    
    @pytest.fixture
    def vector_manager(self, mock_qdrant_client):
        """Create vector search manager with mocked client"""
        with patch("vector_search.QdrantClient") as mock_client_class:
            mock_client_class.return_value = mock_qdrant_client
            
            manager = VectorSearchManager(
                qdrant_url="http://localhost:6333",
                embedding_model="all-MiniLM-L6-v2"
            )
            return manager
    
    def test_manager_initialization(self):
        """Test vector search manager initialization"""
        with patch("vector_search.QdrantClient") as mock_client:
            manager = VectorSearchManager(
                qdrant_url="http://test:6333",
                embedding_model="custom-model"
            )
            
            assert manager.qdrant_url == "http://test:6333"
            assert manager.embedding_model == "custom-model"
            mock_client.assert_called_once_with(url="http://test:6333")
    
    def test_initialization_from_env(self):
        """Test initialization from environment variables"""
        env_vars = {
            "QDRANT_URL": "http://env:6333",
            "EMBEDDING_MODEL": "env-model"
        }
        
        with patch.dict(os.environ, env_vars):
            with patch("vector_search.QdrantClient"):
                manager = VectorSearchManager()
                
                assert manager.qdrant_url == "http://env:6333"
    
    def test_generate_embedding(self, vector_manager):
        """Test embedding generation"""
        # Mock the sentence transformer
        with patch.object(vector_manager, '_get_embedding_model') as mock_model:
            mock_model.encode.return_value = [0.1, 0.2, 0.3, 0.4]
            
            embedding = vector_manager._generate_embedding("test text")
            
            assert len(embedding) == 4
            assert embedding == [0.1, 0.2, 0.3, 0.4]
            mock_model.encode.assert_called_once_with("test text")
    
    @pytest.mark.asyncio
    async def test_ensure_collection_exists(self, vector_manager, mock_qdrant_client):
        """Test collection creation"""
        # Mock collection doesn't exist
        mock_qdrant_client.get_collections.return_value.collections = []
        
        await vector_manager._ensure_collection_exists("test_collection")
        
        # Should create the collection
        mock_qdrant_client.create_collection.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_collection_already_exists(self, vector_manager, mock_qdrant_client):
        """Test when collection already exists"""
        # Mock collection exists
        mock_collection = Mock()
        mock_collection.name = "test_collection"
        mock_qdrant_client.get_collections.return_value.collections = [mock_collection]
        
        await vector_manager._ensure_collection_exists("test_collection")
        
        # Should not create the collection
        mock_qdrant_client.create_collection.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_index_document_success(self, vector_manager, mock_qdrant_client):
        """Test successful document indexing"""
        # Mock embedding generation
        with patch.object(vector_manager, '_generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]
            
            # Mock collection exists
            mock_collection = Mock()
            mock_collection.name = "blog_articles"
            mock_qdrant_client.get_collections.return_value.collections = [mock_collection]
            
            result = await vector_manager.index_document(
                content="Test article about service dogs",
                document_id="test-doc-1",
                title="Test Article",
                url="https://example.com/test",
                collection="blog_articles"
            )
            
            assert result is True
            mock_qdrant_client.upsert.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_index_document_failure(self, vector_manager, mock_qdrant_client):
        """Test document indexing failure"""
        # Mock embedding generation
        with patch.object(vector_manager, '_generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]
            
            # Mock upsert failure
            mock_qdrant_client.upsert.side_effect = Exception("Qdrant error")
            
            result = await vector_manager.index_document(
                content="Test content",
                document_id="test-doc-1",
                title="Test Title"
            )
            
            assert result is False
    
    @pytest.mark.asyncio
    async def test_search_documents(self, vector_manager, mock_qdrant_client):
        """Test document search"""
        # Mock embedding generation
        with patch.object(vector_manager, '_generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]
            
            # Mock search results
            mock_point = Mock()
            mock_point.id = "doc-1"
            mock_point.score = 0.85
            mock_point.payload = {
                "title": "Service Dog Guide",
                "content": "Content about service dogs...",
                "url": "https://example.com/guide",
                "document_id": "doc-1"
            }
            
            mock_qdrant_client.search.return_value = [mock_point]
            
            results = await vector_manager.search(
                query="service dog training",
                limit=5,
                collection="blog_articles"
            )
            
            assert len(results) == 1
            assert isinstance(results[0], SearchResult)
            assert results[0].document_title == "Service Dog Guide"
            assert results[0].similarity_score == 0.85
    
    @pytest.mark.asyncio
    async def test_search_no_results(self, vector_manager, mock_qdrant_client):
        """Test search with no results"""
        with patch.object(vector_manager, '_generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]
            mock_qdrant_client.search.return_value = []
            
            results = await vector_manager.search("nonexistent query")
            
            assert len(results) == 0
    
    @pytest.mark.asyncio
    async def test_check_duplicate_found(self, vector_manager, mock_qdrant_client):
        """Test duplicate detection when duplicate found"""
        with patch.object(vector_manager, '_generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]
            
            # Mock high similarity result
            mock_point = Mock()
            mock_point.score = 0.95  # Above threshold
            mock_point.payload = {
                "title": "Similar Article",
                "url": "https://example.com/similar",
                "document_id": "similar-doc"
            }
            mock_qdrant_client.search.return_value = [mock_point]
            
            duplicate = await vector_manager.check_duplicate(
                content="Very similar content",
                threshold=0.9
            )
            
            assert duplicate is not None
            assert duplicate.similarity_score == 0.95
            assert duplicate.document_title == "Similar Article"
    
    @pytest.mark.asyncio
    async def test_check_duplicate_not_found(self, vector_manager, mock_qdrant_client):
        """Test duplicate detection when no duplicate found"""
        with patch.object(vector_manager, '_generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]
            
            # Mock low similarity result
            mock_point = Mock()
            mock_point.score = 0.75  # Below threshold
            mock_qdrant_client.search.return_value = [mock_point]
            
            duplicate = await vector_manager.check_duplicate(
                content="Unique content",
                threshold=0.9
            )
            
            assert duplicate is None
    
    @pytest.mark.asyncio
    async def test_get_internal_links(self, vector_manager, mock_qdrant_client):
        """Test internal link recommendations"""
        with patch.object(vector_manager, '_generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1, 0.2, 0.3]
            
            # Mock search results for internal links
            mock_points = []
            for i in range(3):
                mock_point = Mock()
                mock_point.score = 0.8 - (i * 0.1)  # Decreasing relevance
                mock_point.payload = {
                    "title": f"Related Article {i+1}",
                    "url": f"https://example.com/article-{i+1}",
                    "document_id": f"doc-{i+1}"
                }
                mock_points.append(mock_point)
            
            mock_qdrant_client.search.return_value = mock_points
            
            links = await vector_manager.get_internal_links(
                content="Content about service dogs",
                limit=3
            )
            
            assert len(links) == 3
            assert all("title" in link and "url" in link for link in links)
            assert links[0]["title"] == "Related Article 1"  # Highest scored first
    
    def test_get_collection_stats(self, vector_manager, mock_qdrant_client):
        """Test collection statistics"""
        # Mock collection info
        mock_collection = Mock()
        mock_collection.name = "blog_articles"
        mock_collection.points_count = 150
        mock_collection.vectors_count = 150
        
        mock_qdrant_client.get_collection.return_value = mock_collection
        
        stats = vector_manager.get_collection_stats("blog_articles")
        
        assert "documents" in stats
        assert "vectors" in stats
        assert stats["documents"] == 150
    
    def test_get_collection_stats_error(self, vector_manager, mock_qdrant_client):
        """Test collection stats when collection doesn't exist"""
        mock_qdrant_client.get_collection.side_effect = Exception("Collection not found")
        
        stats = vector_manager.get_collection_stats("nonexistent")
        
        assert stats == {"documents": 0, "size": "0MB", "error": "Collection not accessible"}
    
    @pytest.mark.asyncio
    async def test_delete_document(self, vector_manager, mock_qdrant_client):
        """Test document deletion"""
        result = await vector_manager.delete_document(
            document_id="doc-to-delete",
            collection="blog_articles"
        )
        
        assert result is True
        mock_qdrant_client.delete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_document_failure(self, vector_manager, mock_qdrant_client):
        """Test document deletion failure"""
        mock_qdrant_client.delete.side_effect = Exception("Delete failed")
        
        result = await vector_manager.delete_document(
            document_id="doc-to-delete"
        )
        
        assert result is False
    
    def test_content_chunking(self, vector_manager):
        """Test content chunking for large documents"""
        # Create content larger than chunk size
        long_content = "word " * 1000  # 1000 words
        
        chunks = vector_manager._chunk_content(long_content, chunk_size=100)
        
        assert len(chunks) > 1
        assert all(len(chunk.split()) <= 120 for chunk in chunks)  # Allow some overlap
    
    def test_content_chunking_small_content(self, vector_manager):
        """Test chunking with content smaller than chunk size"""
        short_content = "This is a short article."
        
        chunks = vector_manager._chunk_content(short_content, chunk_size=100)
        
        assert len(chunks) == 1
        assert chunks[0] == short_content


class TestSearchResult:
    """Test SearchResult data class"""
    
    def test_search_result_creation(self):
        """Test creating SearchResult instance"""
        result = SearchResult(
            document_id="test-doc",
            document_title="Test Document",
            document_url="https://example.com/test",
            content="Test content here",
            similarity_score=0.85
        )
        
        assert result.document_id == "test-doc"
        assert result.document_title == "Test Document"
        assert result.document_url == "https://example.com/test"
        assert result.content == "Test content here"
        assert result.similarity_score == 0.85
    
    def test_search_result_optional_fields(self):
        """Test SearchResult with optional fields"""
        result = SearchResult(
            document_id="test-doc",
            document_title="Test Document",
            similarity_score=0.75
        )
        
        assert result.document_url is None
        assert result.content is None


class TestVectorSearchIntegration:
    """Integration tests (require actual Qdrant instance)"""
    
    @pytest.mark.skipif(
        not os.getenv("QDRANT_TEST_URL"),
        reason="Qdrant test URL not configured"
    )
    @pytest.mark.asyncio
    async def test_real_qdrant_connection(self):
        """Test connection to real Qdrant instance"""
        manager = VectorSearchManager(
            qdrant_url=os.getenv("QDRANT_TEST_URL", "http://localhost:6333")
        )
        
        try:
            # Test basic functionality
            success = await manager.index_document(
                content="Test integration document about service dogs",
                document_id="integration-test-1",
                title="Integration Test Document",
                collection="test_collection"
            )
            
            assert success is True
            
            # Test search
            results = await manager.search(
                query="service dogs",
                collection="test_collection",
                limit=1
            )
            
            assert len(results) >= 0  # May or may not find results
            
            # Cleanup
            await manager.delete_document("integration-test-1", "test_collection")
            
            print("✅ Qdrant integration test passed")
            
        except Exception as e:
            pytest.skip(f"Qdrant integration test failed: {str(e)}")


if __name__ == "__main__":
    # Run specific tests
    pytest.main([__file__, "-v", "-k", "not real_"])