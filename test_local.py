#!/usr/bin/env python3
"""Test local app imports and database connection"""

import os
import sys

# Set production environment
os.environ['ENVIRONMENT'] = 'production'
# Try local database that's actually running
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
os.environ['SUPABASE_URL'] = 'https://pynlhikthsmduttvihuw.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5bmxoaWt0aHNtZHV0dHZpaHV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUzODIwMTYsImV4cCI6MjA3MDk1ODAxNn0.BDGAvf1jeX9iiQF7RaouCyzds6NS58guKB4l39AX_uQ'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5bmxoaWt0aHNtZHV0dHZpaHV3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTM4MjAxNiwiZXhwIjoyMDcwOTU4MDE2fQ._hyfVCT8sAMVKPZkqjxu3RMW7fX2BEofW05H9G1tSrM'

print("Testing database connection...")
try:
    from src.database.connection import test_connection, engine
    
    result = test_connection()
    print(f"Database connection test: {'SUCCESS' if result else 'FAILED'}")
    
    # Try to get connection string info
    print(f"Database URL parsed: {engine.url}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting health router...")
try:
    from src.routers.health import router
    print("Health router imported successfully")
    
    # Check if it has the expected endpoints
    for route in router.routes:
        print(f"  - {route.path}: {route.endpoint.__name__ if hasattr(route, 'endpoint') else 'N/A'}")
        
except Exception as e:
    print(f"Error importing health router: {e}")