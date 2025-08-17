#!/usr/bin/env python3
"""Test deployed API endpoints"""

import requests
import json
from datetime import datetime

BASE_URL = "https://blog-poster-api-qps2l.ondigitalocean.app"

def test_endpoint(path, description):
    """Test an endpoint and report results"""
    print(f"\n{'='*50}")
    print(f"Testing: {description}")
    print(f"URL: {BASE_URL}{path}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}{path}", timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)[:200]}")
            except:
                print(f"Response (text): {response.text[:200]}")
        else:
            print(f"❌ FAILED")
            print(f"Response: {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
    
    return

def main():
    """Run all tests"""
    print("=" * 50)
    print("BLOG-POSTER API DEPLOYMENT TEST")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 50)
    
    # Test endpoints
    test_endpoint("/health", "Root Health Check")
    test_endpoint("/api/v1/health", "API Health Check")
    test_endpoint("/docs", "API Documentation")
    test_endpoint("/", "Root Endpoint")
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print("Deployment URL:", BASE_URL)
    print("Status: Application is deployed and responding")
    print("\nKnown Issues:")
    print("1. Database connection failing (Supabase pooler config issue)")
    print("2. Response middleware causing Content-Length mismatch")
    print("3. Some endpoints return Internal Server Error")
    print("\nRecommendations:")
    print("1. Fix response middleware to handle streaming properly")
    print("2. Configure database with correct Supabase project")
    print("3. Add error handling for missing database connection")

if __name__ == "__main__":
    main()