import redis
import json
from datetime import date
from typing import Optional, Any
from src.interfaces.cache import ICacheHandler

class RedisCacheHandler(ICacheHandler):
    def __init__(self, host: str = 'redis', port: int = 6379, db: int = 0):
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        try:
            cached = self.redis.get(key)
            return json.loads(cached) if cached else None
        except json.JSONDecodeError:
            print(f"[RedisCacheHandler] Erro ao decodificar JSON para a chave {key}")
            return None
    
    def set(self, key: str, value: any, ttl: Optional[int] = None) -> bool:
        try:
            def default_serializer(obj):
                if isinstance(obj, (date,)):
                    return obj.isoformat()
                raise TypeError(f"Tipo não serializável: {type(obj)}")
            serialized = json.dumps(value, default=default_serializer)

            if ttl:
                return self.redis.setex(key, ttl, serialized)
            return self.redis.set(key, serialized)
        
        except TypeError as e:
            print(f"[RedisCacheHandler] Erro ao serializar valor para a chave {key}: {e}")
            return False

        
    def invalidate(self, key: str) -> bool:
        return bool(self.redis.delete(key))