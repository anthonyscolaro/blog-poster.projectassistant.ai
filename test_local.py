#!/usr/bin/env python3
"""Test local app imports and database connection"""

import os
import sys

# Set production environment
os.environ['ENVIRONMENT'] = 'production'
os.environ['DATABASE_URL'] = 'postgresql://postgres.epftkydwdqerdlhvqili:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwZnRreWR3ZHFlcmRsaHZxaWxpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTI4NDU0MCwiZXhwIjoyMDcwODYwNTQwfQ.vM4-DdBqqQh9KfsHmuxKlXyNHMVyZ60qZ6kmXHW7k9o@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres'
os.environ['SUPABASE_URL'] = 'https://epftkydwdqerdlhvqili.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVwZnRreWR3ZHFlcmRsaHZxaWxpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyODQ1NDAsImV4cCI6MjA3MDg2MDU0MH0.Mn9Re4itgw0w7Qi2RyD4V0vmGx8tLtJPNdbNtpP0-Ng'

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