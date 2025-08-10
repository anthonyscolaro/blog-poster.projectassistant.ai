#!/usr/bin/env python3
"""
Portainer API Deployment Script Template
Deploys Docker Compose stack via Portainer API using configurable environment variables

TEMPLATE USAGE:
1. Copy this script to your project's scripts/ directory
2. Configure variables in PROJECT_CONFIG section below
3. Create .env.portainer file with your Portainer credentials
4. Run: python scripts/portainer_deploy_template.py
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional
from pathlib import Path
import time

# =============================================================================
# PROJECT CONFIGURATION - CUSTOMIZE THESE VALUES FOR YOUR PROJECT
# =============================================================================
PROJECT_CONFIG = {
    # Project identifiers
    "PROJECT_NAME": "your-project",  # Change this to your project name
    "DEFAULT_STACK_NAME": "your-project-dev",  # Default stack name
    
    # File paths (relative to script directory)
    "ENV_FILE": ".env.portainer",  # Environment file name
    "COMPOSE_FILE": "docker-compose.dev.yml",  # Docker compose file
    
    # Portainer defaults
    "DEFAULT_ENDPOINT_ID": 3,  # Default Portainer environment ID
    "DEFAULT_PORTAINER_URL": "https://portainer.example.com",  # Update with your URL
    
    # Domain configuration (for success message)
    "DOMAINS": {
        "frontend": "FRONTEND_DOMAIN",
        "api": "API_DOMAIN", 
        "database": "PGADMIN_DOMAIN"
    }
}
# =============================================================================

class PortainerAPIWithToken:
    """Portainer API client using API key for stack deployment operations."""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize Portainer API client with API key.
        
        Args:
            base_url: Portainer instance URL (e.g., https://portainer.example.com)
            api_key: Portainer API access token
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"{PROJECT_CONFIG['PROJECT_NAME']}-Portainer-Deploy/1.0",
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        })
        
    def authenticate(self) -> bool:
        """
        Test API key authentication (no separate auth needed with API keys).
        
        Returns:
            bool: True if API key works, False otherwise
        """
        try:
            # Test the API key by listing environments
            response = self.session.get(f"{self.base_url}/api/endpoints", timeout=30)
            
            if response.status_code == 200:
                print("✅ Successfully authenticated with Portainer API key")
                return True
            else:
                print(f"❌ API key authentication failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API key authentication error: {e}")
            return False
    
    def list_environments(self) -> List[Dict]:
        """
        List all Portainer environments.
        
        Returns:
            List[Dict]: List of available environments
        """
        try:
            response = self.session.get(f"{self.base_url}/api/endpoints", timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to list environments: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error listing environments: {e}")
            return []
    
    def list_stacks(self) -> List[Dict]:
        """
        List all stacks in Portainer.
        
        Returns:
            List[Dict]: List of existing stacks
        """
        try:
            response = self.session.get(f"{self.base_url}/api/stacks", timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to list stacks: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error listing stacks: {e}")
            return []
    
    def list_containers(self, endpoint_id: int = None) -> List[Dict]:
        """
        List all containers in the environment.
        
        Args:
            endpoint_id: Environment ID to query
            
        Returns:
            List[Dict]: List of containers
        """
        if endpoint_id is None:
            endpoint_id = PROJECT_CONFIG["DEFAULT_ENDPOINT_ID"]
            
        try:
            response = self.session.get(
                f"{self.base_url}/api/endpoints/{endpoint_id}/docker/containers/json?all=true", 
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to list containers: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error listing containers: {e}")
            return []
    
    def stop_and_remove_container(self, container_id: str, endpoint_id: int = None) -> bool:
        """
        Stop and remove a container.
        
        Args:
            container_id: Container ID to remove
            endpoint_id: Environment ID
            
        Returns:
            bool: True if successful
        """
        if endpoint_id is None:
            endpoint_id = PROJECT_CONFIG["DEFAULT_ENDPOINT_ID"]
            
        try:
            # Stop container first
            stop_response = self.session.post(
                f"{self.base_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}/stop",
                timeout=30
            )
            
            # Remove container
            remove_response = self.session.delete(
                f"{self.base_url}/api/endpoints/{endpoint_id}/docker/containers/{container_id}?force=true",
                timeout=30
            )
            
            if remove_response.status_code in [204, 404]:  # 404 means already removed
                print(f"✅ Container {container_id[:12]} removed")
                return True
            else:
                print(f"❌ Failed to remove container {container_id[:12]}: {remove_response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error removing container {container_id[:12]}: {e}")
            return False
    
    def delete_stack(self, stack_id: int) -> bool:
        """
        Delete an existing stack.
        
        Args:
            stack_id: ID of stack to delete
            
        Returns:
            bool: True if deletion successful
        """
        try:
            response = self.session.delete(f"{self.base_url}/api/stacks/{stack_id}", timeout=60)
            if response.status_code == 204:
                print(f"✅ Successfully deleted stack {stack_id}")
                return True
            else:
                print(f"❌ Failed to delete stack: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error deleting stack: {e}")
            return False
            
    def force_delete_stack_by_name(self, stack_name: str) -> bool:
        """
        Force delete stack by finding it in the stack list and attempting removal.
        
        Args:
            stack_name: Name of stack to delete
            
        Returns:
            bool: True if deletion successful
        """
        try:
            # Get all stacks and find the one with matching name
            stacks = self.list_stacks()
            target_stack = next((stack for stack in stacks if stack.get("Name") == stack_name), None)
            
            if not target_stack:
                print(f"✅ Stack '{stack_name}' not found in stack list")
                return True
                
            stack_id = target_stack.get("Id")
            print(f"🎯 Found stack '{stack_name}' with ID {stack_id}, attempting force delete...")
            
            # Try different delete approaches
            for external_param in [True, False]:
                try:
                    params = {"external": external_param} if external_param else {}
                    response = self.session.delete(
                        f"{self.base_url}/api/stacks/{stack_id}", 
                        params=params,
                        timeout=60
                    )
                    if response.status_code in [204, 404]:
                        print(f"✅ Force deleted stack '{stack_name}' (external={external_param})")
                        return True
                    else:
                        print(f"⚠️  Delete attempt failed (external={external_param}): {response.status_code}")
                except Exception as e:
                    print(f"⚠️  Delete attempt error (external={external_param}): {e}")
                    
            return False
                    
        except Exception as e:
            print(f"❌ Force delete error: {e}")
            return False
    
    def create_stack_from_compose(
        self, 
        stack_name: str, 
        compose_content: str, 
        environment_vars: List[Dict[str, str]], 
        endpoint_id: int = None
    ) -> Optional[Dict]:
        """
        Create a new Docker Compose stack from string content.
        
        Args:
            stack_name: Name for the new stack
            compose_content: Docker Compose YAML content
            environment_vars: List of environment variables as {"name": "key", "value": "val"}
            endpoint_id: Target environment ID
            
        Returns:
            Dict: Stack creation response or None if failed
        """
        if endpoint_id is None:
            endpoint_id = PROJECT_CONFIG["DEFAULT_ENDPOINT_ID"]
            
        try:
            payload = {
                "Name": stack_name,
                "StackFileContent": compose_content,
                "Env": environment_vars
            }
            
            response = self.session.post(
                f"{self.base_url}/api/stacks/create/standalone/string",
                params={"endpointId": endpoint_id},
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                stack_data = response.json()
                print(f"✅ Successfully created stack '{stack_name}'")
                return stack_data
            else:
                print(f"❌ Failed to create stack: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creating stack: {e}")
            return None

def load_environment_variables() -> Dict[str, str]:
    """
    Load environment variables from configured environment file.
    
    Returns:
        Dict[str, str]: Environment variables as key-value pairs
    """
    env_file = Path(__file__).parent.parent / PROJECT_CONFIG["ENV_FILE"]
    
    if not env_file.exists():
        print(f"❌ Environment file not found: {env_file}")
        print(f"💡 Create {PROJECT_CONFIG['ENV_FILE']} with your Portainer credentials")
        sys.exit(1)
    
    env_vars = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    return env_vars

def load_compose_file() -> str:
    """
    Load Docker Compose file content.
    
    Returns:
        str: Docker Compose YAML content
    """
    compose_file = Path(__file__).parent.parent / PROJECT_CONFIG["COMPOSE_FILE"]
    
    if not compose_file.exists():
        print(f"❌ Compose file not found: {compose_file}")
        print(f"💡 Ensure {PROJECT_CONFIG['COMPOSE_FILE']} exists in your project root")
        sys.exit(1)
    
    with open(compose_file, 'r') as f:
        return f.read()

def convert_env_vars_to_api_format(env_vars: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Convert environment variables to Portainer API format.
    
    Args:
        env_vars: Environment variables as key-value pairs
        
    Returns:
        List[Dict[str, str]]: Environment variables in API format
    """
    return [{"name": key, "value": value} for key, value in env_vars.items()]

