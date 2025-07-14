import pytest
from datetime import date
from pydantic import ValidationError
from src.entities.lancamento import Lancamento 

def test_lancamento_valido():
    lanc = Lancamento(
        valor=100.0,
        tipo="CREDITO",
        descricao="Pagamento recebido",
        data=date(2025, 7, 14)
    )
    assert lanc.valor == 100.0
    assert lanc.tipo == "CREDITO"
    assert lanc.descricao == "Pagamento recebido"
    assert lanc.data == date(2025, 7, 14)
    assert lanc.id is None

def test_valor_negativo_gera_erro():
    with pytest.raises(ValidationError):
        Lancamento(
            valor=-50.0,
            tipo="DEBITO",
            descricao="Pagamento",
            data=date(2025, 7, 14)
        )

def test_tipo_invalido_gera_erro():
    with pytest.raises(ValidationError):
        Lancamento(
            valor=50.0,
            tipo="OUTRO",  # Tipo inválido
            descricao="Pagamento",
            data=date(2025, 7, 14)
        )

def test_campos_obrigatorios_faltando():
    with pytest.raises(ValidationError):
        Lancamento(
            valor=50.0,
            tipo="CREDITO",
            # descricao faltando
            data=date(2025, 7, 14)
        )
