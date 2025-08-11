"""
Redis caching utilities for the application
"""
import json
import hashlib
import logging
from typing import Optional, Any, Callable, Union
from functools import wraps
from datetime import timedelta

import redis
from redis.exceptions import RedisError
from tenacity import retry, stop_after_attempt, wait_exponential

from src.core.config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Redis cache manager with automatic serialization and error handling
    """
    
    def __init__(self):
        self.redis_client = None
        self.is_connected = False
        self._connect()
    
    def _connect(self):
        """Establish Redis connection"""
        try:
            if settings.redis_url:
                self.redis_client = redis.from_url(
                    settings.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30
                )
                # Test connection
                self.redis_client.ping()
                self.is_connected = True
                logger.info("Redis cache connected successfully")
            else:
                logger.warning("Redis URL not configured, caching disabled")
        except RedisError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.is_connected = False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5)
    )
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache with automatic deserialization"""
        if not self.is_connected:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except RedisError as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5)
    )
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache with automatic serialization"""
        if not self.is_connected:
            return False
        
        try:
            # Serialize if needed
            if not isinstance(value, str):
                value = json.dumps(value)
            
            # Set with TTL if provided
            if ttl:
                self.redis_client.setex(key, ttl, value)
            else:
                self.redis_client.set(key, value)
            
            return True
        except (RedisError, json.JSONEncodeError) as e:
            logger.warning(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.is_connected:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except RedisError as e:
            logger.warning(f"Cache delete error for key {key}: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        if not self.is_connected:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except RedisError as e:
            logger.warning(f"Cache clear pattern error for {pattern}: {e}")
            return 0
    
    def get_ttl(self, key: str) -> Optional[int]:
        """Get TTL for a key"""
        if not self.is_connected:
            return None
        
        try:
            ttl = self.redis_client.ttl(key)
            return ttl if ttl >= 0 else None
        except RedisError:
            return None


# Singleton instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Get or create cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments"""
    key_data = f"{args}:{kwargs}"
    return hashlib.md5(key_data.encode()).hexdigest()


def cached(
    ttl: Union[int, timedelta] = 3600,
    prefix: str = "cache",
    key_func: Optional[Callable] = None
):
    """
    Decorator for caching function results
    
    Args:
        ttl: Time to live in seconds or timedelta
        prefix: Cache key prefix
        key_func: Custom key generation function
    
    Example:
        @cached(ttl=3600, prefix="articles")
        async def get_article(article_id: str):
            return fetch_article_from_db(article_id)
    """
    if isinstance(ttl, timedelta):
        ttl = int(ttl.total_seconds())
    
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = f"{prefix}:{key_func(*args, **kwargs)}"
            else:
                key_data = f"{func.__name__}:{args}:{kwargs}"
                cache_key = f"{prefix}:{hashlib.md5(key_data.encode()).hexdigest()}"
            
            # Try to get from cache
            cache = get_cache_manager()
            cached_value = cache.get(cache_key)
            
            if cached_value is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_value
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {cache_key} with TTL {ttl}s")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = f"{prefix}:{key_func(*args, **kwargs)}"
            else:
                key_data = f"{func.__name__}:{args}:{kwargs}"
                cache_key = f"{prefix}:{hashlib.md5(key_data.encode()).hexdigest()}"
            
            # Try to get from cache
            cache = get_cache_manager()
            cached_value = cache.get(cache_key)
            
            if cached_value is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_value
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {cache_key} with TTL {ttl}s")
            
            return result
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def invalidate_cache(pattern: str):
    """
    Invalidate cache entries matching pattern
    
    Args:
        pattern: Redis pattern (e.g., "articles:*")
    """
    cache = get_cache_manager()
    count = cache.clear_pattern(pattern)
    logger.info(f"Invalidated {count} cache entries matching {pattern}")
    return count