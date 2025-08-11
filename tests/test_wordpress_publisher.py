"""
Test suite for WordPress Publisher
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.wordpress_publisher import WordPressPublisher


class TestWordPressPublisher:
    """Test cases for WordPress Publisher"""
    
    @pytest.fixture
    def publisher(self):
        """Create a WordPress publisher instance"""
        with patch.dict(os.environ, {
            'WORDPRESS_URL': 'https://test.wordpress.com',
            'WP_USERNAME': 'testuser',
            'WP_APP_PASSWORD': 'test pass word',
            'WP_VERIFY_SSL': 'false'
        }):
            return WordPressPublisher()
    
    def test_initialization_from_env(self):
        """Test publisher initialization from environment variables"""
        with patch.dict(os.environ, {
            'WORDPRESS_URL': 'https://example.com',
            'WP_USERNAME': 'admin',
            'WP_APP_PASSWORD': 'app password here'
        }):
            publisher = WordPressPublisher()
            
            assert publisher.wordpress_url == 'https://example.com'
            assert publisher.username == 'admin'
            assert publisher.app_password == 'app password here'
            assert publisher.auth_method == 'app_password'
    
    def test_initialization_with_params(self):
        """Test publisher initialization with explicit parameters"""
        publisher = WordPressPublisher(
            wordpress_url='https://custom.site.com',
            username='customuser',
            app_password='custom_password'
        )
        
        assert publisher.wordpress_url == 'https://custom.site.com'
        assert publisher.username == 'customuser'
        assert publisher.app_password == 'custom_password'
    
    def test_local_detection(self):
        """Test detection of local WordPress instances"""
        local_urls = [
            'http://localhost',
            'http://localhost:8080',
            'http://127.0.0.1',
            'http://test.local',
            'http://wordpress.test'
        ]
        
        for url in local_urls:
            publisher = WordPressPublisher(
                wordpress_url=url,
                username='test',
                app_password='test'
            )
            assert publisher.is_local == True
        
        # Test non-local URL
        publisher = WordPressPublisher(
            wordpress_url='https://example.com',
            username='test',
            app_password='test'
        )
        assert publisher.is_local == False
    
    def test_auth_header_generation(self, publisher):
        """Test authentication header generation"""
        headers = publisher._get_headers()
        
        assert 'Authorization' in headers
        assert headers['Authorization'].startswith('Basic ')
        assert 'Content-Type' in headers
        assert headers['Content-Type'] == 'application/json'
    
    @pytest.mark.asyncio
    async def test_test_connection_success(self, publisher):
        """Test successful connection test"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'Test Site',
            'description': 'Test Description'
        }
        
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            result = await publisher.test_connection()
            
            assert result == True
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_test_connection_failure(self, publisher):
        """Test failed connection test"""
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.side_effect = Exception("Connection failed")
            
            result = await publisher.test_connection()
            
            assert result == False
    
    @pytest.mark.asyncio
    async def test_create_post_success(self, publisher):
        """Test successful post creation"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'id': 123,
            'link': 'https://test.wordpress.com/test-post/',
            'status': 'draft',
            'title': {'rendered': 'Test Post'}
        }
        
        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            result = await publisher.create_post(
                title="Test Post",
                content="<p>Test content</p>",
                status="draft",
                slug="test-post"
            )
            
            assert result['success'] == True
            assert result['post_id'] == 123
            assert result['post_url'] == 'https://test.wordpress.com/test-post/'
            assert 'edit_link' in result
    
    @pytest.mark.asyncio
    async def test_create_post_with_categories_and_tags(self, publisher):
        """Test post creation with categories and tags"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'id': 456,
            'link': 'https://test.wordpress.com/categorized-post/',
            'categories': [1, 2],
            'tags': [3, 4]
        }
        
        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            result = await publisher.create_post(
                title="Categorized Post",
                content="Content with categories",
                categories=[1, 2],
                tags=[3, 4]
            )
            
            assert result['success'] == True
            
            # Check the call was made with correct data
            call_args = mock_post.call_args
            posted_data = json.loads(call_args.kwargs['data'])
            assert posted_data['categories'] == [1, 2]
            assert posted_data['tags'] == [3, 4]
    
    @pytest.mark.asyncio
    async def test_create_post_failure(self, publisher):
        """Test failed post creation"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request: Invalid content"
        
        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            result = await publisher.create_post(
                title="Failed Post",
                content="Invalid content"
            )
            
            assert result['success'] == False
            assert 'error' in result
            assert "400" in result['error']
    
    @pytest.mark.asyncio
    async def test_get_categories(self, publisher):
        """Test fetching categories"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'name': 'Category 1', 'slug': 'category-1'},
            {'id': 2, 'name': 'Category 2', 'slug': 'category-2'}
        ]
        
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            categories = await publisher.get_categories()
            
            assert len(categories) == 2
            assert categories[0]['name'] == 'Category 1'
            assert categories[1]['id'] == 2
    
    @pytest.mark.asyncio
    async def test_get_tags(self, publisher):
        """Test fetching tags"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 10, 'name': 'Tag 1', 'slug': 'tag-1'},
            {'id': 20, 'name': 'Tag 2', 'slug': 'tag-2'}
        ]
        
        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            
            tags = await publisher.get_tags()
            
            assert len(tags) == 2
            assert tags[0]['name'] == 'Tag 1'
            assert tags[1]['id'] == 20
    
    @pytest.mark.asyncio
    async def test_update_post(self, publisher):
        """Test updating an existing post"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 789,
            'title': {'rendered': 'Updated Title'},
            'modified': '2024-01-01T12:00:00'
        }
        
        with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            result = await publisher.update_post(
                post_id=789,
                title="Updated Title",
                content="Updated content"
            )
            
            assert result['success'] == True
            assert result['post_id'] == 789
    
    @pytest.mark.asyncio
    async def test_delete_post(self, publisher):
        """Test deleting a post"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'deleted': True,
            'previous': {'id': 999}
        }
        
        with patch('httpx.AsyncClient.delete', new_callable=AsyncMock) as mock_delete:
            mock_delete.return_value = mock_response
            
            result = await publisher.delete_post(post_id=999)
            
            assert result['success'] == True
            assert result['deleted'] == True


class TestWordPressIntegration:
    """Integration tests (require actual WordPress instance)"""
    
    @pytest.mark.skipif(
        not os.getenv('WP_TEST_URL'),
        reason="WordPress test URL not configured"
    )
    @pytest.mark.asyncio
    async def test_real_wordpress_connection(self):
        """Test connection to real WordPress instance"""
        publisher = WordPressPublisher()
        
        connected = await publisher.test_connection()
        assert connected == True
        
        # Try to get categories
        categories = await publisher.get_categories()
        assert isinstance(categories, list)
    
    @pytest.mark.skipif(
        not os.getenv('WP_TEST_URL'),
        reason="WordPress test URL not configured"
    )
    @pytest.mark.asyncio
    async def test_real_post_creation_and_deletion(self):
        """Test creating and deleting a real post"""
        publisher = WordPressPublisher()
        
        # Create a test post
        result = await publisher.create_post(
            title="Test Post - Delete Me",
            content="<p>This is a test post that should be deleted.</p>",
            status="draft",
            slug="test-post-delete-me"
        )
        
        assert result['success'] == True
        post_id = result['post_id']
        
        # Delete the test post
        delete_result = await publisher.delete_post(post_id)
        assert delete_result['success'] == True


if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, '-v', '-k', 'not real_'])