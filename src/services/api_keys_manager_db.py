"""
API Keys Manager with PostgreSQL Backend
Securely manages API keys using database storage with encryption
"""
import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime
from cryptography.fernet import Fernet
import base64

from src.database import get_db_session
from src.database.repositories import ApiKeyRepository

logger = logging.getLogger(__name__)


class APIKeysManagerDB:
    """
    Manages API keys with PostgreSQL storage and encryption
    """
    
    def __init__(self):
        """Initialize API Keys Manager with database backend"""
        # Get or create encryption key from environment
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        
    def _get_or_create_encryption_key(self) -> bytes:
        """Get encryption key from environment or create new one"""
        key_str = os.getenv('API_ENCRYPTION_KEY')
        
        if key_str:
            # Decode from base64 if exists
            return base64.b64decode(key_str.encode())
        else:
            # Generate new key (for local development)
            # In production, this should be set via environment variable
            key = Fernet.generate_key()
            logger.warning("Generated new encryption key - set API_ENCRYPTION_KEY in production!")
            return key
    
    def set_key(self, service: str, api_key: str) -> bool:
        """
        Store an encrypted API key in database
        
        Args:
            service: Service name (e.g., 'anthropic', 'openai', 'jina')
            api_key: The actual API key to store
            
        Returns:
            bool: Success status
        """
        try:
            # Encrypt the API key
            encrypted_key = self.cipher.encrypt(api_key.encode()).decode()
            
            # Create preview (first 4 and last 4 characters)
            if len(api_key) > 8:
                preview = f"{api_key[:4]}...{api_key[-4:]}"
            else:
                preview = "****"
            
            # Store in database
            with get_db_session() as db:
                repo = ApiKeyRepository(db)
                repo.upsert(
                    service=service.lower(),
                    encrypted_key=encrypted_key,
                    key_preview=preview
                )
            
            logger.info(f"API key for {service} saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save API key for {service}: {e}")
            return False
    
    def get_key(self, service: str) -> Optional[str]:
        """
        Retrieve and decrypt an API key from database
        
        Args:
            service: Service name
            
        Returns:
            Decrypted API key or None if not found
        """
        try:
            with get_db_session() as db:
                repo = ApiKeyRepository(db)
                api_key = repo.get_by_service(service.lower())
                
                if not api_key:
                    return None
                
                # Decrypt the key
                decrypted = self.cipher.decrypt(api_key.encrypted_key.encode()).decode()
                
                # Update usage statistics
                repo.update_usage(service.lower())
                
                return decrypted
                
        except Exception as e:
            logger.error(f"Failed to retrieve API key for {service}: {e}")
            return None
    
    def get_all_keys(self, masked: bool = True) -> Dict[str, str]:
        """
        Get all API keys (masked by default for display)
        
        Args:
            masked: If True, return masked versions for display
            
        Returns:
            Dictionary of service: key pairs
        """
        try:
            with get_db_session() as db:
                repo = ApiKeyRepository(db)
                api_keys = repo.get_all_active()
                
                result = {}
                for api_key in api_keys:
                    if masked:
                        # Return preview version
                        result[api_key.service] = api_key.key_preview or "****"
                    else:
                        # Decrypt and return actual key (use with caution!)
                        try:
                            decrypted = self.cipher.decrypt(api_key.encrypted_key.encode()).decode()
                            result[api_key.service] = decrypted
                        except:
                            result[api_key.service] = "Error decrypting"
                
                return result
                
        except Exception as e:
            logger.error(f"Failed to get all API keys: {e}")
            return {}
    
    def delete_key(self, service: str) -> bool:
        """
        Deactivate an API key (soft delete)
        
        Args:
            service: Service name
            
        Returns:
            bool: Success status
        """
        try:
            with get_db_session() as db:
                repo = ApiKeyRepository(db)
                return repo.deactivate(service.lower())
                
        except Exception as e:
            logger.error(f"Failed to delete API key for {service}: {e}")
            return False
    
    def validate_key(self, service: str) -> bool:
        """
        Check if a valid API key exists for a service
        
        Args:
            service: Service name
            
        Returns:
            bool: True if valid key exists
        """
        key = self.get_key(service)
        return key is not None and len(key) > 0
    
    def get_key_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for all API keys
        
        Returns:
            Dictionary with usage stats
        """
        try:
            with get_db_session() as db:
                repo = ApiKeyRepository(db)
                api_keys = repo.get_all_active()
                
                stats = {}
                for api_key in api_keys:
                    stats[api_key.service] = {
                        'active': api_key.is_active,
                        'last_used': api_key.last_used_at.isoformat() if api_key.last_used_at else 'Never',
                        'usage_count': api_key.usage_count or 0,
                        'created': api_key.created_at.isoformat() if api_key.created_at else 'Unknown'
                    }
                
                return stats
                
        except Exception as e:
            logger.error(f"Failed to get API key stats: {e}")
            return {}
    
    # Convenience methods for specific services
    def get_anthropic_key(self) -> Optional[str]:
        """Get Anthropic API key"""
        return self.get_key('anthropic')
    
    def get_openai_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return self.get_key('openai')
    
    def get_jina_key(self) -> Optional[str]:
        """Get Jina API key"""
        return self.get_key('jina')
    
    def get_bright_data_key(self) -> Optional[str]:
        """Get Bright Data API key"""
        return self.get_key('bright_data')


# Singleton instance
_manager_instance = None


def get_api_keys_manager_db() -> APIKeysManagerDB:
    """Get or create API keys manager instance"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = APIKeysManagerDB()
    return _manager_instance