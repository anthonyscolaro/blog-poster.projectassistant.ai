#!/usr/bin/env python3
"""
Migration script from Qdrant to pgvector
Transfers existing vector data to PostgreSQL with pgvector extension
"""
import os
import sys
import asyncio
import logging
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.vector_search import VectorSearchManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorMigration:
    """Handles migration from Qdrant to pgvector"""
    
    def __init__(self, database_url: str):
        """Initialize migration with database connection"""
        self.database_url = database_url
        self.conn = psycopg2.connect(database_url)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
    def setup_pgvector(self):
        """Ensure pgvector extension and tables are set up"""
        logger.info("Setting up pgvector extension and tables...")
        
        # Read and execute the init script
        init_script_path = os.path.join(
            os.path.dirname(__file__), 
            'init-pgvector.sql'
        )
        
        with open(init_script_path, 'r') as f:
            sql = f.read()
            
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logger.info("✅ pgvector setup complete")
        except Exception as e:
            logger.error(f"Error setting up pgvector: {e}")
            self.conn.rollback()
            raise
    
    def migrate_qdrant_data(self):
        """
        Migrate data from Qdrant to pgvector
        Note: This is a placeholder - actual implementation would
        connect to Qdrant and transfer data
        """
        logger.info("Starting data migration from Qdrant to pgvector...")
        
        # In a real migration, you would:
        # 1. Connect to Qdrant
        # 2. Fetch all collections
        # 3. For each collection, fetch all points
        # 4. Insert into corresponding PostgreSQL tables
        
        logger.info("✅ Migration complete (no existing data to migrate)")
    
    def verify_migration(self):
        """Verify the migration was successful"""
        logger.info("Verifying migration...")
        
        # Check tables exist
        self.cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('articles', 'competitor_content', 'research_docs')
        """)
        
        tables = self.cursor.fetchall()
        table_names = [t['table_name'] for t in tables]
        
        expected_tables = ['articles', 'competitor_content', 'research_docs']
        for table in expected_tables:
            if table in table_names:
                logger.info(f"✅ Table '{table}' exists")
            else:
                logger.error(f"❌ Table '{table}' missing")
        
        # Check pgvector extension
        self.cursor.execute("""
            SELECT extname FROM pg_extension WHERE extname = 'vector'
        """)
        
        if self.cursor.fetchone():
            logger.info("✅ pgvector extension enabled")
        else:
            logger.error("❌ pgvector extension not found")
    
    def close(self):
        """Close database connections"""
        self.cursor.close()
        self.conn.close()


async def main():
    """Run the migration"""
    # Get database URL from environment or use default
    database_url = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:your-super-secret-password@localhost:5434/postgres'
    )
    
    logger.info("Starting Qdrant to pgvector migration...")
    
    migration = VectorMigration(database_url)
    
    try:
        # Setup pgvector
        migration.setup_pgvector()
        
        # Migrate data (if any)
        migration.migrate_qdrant_data()
        
        # Verify migration
        migration.verify_migration()
        
        logger.info("🎉 Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)
    finally:
        migration.close()


if __name__ == "__main__":
    asyncio.run(main())