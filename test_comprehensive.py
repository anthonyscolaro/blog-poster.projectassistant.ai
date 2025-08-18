#!/usr/bin/env python3
"""Comprehensive deployment test"""

import requests
import json
from datetime import datetime

BASE_URL = "https://blog-poster-api-qps2l.ondigitalocean.app"

def test_endpoint(method, path, description, data=None, headers=None):
    """Test an endpoint and report results"""
    print(f"\n{'='*50}")
    print(f"Testing: {description}")
    print(f"Method: {method}")
    print(f"URL: {BASE_URL}{path}")
    if headers:
        print(f"Headers: {headers}")
    if data:
        print(f"Data: {json.dumps(data, indent=2)[:100]}...")
    print("-" * 50)
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{path}", json=data, headers=headers, timeout=10)
        else:
            response = requests.request(method, f"{BASE_URL}{path}", json=data, headers=headers, timeout=10)
            
        print(f"Status Code: {response.status_code}")
        
        if response.status_code < 400:
            print("✅ SUCCESS")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)[:300]}")
            except:
                # Check if it's HTML (like docs)
                if 'text/html' in response.headers.get('content-type', ''):
                    print(f"Response (HTML): Page loaded successfully")
                else:
                    print(f"Response (text): {response.text[:300]}")
        else:
            print(f"❌ FAILED")
            print(f"Response: {response.text[:300]}")
            
        return response.status_code < 400
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("COMPREHENSIVE BLOG-POSTER API TEST")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 50)
    
    results = []
    
    # Health checks
    results.append(("Health (root)", test_endpoint("GET", "/health", "Root Health Check")))
    results.append(("Health (API)", test_endpoint("GET", "/api/v1/health", "API Health Check")))
    
    # Documentation
    results.append(("Docs", test_endpoint("GET", "/docs", "API Documentation")))
    results.append(("OpenAPI", test_endpoint("GET", "/openapi.json", "OpenAPI Specification")))
    
    # Public endpoints (no auth required)
    results.append(("SEO Lint", test_endpoint("POST", "/api/v1/seo/lint", "SEO Lint Check", {
        "title": "Test Article",
        "content": "This is a test article with some content.",
        "meta_description": "Test description"
    })))
    
    # Auth endpoints
    results.append(("Auth Status", test_endpoint("GET", "/api/v1/auth/status", "Auth Status Check")))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    working = []
    failing = []
    
    for name, success in results:
        if success:
            working.append(name)
        else:
            failing.append(name)
    
    print(f"\n✅ Working Endpoints ({len(working)}):")
    for endpoint in working:
        print(f"  - {endpoint}")
    
    print(f"\n❌ Failing Endpoints ({len(failing)}):")
    for endpoint in failing:
        print(f"  - {endpoint}")
    
    print("\n" + "=" * 50)
    print("DEPLOYMENT STATUS")
    print("=" * 50)
    print(f"Success Rate: {len(working)}/{len(results)} ({len(working)*100/len(results):.1f}%)")
    
    if len(working) >= 3:
        print("✅ Deployment is SUCCESSFUL - Core functionality working")
    else:
        print("⚠️  Deployment has ISSUES - Limited functionality")

if __name__ == "__main__":
    main()