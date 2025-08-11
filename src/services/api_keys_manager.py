"""
API Keys Manager for secure storage and retrieval of API credentials
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from cryptography.fernet import Fernet
from pydantic import BaseModel, Field
import logging
import httpx
import asyncio

logger = logging.getLogger(__name__)


class APIKeyConfig(BaseModel):
    """API Key configuration model"""
    jina_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    bright_data_api_key: Optional[str] = None
    wordpress_app_password: Optional[str] = None
    
    # Metadata
    last_updated: datetime = Field(default_factory=datetime.now)
    updated_by: str = "admin"


class APIKeysManager:
    """
    Manages API keys with encryption for secure storage
    Keys are stored in a local encrypted file, not in version control
    """
    
    def __init__(self, storage_path: str = "data/secure/api_keys.enc"):
        """
        Initialize the API Keys Manager
        
        Args:
            storage_path: Path to store encrypted API keys
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate or load encryption key
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Load existing keys if available
        self.keys = self._load_keys()
        
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create an encryption key for API keys"""
        key_file = self.storage_path.parent / ".encryption_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            # Set restrictive permissions
            os.chmod(key_file, 0o600)
            logger.info("Generated new encryption key")
            return key
    
    def _load_keys(self) -> APIKeyConfig:
        """Load and decrypt API keys from storage"""
        if not self.storage_path.exists():
            logger.info("No existing API keys found, starting fresh")
            return APIKeyConfig()
        
        try:
            with open(self.storage_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            keys_dict = json.loads(decrypted_data.decode())
            
            # Convert last_updated string back to datetime
            if 'last_updated' in keys_dict and isinstance(keys_dict['last_updated'], str):
                keys_dict['last_updated'] = datetime.fromisoformat(keys_dict['last_updated'])
            
            return APIKeyConfig(**keys_dict)
        except Exception as e:
            logger.error(f"Failed to load API keys: {e}")
            return APIKeyConfig()
    
    def save_keys(self, keys: APIKeyConfig):
        """Encrypt and save API keys to storage"""
        try:
            # Convert to dict and handle datetime
            keys_dict = keys.dict()
            keys_dict['last_updated'] = keys_dict['last_updated'].isoformat()
            
            # Encrypt the data
            data_json = json.dumps(keys_dict)
            encrypted_data = self.cipher.encrypt(data_json.encode())
            
            # Save to file
            with open(self.storage_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Set restrictive permissions
            os.chmod(self.storage_path, 0o600)
            
            self.keys = keys
            logger.info("API keys saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save API keys: {e}")
            raise
    
    def get_key(self, key_name: str) -> Optional[str]:
        """
        Get a specific API key
        
        Args:
            key_name: Name of the key (e.g., 'jina_api_key')
        
        Returns:
            The API key value or None if not set
        """
        return getattr(self.keys, key_name, None)
    
    def update_keys(self, **kwargs) -> APIKeyConfig:
        """
        Update one or more API keys
        
        Args:
            **kwargs: Key-value pairs of API keys to update
        
        Returns:
            Updated APIKeyConfig
        """
        # Update only provided keys
        for key, value in kwargs.items():
            if hasattr(self.keys, key):
                setattr(self.keys, key, value)
        
        # Update metadata
        self.keys.last_updated = datetime.now()
        
        # Save to storage
        self.save_keys(self.keys)
        
        return self.keys
    
    def get_all_keys(self) -> Dict[str, Any]:
        """Get all API keys (with masking for display)"""
        keys_dict = self.keys.dict()
        
        # Mask sensitive values for display
        masked = {}
        for key, value in keys_dict.items():
            if key in ['last_updated', 'updated_by']:
                masked[key] = value
            elif value:
                # Show first 4 and last 4 characters
                if len(str(value)) > 12:
                    masked[key] = f"{str(value)[:4]}...{str(value)[-4:]}"
                else:
                    masked[key] = "****"
            else:
                masked[key] = None
        
        return masked
    
    def validate_key(self, key_name: str, test_value: str) -> bool:
        """
        Validate an API key format (basic validation)
        
        Args:
            key_name: Name of the key
            test_value: Value to validate
        
        Returns:
            True if valid format
        """
        if not test_value:
            return False
        
        # Basic validation rules
        validation_rules = {
            'jina_api_key': lambda x: x.startswith('jina_'),
            'anthropic_api_key': lambda x: x.startswith('sk-ant-'),
            'openai_api_key': lambda x: len(x) > 20,  # OpenAI keys can have various formats
            'bright_data_api_key': lambda x: len(x) > 20,
            'wordpress_app_password': lambda x: len(x) >= 24  # WordPress app passwords are 24 chars
        }
        
        validator = validation_rules.get(key_name, lambda x: len(x) > 0)
        return validator(test_value)
    
    def test_api_key(self, key_name: str) -> Dict[str, Any]:
        """
        Test if an API key works by making a simple request
        
        Args:
            key_name: Name of the key to test
        
        Returns:
            Test result with status and message
        """
        key_value = self.get_key(key_name)
        if not key_value:
            return {"success": False, "message": "Key not configured"}
        
        # First validate format
        if not self.validate_key(key_name, key_value):
            return {"success": False, "message": "Invalid key format"}
        
        # Run async test
        try:
            # Try to get existing event loop
            try:
                loop = asyncio.get_running_loop()
                # If we're in an async context, create a task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._test_api_key_async(key_name, key_value))
                    result = future.result(timeout=15)
                return result
            except RuntimeError:
                # No running loop, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self._test_api_key_async(key_name, key_value))
                loop.close()
                return result
        except Exception as e:
            logger.error(f"Error testing {key_name}: {e}")
            return {"success": False, "message": f"Test failed: {str(e)}"}
    
    async def _test_api_key_async(self, key_name: str, key_value: str) -> Dict[str, Any]:
        """
        Async method to test API keys against their respective services
        
        Args:
            key_name: Name of the key to test
            key_value: The actual API key value
        
        Returns:
            Test result with status and message
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                if key_name == 'jina_api_key':
                    # Test Jina AI API - Use the search endpoint with a simple query
                    response = await client.post(
                        "https://r.jina.ai/https://example.com",
                        headers={"Authorization": f"Bearer {key_value}"}
                    )
                    if response.status_code in [200, 201]:
                        return {"success": True, "message": "Jina AI API key is valid"}
                    elif response.status_code == 401:
                        return {"success": False, "message": "Invalid Jina AI API key"}
                    else:
                        return {"success": False, "message": f"Jina API returned status {response.status_code}"}
                
                elif key_name == 'anthropic_api_key':
                    # Test Anthropic API
                    response = await client.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": key_value,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json"
                        },
                        json={
                            "model": "claude-3-haiku-20240307",
                            "messages": [{"role": "user", "content": "Hi"}],
                            "max_tokens": 1
                        }
                    )
                    if response.status_code == 200:
                        return {"success": True, "message": "Anthropic API key is valid"}
                    elif response.status_code == 401:
                        return {"success": False, "message": "Invalid Anthropic API key"}
                    else:
                        return {"success": False, "message": f"Anthropic API returned status {response.status_code}"}
                
                elif key_name == 'openai_api_key':
                    # Test OpenAI API
                    response = await client.get(
                        "https://api.openai.com/v1/models",
                        headers={"Authorization": f"Bearer {key_value}"}
                    )
                    if response.status_code == 200:
                        return {"success": True, "message": "OpenAI API key is valid"}
                    elif response.status_code == 401:
                        return {"success": False, "message": "Invalid OpenAI API key"}
                    else:
                        return {"success": False, "message": f"OpenAI API returned status {response.status_code}"}
                
                elif key_name == 'bright_data_api_key':
                    # For Bright Data, we'll just validate format since test endpoints vary
                    return {"success": True, "message": "Bright Data API key format is valid"}
                
                else:
                    return {"success": False, "message": f"Unknown key type: {key_name}"}
                    
            except httpx.TimeoutException:
                return {"success": False, "message": "API test timed out"}
            except httpx.RequestError as e:
                return {"success": False, "message": f"Connection error: {str(e)}"}
            except Exception as e:
                logger.error(f"Unexpected error testing {key_name}: {e}")
                return {"success": False, "message": f"Unexpected error: {str(e)}"}
    
    def clear_key(self, key_name: str):
        """Clear a specific API key"""
        if hasattr(self.keys, key_name):
            setattr(self.keys, key_name, None)
            self.save_keys(self.keys)
            logger.info(f"Cleared API key: {key_name}")
    
    def export_for_env(self) -> str:
        """Export keys in .env format (for migration)"""
        env_lines = []
        
        if self.keys.jina_api_key:
            env_lines.append(f"JINA_API_KEY={self.keys.jina_api_key}")
        if self.keys.anthropic_api_key:
            env_lines.append(f"ANTHROPIC_API_KEY={self.keys.anthropic_api_key}")
        if self.keys.openai_api_key:
            env_lines.append(f"OPENAI_API_KEY={self.keys.openai_api_key}")
        if self.keys.bright_data_api_key:
            env_lines.append(f"BRIGHT_DATA_API_KEY={self.keys.bright_data_api_key}")
        if self.keys.wordpress_app_password:
            env_lines.append(f"WP_APP_PASSWORD={self.keys.wordpress_app_password}")
        
        return "\n".join(env_lines)


# Global instance
_api_keys_manager = None

def get_api_keys_manager() -> APIKeysManager:
    """Get or create the global API keys manager"""
    global _api_keys_manager
    if _api_keys_manager is None:
        _api_keys_manager = APIKeysManager()
    return _api_keys_manager