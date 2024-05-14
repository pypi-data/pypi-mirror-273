import pytest

# from tenacity import retry
from src.uc_tools import retry


async def test_retry_successful_execution():
    async def mock_coroutine(*args, **kwargs):
        return 42

    decorated_func = retry()(mock_coroutine)
    result = await decorated_func()
    assert result == 42


async def test_retry_max_retries_reached():
    async def mock_coroutine(*args, **kwargs):
        msg = 'Something went wrong'
        raise ValueError(msg)

    decorated_func = retry(max_retries=1, max_delay=0.1)(mock_coroutine)
    with pytest.raises(ValueError):
        await decorated_func()
