import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.rabbitmq_publisher import RabbitMQPublisher


@pytest.fixture
def mock_pika():
    with patch("src.infrastructure.rabbitmq_publisher.pika.BlockingConnection") as mock_conn:
        yield mock_conn


def test_publish_success(mock_pika):
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_pika.return_value = mock_connection

    publisher = RabbitMQPublisher()
    message = {"id": 123, "valor": 100.0}

    result = publisher.publish("lancamento_criado", message)

    assert result is True
    assert mock_pika.call_count == 2  # chamada na __init__ e no publish
    assert mock_channel.basic_publish.called
    assert mock_connection.close.called
