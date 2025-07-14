from datetime import date
from pydantic import BaseModel

class ConsolidadoDiario(BaseModel):
    data: date
    total_creditos: float = 0
    total_debitos: float = 0
    saldo_final: float = 0
