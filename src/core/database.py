"""
Enhanced database management with retry logic, connection pooling, and monitoring
"""
import os
import time
import logging
from typing import Optional, Generator, Any, Dict
from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine, event, pool, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError, DisconnectionError
from sqlalchemy.pool import QueuePool, NullPool
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Enhanced database manager with connection pooling, retry logic, and monitoring
    """
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._init_engine()
        self._setup_listeners()
        self._metrics = {
            "connections_created": 0,
            "connections_recycled": 0,
            "connection_errors": 0,
            "queries_executed": 0,
            "query_errors": 0,
            "slow_queries": 0
        }
    
    def _init_engine(self):
        """Initialize database engine with proper pooling"""
        pool_class = NullPool if settings.is_testing else QueuePool
        
        self.engine = create_engine(
            settings.database_url,
            poolclass=pool_class,
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,  # Recycle connections after 1 hour
            echo=settings.db_echo_sql,
            connect_args={
                "connect_timeout": 10,
                "application_name": f"{settings.app_name}_{settings.environment}",
                "options": "-c statement_timeout=30000"  # 30 second statement timeout
            } if "postgresql" in settings.database_url else {}
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False  # Don't expire objects after commit
        )
    
    def _setup_listeners(self):
        """Setup SQLAlchemy event listeners for monitoring"""
        
        @event.listens_for(self.engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            """Track new connections"""
            self._metrics["connections_created"] += 1
            connection_record.info['connect_time'] = time.time()
        
        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            """Track connection checkouts"""
            # Check if connection is stale (older than 1 hour)
            connect_time = connection_record.info.get('connect_time', 0)
            if time.time() - connect_time > 3600:
                self._metrics["connections_recycled"] += 1
        
        @event.listens_for(self.engine, "before_execute")
        def receive_before_execute(conn, clauseelement, multiparams, params, execution_options):
            """Track query execution"""
            conn.info['query_start_time'] = time.time()
            self._metrics["queries_executed"] += 1
        
        @event.listens_for(self.engine, "after_execute")
        def receive_after_execute(conn, clauseelement, multiparams, params, execution_options, result):
            """Track slow queries"""
            start_time = conn.info.get('query_start_time', time.time())
            execution_time = time.time() - start_time
            
            # Log slow queries (>1 second)
            if execution_time > 1.0:
                self._metrics["slow_queries"] += 1
                logger.warning(f"Slow query detected ({execution_time:.2f}s): {str(clauseelement)[:100]}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((OperationalError, DisconnectionError))
    )
    def test_connection(self) -> bool:
        """Test database connection with retry logic"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return result.scalar() == 1
        except Exception as e:
            self._metrics["connection_errors"] += 1
            logger.error(f"Database connection test failed: {e}")
            raise
    
    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        """
        Get database session with automatic retry and error handling
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except OperationalError as e:
            self._metrics["query_errors"] += 1
            session.rollback()
            logger.error(f"Database operational error: {e}")
            # Retry logic could be added here
            raise
        except SQLAlchemyError as e:
            self._metrics["query_errors"] += 1
            session.rollback()
            logger.error(f"Database error: {e}")
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"Unexpected error: {e}")
            raise
        finally:
            session.close()
    
    def get_db(self) -> Generator[Session, None, None]:
        """FastAPI dependency for database sessions"""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    def init_database(self):
        """Initialize database with extensions and tables"""
        from src.database.models import Base
        
        try:
            # Create pgvector extension if using PostgreSQL
            if "postgresql" in settings.database_url:
                with self.engine.connect() as conn:
                    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                    conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_stat_statements"))
                    conn.commit()
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get database metrics"""
        pool_status = {}
        if hasattr(self.engine.pool, 'size'):
            pool_status = {
                "pool_size": self.engine.pool.size(),
                "pool_checked_out": self.engine.pool.checkedout(),
                "pool_overflow": self.engine.pool.overflow(),
                "pool_total": self.engine.pool.checkedout() + self.engine.pool.checkedin()
            }
        
        return {
            **self._metrics,
            **pool_status,
            "database_url": settings.database_url.split('@')[1] if '@' in settings.database_url else 'local'
        }
    
    def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get or create database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


# Convenience exports
def get_db_session():
    """Get database session context manager"""
    return get_db_manager().get_db_session()


def get_db():
    """FastAPI dependency for database sessions"""
    return get_db_manager().get_db()