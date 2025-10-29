# Location: src/cache/redis_client.py
import redis.asyncio as redis
from src.config import get_settings
from src.core.logger import logger
from typing import Optional, Any
import json

settings = get_settings()

class RedisClient:
    """Redis client for caching and session management."""
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis."""
        self.redis = await redis.from_url(
            settings.redis_url,
            encoding="utf8",
            decode_responses=True,
        )
        logger.info("✅ Connected to Redis")
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
        logger.info("✅ Disconnected from Redis")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.redis:
            return None
        value = await self.redis.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        if not self.redis:
            return False
        ttl = ttl or settings.redis_ttl
        await self.redis.setex(key, ttl, json.dumps(value))
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.redis:
            return False
        await self.redis.delete(key)
        return True
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        if not self.redis:
            return False
        return await self.redis.exists(key) > 0

# Global instance
redis_client = RedisClient()

async def get_redis() -> RedisClient:
    """Dependency for getting Redis client."""
    return redis_client
