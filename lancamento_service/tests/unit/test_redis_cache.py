import pytest
from unittest.mock import MagicMock, patch

from src.infrastructure.redis_cache import RedisCacheHandler


@pytest.fixture
def mock_redis():
    with patch("src.infrastructure.redis_cache.redis_client") as mock_client:
        yield mock_client


def test_set_and_get_cache(mock_redis):
    # Arrange
    handler = RedisCacheHandler()
    mock_redis.set.return_value = True
    mock_redis.get.return_value = b'{"foo": "bar"}'

    # Act
    result_set = handler.set("mykey", {"foo": "bar"})
    result_get = handler.get("mykey")

    # Assert
    assert result_set is True
    assert result_get == {"foo": "bar"}
    mock_redis.set.assert_called_once()
    mock_redis.get.assert_called_once_with("mykey")


def test_set_with_ttl(mock_redis):
    handler = RedisCacheHandler()
    mock_redis.setex.return_value = True

    result = handler.set("mykey", {"foo": "bar"}, ttl=60)

    assert result is True
    mock_redis.setex.assert_called_once_with("mykey", 60, '{"foo": "bar"}')


def test_invalidate_key(mock_redis):
    handler = RedisCacheHandler()
    mock_redis.delete.return_value = 1

    result = handler.invalidate("mykey")

    assert result is True
    mock_redis.delete.assert_called_once_with("mykey")


def test_get_nonexistent_key(mock_redis):
    handler = RedisCacheHandler()
    mock_redis.get.return_value = None

    result = handler.get("missingkey")

    assert result is None
    mock_redis.get.assert_called_once_with("missingkey")
