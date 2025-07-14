import json
import asyncio
from celery import Celery
from kombu import Exchange, Queue

from src.infrastructure.elasticsearch_repository import ElasticsearchConsolidadoRepository
from src.infrastructure.redis_cache import RedisCacheHandler
from src.use_cases.processar_lancamento import ProcessarLancamentoUseCase
from config import settings
from tracing import instrument_celery


app = Celery(
    'workers',
    broker=f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}',
    backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
)
# tracing
instrument_celery(app)

# Configurações
app.conf.update(
    task_protocol= 1,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    task_default_queue='lancamento_criado',
    task_queues=[
        Queue(
            'lancamento_criado',
            exchange=Exchange('lancamentos', type='topic'),
            routing_key='lancamento_criado',
            durable=True
        )
    ],
    broker_transport_options={
        'visibility_timeout': 3600,
        'confirm_publish': True
    }
)

# Inicializa dependências
repo = ElasticsearchConsolidadoRepository()
cache = RedisCacheHandler()
use_case = ProcessarLancamentoUseCase(repo, cache)




@app.task(name='processar_lancamento', bind=True, serializer='json')
def processar_lancamento_task(self, event_data):
    try:
        print(f"Processando mensagem: {event_data}")
        
        if isinstance(event_data, str):
            event_data = json.loads(event_data)
        result = asyncio.run(use_case.execute(event_data))
        return {'status': 'success', 'result': result}
    
    except Exception as exc:
        print(f"Erro no processamento: {str(exc)}")
        self.retry(exc=exc, countdown=60)
