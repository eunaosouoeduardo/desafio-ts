from datetime import date
from typing import Optional
from elasticsearch import Elasticsearch, NotFoundError
from src.interfaces.repositories import IConsolidadoRepository
from src.entities.consolidado_diario import ConsolidadoDiario
from src.entities.lancamento_event import LancamentoCriadoEvent

class ElasticsearchConsolidadoRepository(IConsolidadoRepository):
    def __init__(self, es_host: str = 'elasticsearch', es_port: int = 9200):
        self.es = Elasticsearch([f"{es_host}:{es_port}"])
        self.index_name = "consolidados-diarios"
    
    async def obter_por_data(self, data: date) -> Optional[ConsolidadoDiario]:
        try:
            result = self.es.get(index=self.index_name, id=data.isoformat())
            return ConsolidadoDiario(**result['_source'])
        except NotFoundError:
            return None
        except Exception as e:
            print(f"[Elasticsearch] Erro ao buscar consolidado: {e}")
            return None

    async def atualizar_consolidado(self, data: date, valor: float, tipo: str) -> ConsolidadoDiario:
        consolidado = await self.obter_por_data(data) or ConsolidadoDiario(data=data)

        if tipo.upper() == "CREDITO":
            consolidado.total_creditos += valor
            consolidado.saldo_final += valor
        elif tipo.upper() == "DEBITO":
            consolidado.total_debitos += valor
            consolidado.saldo_final -= valor
        else:
            raise ValueError("Tipo inválido: deve ser 'CREDITO' ou 'DEBITO'.")

        self.es.index(
            index=self.index_name,
            id=consolidado.data.isoformat(),
            body=consolidado.dict(),
            refresh=True
        )

        return consolidado