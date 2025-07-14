from datetime import date
from pydantic import BaseModel

class ConsolidadoDiario(BaseModel):
    data: date
    total_creditos: float
    total_debitos: float
    saldo_final: float