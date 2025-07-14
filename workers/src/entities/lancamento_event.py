from datetime import date
from pydantic import BaseModel
from typing_extensions import Literal

class LancamentoCriadoEvent(BaseModel):
    id: int
    valor: float
    tipo: Literal["CREDITO", "DEBITO"]
    descricao: str
    data: date