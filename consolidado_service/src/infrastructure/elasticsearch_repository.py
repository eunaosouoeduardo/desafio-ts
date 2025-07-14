from datetime import date
from typing import Optional
from elasticsearch import Elasticsearch, NotFoundError
from src.entities.consolidado import ConsolidadoDiario
from src.interfaces.repositories import IConsolidadoRepository
from src.core.es_client import es_client

class ElasticsearchConsolidadoRepository(IConsolidadoRepository):
    def __init__(self, es_host: str = 'elasticsearch', es_port: int = 9200):
        self.es = Elasticsearch([f"{es_host}:{es_port}"])
        self.index_name = "consolidados-diarios"
    
    async def obter_por_data(self, data: date) -> Optional[ConsolidadoDiario]:
        try:
            result = self.es.get(index=self.index_name, id=data.isoformat())
            print(f"[Elasticsearch] Documento encontrado: {result['_source']}")
            return ConsolidadoDiario(**result['_source'])
        except NotFoundError as e:
            print(f"[Elasticsearch] Nenhum documento encontrado com essa data: {e}")
            return None
        except Exception as e:
            print(f"[Elasticsearch] Erro ao buscar consolidado: {e}")
            return None
    
