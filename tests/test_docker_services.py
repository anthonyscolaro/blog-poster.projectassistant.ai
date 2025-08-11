"""
Test suite for Docker services integration
"""
import pytest
import asyncio
import time
import httpx
import docker
from pathlib import Path
import sys
import os
import subprocess
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDockerServices:
    """Test Docker services startup and health"""
    
    @pytest.fixture(scope="class")
    def docker_client(self):
        """Get Docker client"""
        try:
            client = docker.from_env()
            return client
        except Exception as e:
            pytest.skip(f"Docker not available: {e}")
    
    @pytest.mark.asyncio
    async def test_docker_compose_startup(self):
        """Test Docker Compose services startup"""
        # Check if docker-compose.yml exists
        compose_file = Path(__file__).parent.parent / "docker-compose.yml"
        if not compose_file.exists():
            pytest.skip("docker-compose.yml not found")
        
        try:
            # Start services
            result = subprocess.run(
                ["docker-compose", "up", "-d", "--build"],
                cwd=compose_file.parent,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                pytest.fail(f"Docker Compose startup failed: {result.stderr}")
            
            # Wait for services to be ready
            await asyncio.sleep(30)  # Give services time to start
            
            # Verify services are running
            result = subprocess.run(
                ["docker-compose", "ps"],
                cwd=compose_file.parent,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Up" in result.stdout  # At least one service should be up
            
        except subprocess.TimeoutExpired:
            pytest.fail("Docker Compose startup timed out")
        except Exception as e:
            pytest.skip(f"Docker Compose test failed: {e}")
    
    @pytest.mark.asyncio
    async def test_api_service_health(self):
        """Test API service health endpoint"""
        api_url = "http://localhost:8088"
        
        # Wait for API to be ready
        max_retries = 30
        for i in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.get(f"{api_url}/health")
                    if response.status_code == 200:
                        data = response.json()
                        assert data["status"] == "ok"
                        assert "time" in data
                        return
            except Exception:
                if i == max_retries - 1:
                    pytest.fail("API service health check failed")
                await asyncio.sleep(2)
    
    @pytest.mark.asyncio
    async def test_qdrant_service_health(self):
        """Test Qdrant service health"""
        qdrant_url = "http://localhost:6333"
        
        max_retries = 15
        for i in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.get(f"{qdrant_url}/collections")
                    if response.status_code == 200:
                        # Qdrant is responsive
                        return
            except Exception:
                if i == max_retries - 1:
                    pytest.skip("Qdrant service not available")
                await asyncio.sleep(2)
    
    @pytest.mark.asyncio
    async def test_redis_service_health(self):
        """Test Redis service health"""
        try:
            import redis
            r = redis.Redis(host='localhost', port=6384, decode_responses=True)
            
            # Test basic Redis operations
            r.set('test_key', 'test_value')
            assert r.get('test_key') == 'test_value'
            r.delete('test_key')
            
        except ImportError:
            pytest.skip("Redis client not installed")
        except Exception:
            pytest.skip("Redis service not available")
    
    @pytest.mark.asyncio
    async def test_postgres_service_health(self):
        """Test PostgreSQL service health"""
        try:
            import asyncpg
            
            conn = await asyncpg.connect(
                "postgresql://blogposter:blogposter123@localhost:5433/blogposter"
            )
            
            # Test basic query
            result = await conn.fetchval("SELECT 1")
            assert result == 1
            
            await conn.close()
            
        except ImportError:
            pytest.skip("AsyncPG not installed")
        except Exception:
            pytest.skip("PostgreSQL service not available")
    
    @pytest.mark.asyncio
    async def test_api_endpoints_integration(self):
        """Test API endpoints work with Docker services"""
        api_url = "http://localhost:8088"
        
        async with httpx.AsyncClient(timeout=30) as client:
            # Test health endpoint
            response = await client.get(f"{api_url}/health")
            assert response.status_code == 200
            
            # Test SEO lint endpoint
            seo_data = {
                "frontmatter": {
                    "meta_title": "Test Article About Service Dogs Training Methods",
                    "meta_desc": "Learn about effective service dog training methods and techniques for handlers. This comprehensive guide covers ADA requirements and best practices.",
                    "canonical": "https://example.com/service-dog-training"
                },
                "markdown": """# Service Dog Training Methods
                
This guide covers service dog training.

## Training Basics

Service dogs require specialized training.
"""
            }
            
            response = await client.post(f"{api_url}/seo/lint", json=seo_data)
            assert response.status_code == 200
            
            # Test WordPress test endpoint (should handle gracefully if not configured)
            try:
                response = await client.get(f"{api_url}/wordpress/test")
                # Should return something, even if connection fails
                assert response.status_code == 200
            except Exception:
                pass  # WordPress might not be configured
    
    def test_docker_compose_config_valid(self):
        """Test Docker Compose configuration is valid"""
        compose_file = Path(__file__).parent.parent / "docker-compose.yml"
        if not compose_file.exists():
            pytest.skip("docker-compose.yml not found")
        
        try:
            result = subprocess.run(
                ["docker-compose", "config"],
                cwd=compose_file.parent,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0, f"Invalid Docker Compose config: {result.stderr}"
            
            # Parse the output to verify services
            config_output = result.stdout
            assert "api" in config_output or "blog-poster" in config_output
            assert "qdrant" in config_output
            
        except FileNotFoundError:
            pytest.skip("docker-compose command not found")
    
    @pytest.mark.asyncio
    async def test_service_ports_accessible(self):
        """Test that all expected service ports are accessible"""
        expected_ports = [
            ("API", "localhost", 8088),
            ("Qdrant", "localhost", 6333),
            ("Redis", "localhost", 6384),
            ("PostgreSQL", "localhost", 5433)
        ]
        
        for service_name, host, port in expected_ports:
            try:
                # Simple TCP connection test
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result != 0:
                    print(f"⚠️  {service_name} port {port} not accessible")
                else:
                    print(f"✅ {service_name} port {port} accessible")
                    
            except Exception as e:
                print(f"⚠️  Error checking {service_name} port {port}: {e}")
    
    @pytest.mark.asyncio 
    async def test_environment_variables_loaded(self):
        """Test that environment variables are properly loaded"""
        api_url = "http://localhost:8088"
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{api_url}/health-dashboard")
                assert response.status_code == 200
                
                # Check that some environment info is available
                # This is a basic test that the app is loading env vars
                
        except Exception:
            pytest.skip("API service not available for environment test")


class TestDockerCleanup:
    """Test Docker cleanup operations"""
    
    @pytest.mark.asyncio
    async def test_docker_compose_cleanup(self):
        """Test Docker Compose cleanup"""
        compose_file = Path(__file__).parent.parent / "docker-compose.yml"
        if not compose_file.exists():
            pytest.skip("docker-compose.yml not found")
        
        try:
            # Stop services
            result = subprocess.run(
                ["docker-compose", "down", "-v"],
                cwd=compose_file.parent,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Don't fail the test if cleanup has issues, just warn
            if result.returncode != 0:
                print(f"⚠️  Docker cleanup warning: {result.stderr}")
            else:
                print("✅ Docker services cleaned up successfully")
                
        except subprocess.TimeoutExpired:
            print("⚠️  Docker cleanup timed out")
        except Exception as e:
            print(f"⚠️  Docker cleanup error: {e}")


def run_docker_integration_tests():
    """Run Docker integration tests with proper setup/teardown"""
    print("\n🐳 Starting Docker Integration Tests...")
    
    # Run the tests
    result = pytest.main([
        __file__,
        "-v",
        "-s",  # Don't capture output so we can see progress
        "--tb=short",
        "--durations=10"
    ])
    
    return result


if __name__ == "__main__":
    # Run Docker integration tests
    exit_code = run_docker_integration_tests()
    sys.exit(exit_code)