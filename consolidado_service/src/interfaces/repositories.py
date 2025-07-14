from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from src.entities.consolidado import ConsolidadoDiario

class IConsolidadoRepository(ABC):
    @abstractmethod
    async def obter_por_data(self, data: date) -> Optional[ConsolidadoDiario]:
        pass
