import json
import redis
from src.interfaces.cache import ICacheHandler
from src.core.config import settings
from src.core.redis_client import redis_client

class RedisCacheHandler(ICacheHandler):
    def __init__(self):
        self.redis = redis_client

    def get(self, key: str) -> any:
        cached = self.redis.get(key)
        return json.loads(cached) if cached else None
    
    def set(self, key: str, value: any, ttl: int = None) -> bool:
        serialized = json.dumps(value)
        if ttl:
            return self.redis.setex(key, ttl, serialized)
        return self.redis.set(key, serialized)
    

    def invalidate(self, key: str) -> bool:
        return bool(self.redis.delete(key))