from datetime import date
from typing import Optional
import redis
from opentelemetry import trace

from src.entities.consolidado import ConsolidadoDiario
from src.interfaces.repositories import IConsolidadoRepository
from src.interfaces.cache import ICacheHandler

tracer = trace.get_tracer(__name__)

class ObterConsolidadoUseCase:
    def __init__(
        self,
        repository: IConsolidadoRepository,
        cache: ICacheHandler
    ):
        self.repo = repository
        self.cache = cache

    async def execute(self, data: date) -> Optional[ConsolidadoDiario]:
        cache_key = f"consolidado:{data.isoformat()}"
        print('Cache key:', cache_key)

        with tracer.start_as_current_span("obter_consolidado.execute") as span:
            span.set_attribute("consolidado.data", data.isoformat())

            # 🔍 Tentativa de buscar no Redis
            with tracer.start_as_current_span("obter_consolidado.cache_get"):
                try:
                    cached = self.cache.get(key=cache_key)
                    if cached:
                        span.set_attribute("consolidado.cache_hit", True)
                        return ConsolidadoDiario(**cached)
                    else:
                        span.set_attribute("consolidado.cache_hit", False)
                except redis.exceptions.ConnectionError as e:
                    span.set_attribute("consolidado.cache_error", str(e))
                    print(f"[Cache] Redis offline ou não disponível: {str(e)}")
                except Exception as e:
                    span.set_attribute("consolidado.cache_exception", str(e))
                    print(f"[Cache] Erro inesperado: {str(e)}")

            # 📦 Tentativa de buscar no banco
            with tracer.start_as_current_span("obter_consolidado.db_query"):
                consolidado = await self.repo.obter_por_data(data)
                if consolidado:
                    span.set_attribute("consolidado.db_result", "found")
                else:
                    span.set_attribute("consolidado.db_result", "not_found")

            return consolidado