def cleanup_existing_containers(api: PortainerAPIWithToken, stack_name: str, endpoint_id: int):
    """
    Clean up containers related to the project.
    
    Args:
        api: Portainer API client
        stack_name: Stack name to look for
        endpoint_id: Environment ID
    """
    print("🔍 Listing all containers to find conflicts...")
    containers = api.list_containers(endpoint_id=endpoint_id)
    print(f"📊 Found {len(containers)} total containers")
    
    # Look for containers with project name in names
    project_containers = []
    project_name_lower = PROJECT_CONFIG["PROJECT_NAME"].lower()
    
    for container in containers:
        names = container.get('Names', [])
        if any(project_name_lower in name.lower() for name in names):
            project_containers.append(container)
            print(f"🎯 Found related container: {names}")
            
    if not project_containers:
        # Try to find containers by image name
        for container in containers:
            image = container.get('Image', '')
            if project_name_lower in image.lower():
                project_containers.append(container)
                print(f"🎯 Found container by image: {container.get('Names', ['Unknown'])} (image: {image})")
    
    if project_containers:
        print(f"🧹 Found {len(project_containers)} related containers to clean up...")
        for container in project_containers:
            container_id = container['Id']
            names = container.get('Names', ['Unknown'])
            print(f"🗑️  Removing container: {names[0]}")
            api.stop_and_remove_container(container_id, endpoint_id=endpoint_id)
        
        print("⏳ Waiting for container cleanup to complete...")
        time.sleep(10)
    else:
        print("ℹ️  No related containers found")

