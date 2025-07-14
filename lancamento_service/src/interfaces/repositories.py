from abc import ABC, abstractmethod
from typing import Optional
from datetime import date
from src.entities.lancamento import Lancamento

class ILancamentoRepository(ABC):
    @abstractmethod
    def criar(self, lancamento_data: dict) -> Lancamento:
        pass
