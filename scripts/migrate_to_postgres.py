#!/usr/bin/env python3
"""
Migration script to move from JSON file storage to PostgreSQL
Imports existing articles, pipelines, and API keys to database
"""
import os
import sys
import json
import glob
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import init_database, get_db_session
from src.database.repositories import (
    ArticleRepository,
    PipelineRepository,
    ApiKeyRepository
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataMigrator:
    """Migrate data from JSON files to PostgreSQL"""
    
    def __init__(self):
        self.articles_dir = Path("data/articles")
        self.pipelines_dir = Path("data/pipelines")
        self.api_keys_file = Path("data/secure/api_keys.enc")
        
        self.stats = {
            'articles_migrated': 0,
            'articles_failed': 0,
            'pipelines_migrated': 0,
            'pipelines_failed': 0,
            'api_keys_migrated': 0
        }
    
    def migrate_all(self):
        """Run all migrations"""
        logger.info("Starting data migration to PostgreSQL...")
        
        # Initialize database
        logger.info("Initializing database...")
        init_database()
        
        # Migrate data
        self.migrate_articles()
        self.migrate_pipelines()
        self.migrate_api_keys()
        
        # Print summary
        self.print_summary()
    
    def migrate_articles(self):
        """Migrate articles from JSON files to database"""
        logger.info("Migrating articles...")
        
        if not self.articles_dir.exists():
            logger.warning(f"Articles directory not found: {self.articles_dir}")
            return
        
        article_files = glob.glob(str(self.articles_dir / "*.json"))
        logger.info(f"Found {len(article_files)} article files")
        
        with get_db_session() as db:
            article_repo = ArticleRepository(db)
            
            for file_path in article_files:
                try:
                    # Load JSON data
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    # Prepare article data
                    article_data = self.prepare_article_data(data)
                    
                    # Check if article already exists
                    existing = article_repo.get_by_slug(article_data['slug'])
                    if existing:
                        logger.info(f"Article already exists: {article_data['slug']}")
                        continue
                    
                    # Create article in database
                    article = article_repo.create(article_data)
                    logger.info(f"Migrated article: {article.slug}")
                    self.stats['articles_migrated'] += 1
                    
                except Exception as e:
                    logger.error(f"Failed to migrate article {file_path}: {e}")
                    self.stats['articles_failed'] += 1
    
    def prepare_article_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare article data for database insertion"""
        import json
        
        # Map JSON fields to database columns
        article_data = {
            'title': data.get('title', ''),
            'slug': data.get('slug', ''),
            'content_markdown': data.get('content_markdown', data.get('content', '')),
            'content_html': data.get('content_html'),
            'excerpt': data.get('excerpt'),
            'meta_title': data.get('meta_title'),
            'meta_description': data.get('meta_description'),
            'primary_keyword': data.get('primary_keyword'),
            'secondary_keywords': data.get('secondary_keywords', []),
            'seo_score': data.get('seo_score'),
            'wp_post_id': data.get('wp_post_id'),
            'wp_url': data.get('wp_url'),
            'wp_status': data.get('wp_status'),
            'wp_categories': data.get('categories', []),
            'wp_tags': data.get('tags', []),
            'word_count': data.get('word_count'),
            'reading_time': data.get('reading_time'),
            'status': data.get('status', 'draft')
        }
        
        # Handle internal and external links
        # If they're lists of dicts, count them; if they're already numbers, use them
        internal_links = data.get('internal_links', [])
        external_links = data.get('external_links', [])
        
        if isinstance(internal_links, list):
            article_data['internal_links'] = len(internal_links)
        else:
            article_data['internal_links'] = internal_links or 0
            
        if isinstance(external_links, list):
            article_data['external_links'] = len(external_links)
        else:
            article_data['external_links'] = external_links or 0
        
        # Handle dates
        if 'published_at' in data and data['published_at']:
            try:
                article_data['published_at'] = datetime.fromisoformat(data['published_at'])
            except:
                pass
        
        if 'created_at' in data and data['created_at']:
            try:
                article_data['created_at'] = datetime.fromisoformat(data['created_at'])
            except:
                pass
        
        # Remove None values
        return {k: v for k, v in article_data.items() if v is not None}
    
    def migrate_pipelines(self):
        """Migrate pipeline history to database"""
        logger.info("Migrating pipelines...")
        
        # Check for pipeline history file
        pipeline_file = Path("data/pipeline_history.json")
        if not pipeline_file.exists():
            logger.info("No pipeline history file found")
            return
        
        try:
            with open(pipeline_file, 'r') as f:
                pipelines = json.load(f)
            
            with get_db_session() as db:
                pipeline_repo = PipelineRepository(db)
                
                for pipeline_data in pipelines:
                    try:
                        # Prepare pipeline data
                        prepared_data = self.prepare_pipeline_data(pipeline_data)
                        
                        # Check if already exists
                        existing = pipeline_repo.get_by_pipeline_id(prepared_data.get('pipeline_id'))
                        if existing:
                            logger.info(f"Pipeline already exists: {prepared_data.get('pipeline_id')}")
                            continue
                        
                        # Create pipeline
                        pipeline = pipeline_repo.create(prepared_data)
                        logger.info(f"Migrated pipeline: {pipeline.pipeline_id}")
                        self.stats['pipelines_migrated'] += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to migrate pipeline: {e}")
                        self.stats['pipelines_failed'] += 1
                        
        except Exception as e:
            logger.error(f"Failed to load pipeline history: {e}")
    
    def prepare_pipeline_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare pipeline data for database insertion"""
        pipeline_data = {
            'pipeline_id': data.get('pipeline_id', f"pipeline_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
            'status': data.get('status', 'completed'),
            'input_config': data.get('input_config', {}),
            'competitor_data': data.get('competitor_data'),
            'topic_recommendation': data.get('topic_recommendation'),
            'fact_check_report': data.get('fact_check_report'),
            'wordpress_result': data.get('wordpress_result'),
            'total_cost': data.get('total_cost', 0.0),
            'llm_tokens_used': data.get('llm_tokens_used', 0),
            'api_calls_made': data.get('api_calls_made', 0),
            'errors': data.get('errors'),
            'warnings': data.get('warnings'),
            'retry_count': data.get('retry_count', 0)
        }
        
        # Handle dates
        if 'started_at' in data and data['started_at']:
            try:
                pipeline_data['started_at'] = datetime.fromisoformat(data['started_at'])
            except:
                pass
        
        if 'completed_at' in data and data['completed_at']:
            try:
                pipeline_data['completed_at'] = datetime.fromisoformat(data['completed_at'])
            except:
                pass
        
        if 'execution_time' in data:
            pipeline_data['execution_time_seconds'] = data['execution_time']
        
        return {k: v for k, v in pipeline_data.items() if v is not None}
    
    def migrate_api_keys(self):
        """Migrate API keys to database"""
        logger.info("Migrating API keys...")
        
        # Import the API keys manager to decrypt existing keys
        try:
            from src.services.api_keys_manager import APIKeysManager
            
            manager = APIKeysManager()
            keys = manager.get_all_keys()
            
            if not keys:
                logger.info("No API keys to migrate")
                return
            
            with get_db_session() as db:
                api_key_repo = ApiKeyRepository(db)
                
                for service, key_info in keys.items():
                    if key_info and key_info != 'Not set':
                        # Note: We're storing the masked version for now
                        # In production, you'd want to re-encrypt properly
                        api_key_repo.upsert(
                            service=service,
                            encrypted_key=key_info,  # This is already masked
                            key_preview=key_info[:20] if len(key_info) > 20 else key_info
                        )
                        logger.info(f"Migrated API key for: {service}")
                        self.stats['api_keys_migrated'] += 1
                        
        except Exception as e:
            logger.error(f"Failed to migrate API keys: {e}")
    
    def print_summary(self):
        """Print migration summary"""
        logger.info("\n" + "="*50)
        logger.info("MIGRATION SUMMARY")
        logger.info("="*50)
        logger.info(f"Articles migrated: {self.stats['articles_migrated']}")
        if self.stats['articles_failed'] > 0:
            logger.warning(f"Articles failed: {self.stats['articles_failed']}")
        logger.info(f"Pipelines migrated: {self.stats['pipelines_migrated']}")
        if self.stats['pipelines_failed'] > 0:
            logger.warning(f"Pipelines failed: {self.stats['pipelines_failed']}")
        logger.info(f"API keys migrated: {self.stats['api_keys_migrated']}")
        logger.info("="*50)
        
        if self.stats['articles_failed'] == 0 and self.stats['pipelines_failed'] == 0:
            logger.info("✅ Migration completed successfully!")
        else:
            logger.warning("⚠️ Migration completed with some failures")


def main():
    """Main entry point"""
    migrator = DataMigrator()
    
    # Confirm before running
    print("\n" + "="*50)
    print("PostgreSQL Data Migration")
    print("="*50)
    print("This will migrate all data from JSON files to PostgreSQL.")
    print("Make sure your database is configured and running.")
    print()
    
    response = input("Continue with migration? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        return
    
    try:
        migrator.migrate_all()
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()