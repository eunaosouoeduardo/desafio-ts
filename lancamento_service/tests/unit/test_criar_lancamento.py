import pytest
from unittest.mock import Mock
from datetime import date

from src.use_cases.criar_lancamento import CriarLancamentoUseCase
from src.entities.lancamento import Lancamento


@pytest.fixture
def mock_dependencies():
    mock_repo = Mock()
    mock_cache = Mock()
    mock_publisher = Mock()

    use_case = CriarLancamentoUseCase(
        repository=mock_repo,
        cache=mock_cache,
        message_publisher=mock_publisher
    )

    valid_data = Lancamento(
        valor=100.0,
        tipo="CREDITO",
        descricao="Teste",
        data=date(2025, 7, 13)
    )

    # Simula retorno do método criar()
    mock_repo.criar.return_value = Lancamento(
        id=1,
        valor=valid_data.valor,
        tipo=valid_data.tipo,
        descricao=valid_data.descricao,
        data=valid_data.data
    )

    return use_case, mock_repo, mock_cache, mock_publisher, valid_data


def test_deve_criar_lancamento_com_dados_validos(mock_dependencies):
    use_case, mock_repo, mock_cache, mock_publisher, valid_data = mock_dependencies

    lancamento = use_case.execute(valid_data)

    mock_repo.criar.assert_called_once()
    mock_cache.invalidate.assert_called_once_with("consolidado:2025-07-13")
    mock_publisher.publish.assert_called_once()
    assert lancamento.valor == 100.0


def test_deve_lancar_erro_para_valor_invalido(mock_dependencies):
    use_case, mock_repo, mock_cache, mock_publisher, valid_data = mock_dependencies
    valid_data.valor = 0

    with pytest.raises(ValueError, match="Valor deve ser positivo"):
        use_case.execute(valid_data)

    mock_repo.criar.assert_not_called()
    mock_cache.invalidate.assert_not_called()
    mock_publisher.publish.assert_not_called()


def test_deve_continuar_mesmo_se_cache_falhar(mock_dependencies):
    use_case, mock_repo, mock_cache, mock_publisher, valid_data = mock_dependencies
    mock_cache.invalidate.side_effect = Exception("Erro no Redis")

    lancamento = use_case.execute(valid_data)

    mock_repo.criar.assert_called_once()
    mock_publisher.publish.assert_called_once()
    assert lancamento.valor == 100.0


def test_deve_continuar_mesmo_se_publish_falhar(mock_dependencies):
    use_case, mock_repo, mock_cache, mock_publisher, valid_data = mock_dependencies
    mock_publisher.publish.side_effect = Exception("Erro no RabbitMQ")

    lancamento = use_case.execute(valid_data)

    mock_repo.criar.assert_called_once()
    mock_cache.invalidate.assert_called_once()
    assert lancamento.valor == 100.0
