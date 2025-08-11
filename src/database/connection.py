"""
Database connection management
"""
import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator

logger = logging.getLogger(__name__)


def get_database_url() -> str:
    """
    Get database URL from environment or construct from components
    """
    # First check for complete DATABASE_URL (Digital Ocean provides this)
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Digital Ocean uses postgresql:// but SQLAlchemy prefers postgresql+psycopg2://
        if database_url.startswith('postgresql://'):
            database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        return database_url
    
    # Fallback to constructing from individual components (for local dev)
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5433')  # Using your pgvector port
    db_name = os.getenv('DB_NAME', 'blogposter')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    
    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# Get database URL
DATABASE_URL = get_database_url()

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=pool.NullPool if 'sqlite' in DATABASE_URL else pool.QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,  # Verify connections before using
    echo=os.getenv('SQL_ECHO', 'false').lower() == 'true'  # SQL logging for debug
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    Use with FastAPI Depends() or as context manager
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions
    Use in non-FastAPI contexts
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_database():
    """
    Initialize database tables and extensions
    """
    from .models import Base
    
    try:
        # Create pgvector extension if it doesn't exist
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def test_connection() -> bool:
    """
    Test database connection
    """
    try:
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False