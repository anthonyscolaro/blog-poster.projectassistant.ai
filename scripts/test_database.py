#!/usr/bin/env python3
"""
Test script to verify database integration is working correctly
"""
import os
import sys
import asyncio
import logging
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_database_connection():
    """Test basic database connection"""
    logger.info("Testing database connection...")
    
    try:
        from src.database import get_db_session, init_database
        
        # Initialize database
        init_database()
        logger.info("✅ Database initialized")
        
        # Test connection
        with get_db_session() as db:
            from sqlalchemy import text
            result = db.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            
            # Check for pgvector
            result = db.execute(text("""
                SELECT installed_version 
                FROM pg_available_extensions 
                WHERE name = 'vector'
            """))
            vector_version = result.fetchone()
            if vector_version and vector_version[0]:
                logger.info(f"✅ pgvector installed: v{vector_version[0]}")
            else:
                logger.warning("⚠️ pgvector not installed")
                
        return True
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


async def test_api_keys_manager():
    """Test API keys manager with database backend"""
    logger.info("\nTesting API Keys Manager...")
    
    try:
        from src.services.api_keys_manager_db import get_api_keys_manager_db
        
        manager = get_api_keys_manager_db()
        
        # Test saving a key
        test_key = "test_key_12345"
        success = manager.set_key("test_service", test_key)
        if success:
            logger.info("✅ Saved test API key")
        else:
            logger.error("❌ Failed to save test API key")
            return False
        
        # Test retrieving the key
        retrieved = manager.get_key("test_service")
        if retrieved == test_key:
            logger.info("✅ Retrieved test API key correctly")
        else:
            logger.error("❌ Retrieved key doesn't match")
            return False
        
        # Test getting all keys (masked)
        all_keys = manager.get_all_keys(masked=True)
        logger.info(f"✅ Retrieved {len(all_keys)} masked keys")
        
        # Test stats
        stats = manager.get_key_stats()
        logger.info(f"✅ Got stats for {len(stats)} keys")
        
        # Clean up - deactivate test key
        manager.delete_key("test_service")
        logger.info("✅ Cleaned up test key")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API Keys Manager test failed: {e}")
        return False


async def test_orchestration_manager():
    """Test orchestration manager with database backend"""
    logger.info("\nTesting Orchestration Manager...")
    
    try:
        from src.services.orchestration_manager_db import OrchestrationManager
        from src.models.contracts import ArticleRequest
        
        manager = OrchestrationManager()
        
        # Create a test pipeline request
        request = ArticleRequest(
            topic="Test Article for Database Integration",
            keywords=["test", "database", "integration"],
            auto_publish=False  # Don't actually publish
        )
        
        logger.info("Running test pipeline...")
        result = await manager.run_pipeline(request)
        
        if result.status.value == "completed":
            logger.info(f"✅ Pipeline completed: {result.pipeline_id}")
        else:
            logger.error(f"❌ Pipeline failed: {result.status}")
            return False
        
        # Test getting pipeline history
        history = manager.get_pipeline_history(limit=5)
        logger.info(f"✅ Retrieved {len(history)} pipeline records")
        
        # Test getting stats
        stats = await manager.get_pipeline_stats()
        logger.info(f"✅ Got pipeline stats: {stats['total_pipelines']} total pipelines")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Orchestration Manager test failed: {e}")
        return False


async def test_repositories():
    """Test repository classes directly"""
    logger.info("\nTesting Repository Classes...")
    
    try:
        from src.database import get_db_session
        from src.database.repositories import (
            ArticleRepository,
            PipelineRepository,
            ApiKeyRepository
        )
        
        with get_db_session() as db:
            # Test Article Repository
            article_repo = ArticleRepository(db)
            article_data = {
                'title': 'Test Article',
                'slug': f'test-article-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
                'content_markdown': '# Test Article\n\nThis is a test.',
                'content_html': '<h1>Test Article</h1><p>This is a test.</p>',
                'word_count': 5,
                'status': 'draft'
            }
            article = article_repo.create(article_data)
            logger.info(f"✅ Created test article: {article.id}")
            
            # Test Pipeline Repository
            pipeline_repo = PipelineRepository(db)
            pipeline_data = {
                'pipeline_id': f'test_pipeline_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
                'status': 'completed',
                'started_at': datetime.utcnow(),
                'input_config': {'test': True}
            }
            pipeline = pipeline_repo.create(pipeline_data)
            logger.info(f"✅ Created test pipeline: {pipeline.id}")
            
            # Test API Key Repository
            api_key_repo = ApiKeyRepository(db)
            api_key_repo.upsert(
                service='test_service_2',
                encrypted_key='encrypted_test_key',
                key_preview='test****'
            )
            logger.info("✅ Created test API key")
            
            # Test queries
            recent_articles = article_repo.get_recent(limit=5)
            logger.info(f"✅ Queried {len(recent_articles)} recent articles")
            
            article_stats = article_repo.get_stats()
            logger.info(f"✅ Got article stats: {article_stats}")
            
            cost_stats = pipeline_repo.get_cost_stats(days=30)
            logger.info(f"✅ Got cost stats: ${cost_stats['total_cost']:.2f} total")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Repository test failed: {e}")
        return False


async def main():
    """Main test runner"""
    logger.info("="*60)
    logger.info("DATABASE INTEGRATION TEST SUITE")
    logger.info("="*60)
    
    # Check environment
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        logger.info(f"DATABASE_URL: {db_url.split('@')[1] if '@' in db_url else db_url}")
    else:
        logger.warning("No DATABASE_URL found - using default SQLite")
    
    # Run tests
    results = []
    
    # Test 1: Database Connection
    result = await test_database_connection()
    results.append(("Database Connection", result))
    
    if result:  # Only continue if database is connected
        # Test 2: API Keys Manager
        result = await test_api_keys_manager()
        results.append(("API Keys Manager", result))
        
        # Test 3: Repositories
        result = await test_repositories()
        results.append(("Repository Classes", result))
        
        # Test 4: Orchestration Manager (this creates actual data)
        result = await test_orchestration_manager()
        results.append(("Orchestration Manager", result))
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("TEST SUMMARY")
    logger.info("="*60)
    
    passed = 0
    failed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info("="*60)
    logger.info(f"Total: {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 All tests passed!")
        return 0
    else:
        logger.error(f"⚠️ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)