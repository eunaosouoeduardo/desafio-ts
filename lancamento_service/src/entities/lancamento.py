from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from typing_extensions import Literal

class Lancamento(BaseModel):
    id: Optional[int] = None
    valor: float = Field(..., ge=0, description="Valor do lançamento não pode ser negativo")
    tipo: Literal["CREDITO","DEBITO"]
    descricao: str
    data: date

    model_config = ConfigDict(from_attributes=True)