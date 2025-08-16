"""
Database initialization and connection management
Using Supabase-centric architecture with pgvector
"""
from .models import Base, Article, Pipeline, ApiKey, CompetitorArticle

# Use Supabase connection if available, fallback to standard connection
import os
if os.getenv('SUPABASE_URL') or 'supabase' in os.getenv('DATABASE_URL', '').lower():
    from .supabase_connection import (
        get_db, 
        engine, 
        init_database, 
        get_db_session, 
        test_connection,
        get_supabase_connection
    )
    SessionLocal = None  # Not used in Supabase mode
else:
    from .connection import (
        get_db, 
        engine, 
        SessionLocal, 
        init_database, 
        get_db_session, 
        test_connection
    )
    get_supabase_connection = None  # Not available in standard mode

__all__ = [
    'Base',
    'Article', 
    'Pipeline',
    'ApiKey',
    'CompetitorArticle',
    'get_db',
    'get_db_session',
    'engine',
    'SessionLocal',
    'init_database',
    'test_connection'
]