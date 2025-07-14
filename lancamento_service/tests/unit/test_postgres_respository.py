import pytest
from unittest.mock import MagicMock
from src.infrastructure.postgres_models import LancamentoORM
from src.infrastructure.postgres_repository import PostgresLancamentoRepository

def test_criar_lancamento():
    # Mock da sessão do SQLAlchemy
    mock_db = MagicMock()
    
    repo = PostgresLancamentoRepository(db=mock_db)
    
    lancamento_data = {
        "id": 1,
        "valor": 150.0,
        "tipo": "CREDITO",
        "descricao": "Teste criação",
        "data": "2025-07-14"
    }
    
    # Execução do método
    result = repo.criar(lancamento_data)
    
    # Verificações de chamadas na sessão
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    
    args, kwargs = mock_db.add.call_args
    assert isinstance(args[0], LancamentoORM)
    
    assert isinstance(result, LancamentoORM)
