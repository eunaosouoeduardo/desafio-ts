from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LancamentoORM(Base):
    __tablename__ = "lancamentos"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data = Column(Date, nullable=False)
