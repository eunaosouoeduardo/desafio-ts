import pytest
from unittest.mock import AsyncMock, Mock
from datetime import date
from src.use_cases.processar_lancamento import ProcessarLancamentoUseCase
from src.entities.consolidado_diario import ConsolidadoDiario
from src.entities.lancamento_event import LancamentoCriadoEvent

@pytest.fixture
def mock_consolidado_repo():
    mock = AsyncMock()
    mock.atualizar_consolidado.return_value = ConsolidadoDiario(
        data=date(2023, 1, 1),
        valor_total=100.0,
        quantidade_lancamentos=1
    )
    return mock

@pytest.fixture
def mock_cache_handler():
    mock = Mock()
    return mock

@pytest.fixture
def processar_lancamento_use_case(mock_consolidado_repo, mock_cache_handler):
    return ProcessarLancamentoUseCase(mock_consolidado_repo, mock_cache_handler)

@pytest.mark.asyncio
async def test_execute_success(processar_lancamento_use_case, mock_consolidado_repo, mock_cache_handler):
    event_data = {
        "id": "123",
        "data": "2023-01-01",
        "valor": 50.0,
        "tipo": "CREDITO",
        "descricao": "Teste"
    }
    
    result = await processar_lancamento_use_case.execute(event_data)
    
    assert result["status"] == "success"
    assert result["data"] == "2023-01-01"
    assert result["processed_value"] == 50.0
    
    mock_consolidado_repo.atualizar_consolidado.assert_called_once_with(
        data=date(2023, 1, 1),
        valor=50.0,
        tipo="CREDITO"
    )
    
    mock_cache_handler.set.assert_called_once()
    assert mock_cache_handler.set.call_args[0][0] == "consolidado:2023-01-01"
    assert isinstance(mock_cache_handler.set.call_args[0][1], dict)

@pytest.mark.asyncio
async def test_execute_invalid_event_data(processar_lancamento_use_case):
    event_data = {
        "id": "123",
        "data": "invalid-date", # Invalid date format
        "valor": 50.0,
        "tipo": "CREDITO",
        "descricao": "Teste"
    }
    
    result = await processar_lancamento_use_case.execute(event_data)
    
    assert result["status"] == "error"
    assert "message" in result
    assert "event_data" in result
    assert "invalid-date" in result["message"]

@pytest.mark.asyncio
async def test_execute_repository_error(processar_lancamento_use_case, mock_consolidado_repo):
    mock_consolidado_repo.atualizar_consolidado.side_effect = Exception("Repository error")
    
    event_data = {
        "id": "123",
        "data": "2023-01-01",
        "valor": 50.0,
        "tipo": "CREDITO",
        "descricao": "Teste"
    }
    
    result = await processar_lancamento_use_case.execute(event_data)
    
    assert result["status"] == "error"
    assert "message" in result
    assert "Repository error" in result["message"]
    assert "event_data" in result

@pytest.mark.asyncio
async def test_execute_cache_error(processar_lancamento_use_case, mock_cache_handler):
    mock_cache_handler.set.side_effect = Exception("Cache error")
    
    event_data = {
        "id": "123",
        "data": "2023-01-01",
        "valor": 50.0,
        "tipo": "CREDITO",
        "descricao": "Teste"
    }
    
    result = await processar_lancamento_use_case.execute(event_data)
    
    assert result["status"] == "error"
    assert "message" in result
    assert "Cache error" in result["message"]
    assert "event_data" in result