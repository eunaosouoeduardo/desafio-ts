from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.entities.lancamento import Lancamento
from src.use_cases.criar_lancamento import CriarLancamentoUseCase
from src.infrastructure.postgres_repository import PostgresLancamentoRepository
from src.infrastructure.redis_cache import RedisCacheHandler
from src.infrastructure.rabbitmq_publisher import RabbitMQPublisher
from src.core.database import get_db
from src.core.tracing import setup_tracing, instrument_fastapi

app = FastAPI()
tracer = setup_tracing("lancamento_service")
instrument_fastapi(app)


def get_use_case(db: Session = Depends(get_db)):
    return CriarLancamentoUseCase(
        repository=PostgresLancamentoRepository(db),
        cache=RedisCacheHandler(),
        message_publisher=RabbitMQPublisher()
    )

@app.post("/lancamentos")
def criar_lancamento(
    lancamento_data: Lancamento,
    use_case: CriarLancamentoUseCase = Depends(get_use_case)
):
    try:
        lancamento = use_case.execute(lancamento_data)
        return lancamento
    except ValueError as e:
        raise HTTPException(detail=str(e))
        