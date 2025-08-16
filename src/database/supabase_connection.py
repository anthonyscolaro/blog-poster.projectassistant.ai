"""
Supabase-centric database connection management
Provides seamless integration with Supabase PostgreSQL + pgvector
"""
import os
import logging
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any
from urllib.parse import urlparse, parse_qs

from sqlalchemy import create_engine, pool, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class SupabaseConnection:
    """
    Manages Supabase database connections with pgvector support
    """
    
    def __init__(self):
        self.database_url = self._get_supabase_url()
        self.engine = self._create_engine()
        self.SessionLocal = self._create_session_factory()
        
    def _get_supabase_url(self) -> str:
        """
        Get Supabase database URL from environment
        Handles both direct DATABASE_URL and Supabase-specific configs
        """
        # Check for direct DATABASE_URL (Supabase provides this)
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Supabase uses postgresql:// - ensure compatibility
            if database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
            
            # Parse and validate Supabase connection
            parsed = urlparse(database_url)
            if 'supabase.co' in parsed.hostname or 'supabase.com' in parsed.hostname:
                logger.info(f"Using Supabase database: {parsed.hostname}")
                
                # Add connection parameters for production
                if '?' not in database_url:
                    database_url += '?'
                else:
                    database_url += '&'
                    
                # Add production parameters
                params = [
                    'sslmode=require',
                    'connect_timeout=10',
                    'application_name=blog-poster'
                ]
                database_url += '&'.join(params)
                
            return database_url
        
        # Fallback: Construct from Supabase project details
        supabase_url = os.getenv('SUPABASE_URL')
        if supabase_url:
            # Extract project ID from URL
            # Format: https://[project-id].supabase.co
            project_id = supabase_url.split('//')[1].split('.')[0]
            
            # Construct database URL
            db_password = os.getenv('SUPABASE_DB_PASSWORD', os.getenv('DB_PASSWORD'))
            if not db_password:
                raise ValueError("SUPABASE_DB_PASSWORD or DATABASE_URL required for Supabase connection")
            
            database_url = (
                f"postgresql+psycopg2://postgres:{db_password}@"
                f"db.{project_id}.supabase.co:5432/postgres"
                f"?sslmode=require&connect_timeout=10"
            )
            
            logger.info(f"Constructed Supabase URL for project: {project_id}")
            return database_url
        
        # Last fallback: Local development
        logger.warning("No Supabase configuration found, using local PostgreSQL")
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'blog_poster')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        
        return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    def _create_engine(self):
        """
        Create SQLAlchemy engine optimized for Supabase
        """
        # Determine if we're using Supabase
        is_supabase = 'supabase.co' in self.database_url or 'supabase.com' in self.database_url
        
        engine_config = {
            'pool_size': 10 if is_supabase else 20,
            'max_overflow': 20 if is_supabase else 40,
            'pool_timeout': 30,
            'pool_recycle': 300,  # Recycle connections every 5 minutes
            'pool_pre_ping': True,  # Verify connections before using
            'echo': os.getenv('SQL_ECHO', 'false').lower() == 'true',
            'connect_args': {}
        }
        
        # Add Supabase-specific connection args
        if is_supabase:
            engine_config['connect_args'] = {
                'keepalives': 1,
                'keepalives_idle': 30,
                'keepalives_interval': 10,
                'keepalives_count': 5,
                'connect_timeout': 10,
                'options': '-c statement_timeout=30000'  # 30 second statement timeout
            }
        
        return create_engine(self.database_url, **engine_config)
    
    def _create_session_factory(self):
        """
        Create session factory for database operations
        """
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False  # Prevent lazy loading issues
        )
    
    def init_database(self):
        """
        Initialize Supabase database with required extensions and tables
        """
        try:
            with self.engine.connect() as conn:
                # Enable required extensions
                extensions = [
                    "vector",      # pgvector for embeddings
                    "pg_stat_statements",  # Query performance monitoring
                    "uuid-ossp",   # UUID generation
                    "pg_trgm"      # Trigram similarity search
                ]
                
                for ext in extensions:
                    try:
                        conn.execute(text(f"CREATE EXTENSION IF NOT EXISTS \"{ext}\""))
                        logger.info(f"Extension {ext} enabled")
                    except Exception as e:
                        logger.warning(f"Could not create extension {ext}: {e}")
                
                conn.commit()
                
            # Create tables
            from .models import Base
            Base.metadata.create_all(bind=self.engine)
            logger.info("Supabase database initialized successfully")
            
            # Verify pgvector is working
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version()"))
                version = result.scalar()
                logger.info(f"PostgreSQL version: {version}")
                
                # Check pgvector
                result = conn.execute(text(
                    "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
                ))
                vector_version = result.scalar()
                if vector_version:
                    logger.info(f"pgvector version: {vector_version}")
                else:
                    logger.warning("pgvector extension not found - vector search will not work")
                    
        except Exception as e:
            logger.error(f"Failed to initialize Supabase database: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test Supabase database connection
        """
        try:
            with self.engine.connect() as conn:
                # Test basic connectivity
                result = conn.execute(text("SELECT 1"))
                if result.scalar() != 1:
                    return False
                
                # Test Supabase-specific features
                result = conn.execute(text(
                    "SELECT current_database(), current_user, version()"
                ))
                db_info = result.fetchone()
                logger.info(f"Connected to: {db_info[0]} as {db_info[1]}")
                
                # Test pgvector
                result = conn.execute(text(
                    "SELECT '[1,2,3]'::vector"
                ))
                logger.info("pgvector test successful")
                
                return True
                
        except Exception as e:
            logger.error(f"Supabase connection test failed: {e}")
            return False
    
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session for use with FastAPI Depends()
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a raw SQL query
        """
        with self.session_scope() as session:
            result = session.execute(text(query), params or {})
            return result.fetchall()
    
    def health_check(self) -> Dict[str, Any]:
        """
        Comprehensive health check for Supabase connection
        """
        health = {
            'status': 'unknown',
            'database': None,
            'pgvector': False,
            'connection_pool': {},
            'errors': []
        }
        
        try:
            # Test connection
            with self.engine.connect() as conn:
                # Get database info
                result = conn.execute(text(
                    "SELECT current_database(), version(), pg_size_pretty(pg_database_size(current_database()))"
                ))
                db_info = result.fetchone()
                health['database'] = {
                    'name': db_info[0],
                    'version': db_info[1].split(' ')[1],
                    'size': db_info[2]
                }
                
                # Check pgvector
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM pg_extension WHERE extname = 'vector'"
                ))
                health['pgvector'] = result.scalar() > 0
                
                # Get connection pool stats
                pool = self.engine.pool
                health['connection_pool'] = {
                    'size': pool.size(),
                    'checked_in': pool.checkedin(),
                    'overflow': pool.overflow(),
                    'total': pool.size() + pool.overflow()
                }
                
                health['status'] = 'healthy'
                
        except Exception as e:
            health['status'] = 'unhealthy'
            health['errors'].append(str(e))
            
        return health


# Global instance
_supabase_connection: Optional[SupabaseConnection] = None


def get_supabase_connection() -> SupabaseConnection:
    """
    Get or create global Supabase connection instance
    """
    global _supabase_connection
    if _supabase_connection is None:
        _supabase_connection = SupabaseConnection()
    return _supabase_connection


# Convenience exports for backward compatibility
def get_db() -> Generator[Session, None, None]:
    """FastAPI Depends() compatible session getter"""
    return get_supabase_connection().get_session()


def get_db_session():
    """Context manager for database sessions"""
    return get_supabase_connection().session_scope()


def init_database():
    """Initialize Supabase database"""
    return get_supabase_connection().init_database()


def test_connection() -> bool:
    """Test database connection"""
    return get_supabase_connection().test_connection()


# Export engine for migrations and backward compatibility
def get_engine():
    """Get the database engine"""
    return get_supabase_connection().engine

engine = get_engine()