from sqlalchemy.orm import Session
from src.infrastructure.postgres_models import LancamentoORM
from src.interfaces.repositories import ILancamentoRepository

class PostgresLancamentoRepository(ILancamentoRepository):
    def __init__(self, db: Session):
        self.db = db

    def criar(self, lancamento_data: dict) -> LancamentoORM:
        db_lancamento = LancamentoORM(**lancamento_data)
        self.db.add(db_lancamento)
        self.db.commit()
        self.db.refresh(db_lancamento)
        return db_lancamento
    
    