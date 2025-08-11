"""
Utility functions for API key management
Provides a unified interface to get API keys from secure storage or environment variables
"""
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_api_key(key_name: str, env_name: Optional[str] = None) -> Optional[str]:
    """
    Get an API key from secure storage or environment variable
    
    Args:
        key_name: Name of the key in secure storage (e.g., 'jina_api_key')
        env_name: Optional environment variable name to check as fallback
    
    Returns:
        The API key value or None if not found
    """
    # Try to get from secure storage first
    try:
        from src.services.api_keys_manager import get_api_keys_manager
        api_keys_manager = get_api_keys_manager()
        stored_key = api_keys_manager.get_key(key_name)
        if stored_key:
            logger.debug(f"Using {key_name} from secure storage")
            return stored_key
    except Exception as e:
        logger.debug(f"Could not get {key_name} from secure storage: {e}")
    
    # Fall back to environment variable
    if env_name:
        env_key = os.getenv(env_name)
        if env_key:
            logger.debug(f"Using {key_name} from environment variable {env_name}")
            return env_key
    
    # Try default environment variable based on key name
    default_env_name = key_name.upper()
    env_key = os.getenv(default_env_name)
    if env_key:
        logger.debug(f"Using {key_name} from environment variable {default_env_name}")
        return env_key
    
    logger.debug(f"No API key found for {key_name}")
    return None


def get_jina_api_key() -> Optional[str]:
    """Get Jina AI API key from secure storage or environment"""
    return get_api_key('jina_api_key', 'JINA_API_KEY')


def get_anthropic_api_key() -> Optional[str]:
    """Get Anthropic API key from secure storage or environment"""
    return get_api_key('anthropic_api_key', 'ANTHROPIC_API_KEY')


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from secure storage or environment"""
    return get_api_key('openai_api_key', 'OPENAI_API_KEY')


def get_bright_data_api_key() -> Optional[str]:
    """Get Bright Data API key from secure storage or environment"""
    return get_api_key('bright_data_api_key', 'BRIGHT_DATA_API_KEY')


def get_wordpress_app_password() -> Optional[str]:
    """Get WordPress app password from secure storage or environment"""
    return get_api_key('wordpress_app_password', 'WP_APP_PASSWORD')