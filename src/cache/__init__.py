# Location: src/cache/__init__.py
from .redis_client import redis_client, get_redis

__all__ = ["redis_client", "get_redis"]
