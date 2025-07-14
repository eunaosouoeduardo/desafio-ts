from celery import Celery
from src.infastructure.elasticsearch_repository import ElasticsearchConsolidadoRepository
from src.infastructure.redis_cache import RedisCacheHandler
from src.use_cases.processar_lancamento import ProcessarLancamentoUseCase
from core.config import settings

def create_celery_app():
    app = Celery(
        'workers',
        broker=f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}',
        backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
    )
    
    # Configurações
    app.conf.task_serializer = 'json'
    app.conf.result_serializer = 'json'
    app.conf.accept_content = ['json']
    app.conf.task_create_missing_queues = True
    app.conf.task_default_queue = 'consolidado_queue'
    
    return app

celery_app = create_celery_app()

# Inicializa dependências (serão recriadas em cada worker)
def get_use_case():
    repo = ElasticsearchConsolidadoRepository()
    cache = RedisCacheHandler()
    return ProcessarLancamentoUseCase(repo, cache)

@celery_app.task(name='processar_lancamento', bind=True, max_retries=3)
def processar_lancamento(self, event_data):
    use_case = get_use_case()
    try:
        return use_case.execute(event_data)
    except Exception as exc:
        self.retry(exc=exc, countdown=2 ** self.request.retry)