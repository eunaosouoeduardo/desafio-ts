from fastapi import FastAPI, Depends
from datetime import date

from src.entities.consolidado import ConsolidadoDiario
from src.use_cases.obter_consolidado import ObterConsolidadoUseCase
from src.infrastructure.elasticsearch_repository import ElasticsearchConsolidadoRepository
from src.infrastructure.redis_cache import RedisCacheHandler
from src.core.tracing import setup_tracing, instrument_fastapi

app = FastAPI()
tracer = setup_tracing("consolidado_service")
instrument_fastapi(app)


def get_repository():
    return ElasticsearchConsolidadoRepository()

def get_cache():
    return RedisCacheHandler()

def get_use_case(
    repo: ElasticsearchConsolidadoRepository = Depends(get_repository),
    cache: RedisCacheHandler = Depends(get_cache)
):
    return ObterConsolidadoUseCase(repository=repo, cache=cache)


@app.get("/consolidado/{data}")
async def get_consolidado(
    data: date,
    use_case: ObterConsolidadoUseCase = Depends(get_use_case)
):
    consolidado = await use_case.execute(data)
    if not consolidado:
        return {"error": "Dados não encontrados"}, 404
    return consolidado