from elasticsearch import Elasticsearch, RequestsHttpConnection
from src.core.config import settings
from functools import lru_cache


@lru_cache()
def get_es_client():
    """
    Retorna uma instância do cliente Elasticsearch com cache
    """
    return Elasticsearch(
        hosts=[{'host': settings.ES_HOST, 'port': settings.ES_PORT}],
        connection_class=RequestsHttpConnection,
        timeout=30,
        max_retries=3,
        retry_on_timeout=True
    )

# Instância global do Elasticsearch
es_client = get_es_client()