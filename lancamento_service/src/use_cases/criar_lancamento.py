from datetime import date
from typing import Optional

from src.entities.lancamento import Lancamento
from src.interfaces.repositories import ILancamentoRepository
from src.interfaces.cache import ICacheHandler
from src.interfaces.messaging import IMessagePublisher


class CriarLancamentoUseCase:
    def __init__(
            self,
            repository: ILancamentoRepository,
            cache: ICacheHandler,
            message_publisher: IMessagePublisher
    ):
        self.repo = repository
        self.cache = cache
        self.publisher = message_publisher

    def execute(self, lancamento_data: Lancamento) -> Lancamento:
        if lancamento_data.valor <= 0:
            raise ValueError("Valor deve ser positivo")
        
        lancamento = self.repo.criar(lancamento_data.model_dump())

        try:
            self.cache.invalidate(f"consolidado:{lancamento_data.data.isoformat()}")
        except:
            print("Erro ao invalidar cache")
            #logging.error("Erro ao invalidar cache!")

        try:
            self.publisher.publish("lancamento_criado", {
                "id": lancamento.id,
                "valor": lancamento.valor,
                "tipo": lancamento.tipo,
                "data": lancamento.data.isoformat(),
                "descricao": lancamento.descricao
            })
            print(f"Mensagem publicada com sucesso: {lancamento_data}")
            
        except Exception as e:
            print(f"Erro ao publicar mensagem: {e}")
            #logging.error(f"Erro ao publicar mensagem: {e}")

        return lancamento