#!/usr/bin/env python3
"""
Comprehensive test runner for blog-poster project

This script runs all test categories and provides detailed reporting.
"""
import sys
import subprocess
import time
import os
from pathlib import Path


def run_command(cmd, description, timeout=300):
    """Run a command with timeout and error handling"""
    print(f"\n🔄 {description}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        start_time = time.time()
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=Path(__file__).parent
        )
        end_time = time.time()
        
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} passed ({duration:.1f}s)")
            if result.stdout.strip():
                print(f"Output:\n{result.stdout}")
            return True, result.stdout
        else:
            print(f"❌ {description} failed ({duration:.1f}s)")
            print(f"Error:\n{result.stderr}")
            if result.stdout.strip():
                print(f"Output:\n{result.stdout}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out after {timeout}s")
        return False, "Timeout"
    except Exception as e:
        print(f"💥 {description} error: {e}")
        return False, str(e)


def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        "pytest",
        "pytest-asyncio", 
        "pytest-cov",
        "pytest-mock",
        "fastapi",
        "httpx"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True


def run_unit_tests():
    """Run unit tests"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "-k", "not (docker or integration or real_)",
        "--durations=10"
    ]
    
    return run_command(cmd, "Unit Tests")


def run_integration_tests():
    """Run integration tests"""
    cmd = [
        "python", "-m", "pytest",
        "tests/test_api_endpoints.py",
        "-v",
        "--tb=short",
        "-k", "not (docker or real_)",
        "--durations=10"
    ]
    
    return run_command(cmd, "API Integration Tests")


def run_docker_tests():
    """Run Docker integration tests"""
    print("\n🐳 Docker Integration Tests")
    print("Note: These tests require Docker and docker-compose to be running")
    
    # Check if Docker is available
    docker_available = subprocess.run(
        ["docker", "--version"], 
        capture_output=True,
        text=True
    ).returncode == 0
    
    if not docker_available:
        print("⚠️  Docker not available, skipping Docker tests")
        return True, "Skipped - Docker not available"
    
    cmd = [
        "python", "-m", "pytest",
        "tests/test_docker_services.py",
        "-v",
        "--tb=short",
        "-s",  # Don't capture output for Docker tests
        "--durations=10"
    ]
    
    return run_command(cmd, "Docker Integration Tests", timeout=600)  # 10 minutes


def run_style_checks():
    """Run code style checks"""
    results = []
    
    # Black formatting check
    success, output = run_command(
        ["python", "-m", "black", "--check", "--diff", "."],
        "Black Code Formatting Check"
    )
    results.append(("Black formatting", success))
    
    # Import sorting check
    success, output = run_command(
        ["python", "-m", "isort", "--check-only", "--diff", "."],
        "Import Sorting Check"
    )
    results.append(("Import sorting", success))
    
    return results


def generate_test_report(results):
    """Generate a summary test report"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - passed_tests
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed_tests} test categories failed")
        return 1


def main():
    """Main test runner"""
    print("🧪 Blog Poster Test Suite")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        return 1
    
    results = []
    
    # Run unit tests
    success, _ = run_unit_tests()
    results.append(("Unit Tests", success))
    
    # Run integration tests
    success, _ = run_integration_tests()
    results.append(("API Integration Tests", success))
    
    # Run Docker tests (optional)
    if "--include-docker" in sys.argv:
        success, _ = run_docker_tests()
        results.append(("Docker Integration Tests", success))
    else:
        print("\n⏭️  Skipping Docker tests (use --include-docker to run them)")
    
    # Run style checks (optional)
    if "--include-style" in sys.argv:
        style_results = run_style_checks()
        results.extend(style_results)
    else:
        print("\n⏭️  Skipping style checks (use --include-style to run them)")
    
    # Generate report
    return generate_test_report(results)


if __name__ == "__main__":
    sys.exit(main())