from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from src.entities.lancamento_event import LancamentoCriadoEvent

class IConsolidadoRepository(ABC):
    @abstractmethod
    async def obter_por_data(self, data: date) -> Optional[LancamentoCriadoEvent]:
        pass
    
    @abstractmethod
    async def atualizar_consolidado(
        self,
        data: date,
        valor: float,
        tipo: str
    ) -> bool:
        pass