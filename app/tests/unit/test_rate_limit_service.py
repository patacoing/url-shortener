from unittest.mock import Mock
import pytest

from app.service.rate_limit_service import RateLimitService


@pytest.fixture
def rate_limit_service():
    return RateLimitService(
        host="localhost",
        database=Mock()
    )


@pytest.mark.parametrize(
    "count, expected",
    [
        (0, False),
        (1, False),
        (2, True)
    ]
)
def test_is_count_above_limit(count, expected):
    RateLimitService.limit = 1
    assert RateLimitService.is_count_above_limit(count) is expected


def test_increase_client_call_count(rate_limit_service):
    rate_limit_service.database.get_call_count.return_value = 1

    new_count = rate_limit_service.increase_client_call_count()

    assert new_count == 2
    rate_limit_service.database.increase_call_count.assert_called_once
    rate_limit_service.database.get_call_count.assert_called_once


def test_is_client_above_limit(rate_limit_service):
    rate_limit_service.database.get_call_count.return_value = 1
    RateLimitService.is_count_above_limit = Mock(return_value=True)

    is_above = rate_limit_service.is_client_above_limit()

    assert is_above == True
    rate_limit_service.database.get_call_count.assert_called_once
    RateLimitService.is_count_above_limit.assert_called_once_with(1)