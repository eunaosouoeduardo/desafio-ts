import redis
from src.core.config import settings
from functools import lru_cache

@lru_cache()
def get_redis_client():
    """
    Retorna uma instância do cliente Redis com cache
    """
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True
    )

# Instância global do Redis
redis_client = get_redis_client()