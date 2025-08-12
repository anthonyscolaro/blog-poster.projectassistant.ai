#!/usr/bin/env python3
"""
Database initialization script for production deployment
Creates tables, indexes, and runs initial setup
"""
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import init_database, engine
from src.database.models import Base
from sqlalchemy import text

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_extensions():
    """Create PostgreSQL extensions"""
    logger.info("Creating PostgreSQL extensions...")
    
    try:
        with engine.connect() as conn:
            # Create pgvector extension for embeddings
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            logger.info("✅ Created vector extension")
            
            # Create UUID extension
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            conn.commit()
            logger.info("✅ Created uuid-ossp extension")
            
    except Exception as e:
        logger.error(f"Failed to create extensions: {e}")
        # Continue anyway - extensions might already exist


def create_indexes():
    """Create additional database indexes for performance"""
    logger.info("Creating database indexes...")
    
    index_statements = [
        # Articles indexes
        "CREATE INDEX IF NOT EXISTS idx_articles_slug ON articles(slug)",
        "CREATE INDEX IF NOT EXISTS idx_articles_status ON articles(status)",
        "CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at DESC)",
        "CREATE INDEX IF NOT EXISTS idx_articles_pipeline_id ON articles(pipeline_id)",
        "CREATE INDEX IF NOT EXISTS idx_articles_wp_post_id ON articles(wp_post_id)",
        
        # Pipelines indexes
        "CREATE INDEX IF NOT EXISTS idx_pipelines_pipeline_id ON pipelines(pipeline_id)",
        "CREATE INDEX IF NOT EXISTS idx_pipelines_status ON pipelines(status)",
        "CREATE INDEX IF NOT EXISTS idx_pipelines_started_at ON pipelines(started_at DESC)",
        
        # API Keys indexes
        "CREATE INDEX IF NOT EXISTS idx_api_keys_service ON api_keys(service)",
        "CREATE INDEX IF NOT EXISTS idx_api_keys_active ON api_keys(is_active)",
        
        # Competitor Articles indexes
        "CREATE INDEX IF NOT EXISTS idx_competitor_articles_source ON competitor_articles(source)",
        "CREATE INDEX IF NOT EXISTS idx_competitor_articles_scraped_at ON competitor_articles(scraped_at DESC)",
    ]
    
    try:
        with engine.connect() as conn:
            for statement in index_statements:
                conn.execute(text(statement))
                conn.commit()
                logger.info(f"✅ Created index: {statement.split('idx_')[1].split(' ')[0]}")
                
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")


def verify_database():
    """Verify database is properly initialized"""
    logger.info("Verifying database setup...")
    
    try:
        with engine.connect() as conn:
            # Check tables exist
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            logger.info(f"Found {len(tables)} tables: {', '.join(tables)}")
            
            expected_tables = ['articles', 'pipelines', 'api_keys', 'competitor_articles']
            missing_tables = set(expected_tables) - set(tables)
            
            if missing_tables:
                logger.warning(f"⚠️ Missing tables: {', '.join(missing_tables)}")
                return False
            
            # Check pgvector extension
            result = conn.execute(text("""
                SELECT installed_version 
                FROM pg_available_extensions 
                WHERE name = 'vector'
            """))
            
            vector_version = result.fetchone()
            if vector_version and vector_version[0]:
                logger.info(f"✅ pgvector version: {vector_version[0]}")
            else:
                logger.warning("⚠️ pgvector extension not installed")
            
            return True
            
    except Exception as e:
        logger.error(f"Database verification failed: {e}")
        return False


def create_default_data():
    """Create any default data needed for the application"""
    logger.info("Creating default data...")
    
    # No default data needed for now
    # This is where you'd add default categories, tags, etc. if needed
    
    logger.info("✅ Default data setup complete")


def main():
    """Main initialization function"""
    logger.info("="*50)
    logger.info("DATABASE INITIALIZATION")
    logger.info("="*50)
    
    try:
        # Create extensions first (before tables)
        create_extensions()
        
        # Initialize database (create tables)
        logger.info("Creating database tables...")
        init_database()
        logger.info("✅ Database tables created")
        
        # Create indexes
        create_indexes()
        
        # Create default data
        create_default_data()
        
        # Verify setup
        if verify_database():
            logger.info("="*50)
            logger.info("✅ DATABASE INITIALIZATION COMPLETE")
            logger.info("="*50)
            return 0
        else:
            logger.error("Database verification failed")
            return 1
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.exception(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())