def main():
    """Main deployment function."""
    print(f"🚀 Starting {PROJECT_CONFIG['PROJECT_NAME']} stack deployment via Portainer API")
    
    # Load configuration
    env_vars = load_environment_variables()
    compose_content = load_compose_file()
    
    # Extract Portainer configuration  
    portainer_url = env_vars.get("PORTAINER_URL", PROJECT_CONFIG["DEFAULT_PORTAINER_URL"])
    portainer_user = env_vars.get("PORTAINER_WEB_USER", "admin")
    portainer_pass = env_vars.get("PORTAINER_WEB_PASS")
    stack_name = env_vars.get("STACK_NAME", PROJECT_CONFIG["DEFAULT_STACK_NAME"])
    endpoint_id = int(env_vars.get("PORTAINER_ENDPOINT_ID", str(PROJECT_CONFIG["DEFAULT_ENDPOINT_ID"])))
    
    if not portainer_pass:
        print(f"❌ PORTAINER_WEB_PASS not found in {PROJECT_CONFIG['ENV_FILE']}")
        sys.exit(1)
    
    # Initialize Portainer API client
    portainer_api_key = env_vars.get("PORTAINER_API_KEY")
    if not portainer_api_key:
        print(f"❌ PORTAINER_API_KEY not found in {PROJECT_CONFIG['ENV_FILE']}")
        sys.exit(1)
        
    api = PortainerAPIWithToken(portainer_url, portainer_api_key)
    
    # Authenticate
    if not api.authenticate():
        print("❌ Failed to authenticate with Portainer")
        sys.exit(1)
    
    # List environments to verify connectivity
    print("📋 Listing available environments...")
    environments = api.list_environments()
    if environments:
        for env in environments:
            print(f"  - Environment {env['Id']}: {env['Name']} ({env['Type']})")
    
    # Check for existing stack with same name
    print(f"🔍 Checking for existing stack '{stack_name}'...")
    existing_stacks = api.list_stacks()
    existing_stack = next((stack for stack in existing_stacks if stack["Name"] == stack_name), None)
    
    if existing_stack:
        print(f"⚠️  Stack '{stack_name}' already exists (ID: {existing_stack['Id']})")
        print("🗑️  Attempting to delete existing stack for redeployment...")
        if not api.delete_stack(existing_stack["Id"]):
            print("⚠️  Stack deletion failed, manually cleaning up containers...")
            cleanup_existing_containers(api, stack_name, endpoint_id)
            
            # Try force deleting the stack entry
            print("🔧 Attempting force delete of stack entry...")
            if api.force_delete_stack_by_name(stack_name):
                print("✅ Stack entry removed, waiting for database cleanup...")
                time.sleep(15)  # Give more time for Portainer database to update
            else:
                print("⚠️  Force delete failed, using timestamped stack name...")
                import datetime
                timestamp = datetime.datetime.now().strftime("%m%d-%H%M")
                stack_name = f"{PROJECT_CONFIG['PROJECT_NAME']}-{timestamp}"
                print(f"🔄 Using new stack name: {stack_name}")
        else:
            # Wait longer for complete cleanup
            print("⏳ Waiting for stack cleanup to complete...")
            time.sleep(15)
    
    # Convert environment variables to API format
    env_vars_api = convert_env_vars_to_api_format(env_vars)
    
    # Deploy the stack
    print(f"🚀 Deploying stack '{stack_name}'...")
    result = api.create_stack_from_compose(
        stack_name=stack_name,
        compose_content=compose_content,
        environment_vars=env_vars_api,
        endpoint_id=endpoint_id
    )
    
    if result:
        print("✅ Stack deployment completed successfully!")
        print(f"   Stack ID: {result.get('Id')}")
        print(f"   Stack Name: {result.get('Name')}")
        print(f"   Environment ID: {result.get('EndpointId')}")
        print("\n🌐 Your application should be available at:")
        
        # Display configured domains
        for service, domain_var in PROJECT_CONFIG["DOMAINS"].items():
            domain = env_vars.get(domain_var)
            if domain:
                print(f"   {service.title()}: https://{domain}")
    else:
        print("❌ Stack deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()