from typing import Dict, Any
from datetime import date

from src.entities.lancamento_event import LancamentoCriadoEvent
from src.interfaces.repositories import IConsolidadoRepository
from src.interfaces.cache import ICacheHandler

class ProcessarLancamentoUseCase:
    def __init__(self, consolidado_repo: IConsolidadoRepository, cache: ICacheHandler):
        self.consolidado_repo = consolidado_repo
        self.cache = cache
    

    
    async def execute(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Processando evento execute: {event_data}")
        try:
            event = LancamentoCriadoEvent(**event_data)
            
            consolidado = await self.consolidado_repo.atualizar_consolidado(
                data=event.data,
                valor=event.valor,
                tipo=event.tipo
            )
            
            # Invalida o cache para forçar atualização na próxima consulta
            cache_key = f"consolidado:{event.data.isoformat()}"
            self.cache.set(cache_key, consolidado.model_dump())
            
            
            return {
                "status": "success",
                "data": event.data.isoformat(),
                "processed_value": event.valor
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "event_data": event_data
            }