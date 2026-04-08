import pytest
import respx
import httpx
from monitor import check_uptime
from unittest.mock import MagicMock, patch


# 1. Tell pytest this file contains async tests
@pytest.mark.asyncio
@respx.mock  # 2. Use respx to intercept httpx calls
async def test_check_uptime_success():
    url = "https://google.com"
    # Mock a successful 200 OK response
    respx.get(url).mock(return_value=httpx.Response(200))

    async with httpx.AsyncClient() as client:
        result = await check_uptime(client, url)

    assert result["status"] == "UP"
    assert result["status_code"] == 200
    assert result["url"] == url


@pytest.mark.asyncio
@respx.mock
async def test_check_uptime_retry_logic():
    """
    Verify that the script actually retries on failure.
    We mock 2 failures followed by 1 success.
    """
    url = "https://github.com"
    # Create a route that fails twice then succeeds
    route = respx.get(url)
    route.side_effect = [
        httpx.ConnectError("Failing 1"),
        httpx.ConnectError("Failing 2"),
        httpx.Response(200),
    ]

    async with httpx.AsyncClient() as client:
        result = await check_uptime(client, url)

    assert result["status"] == "UP"
    # Verify the route was called exactly 3 times
    assert route.call_count == 3


@pytest.mark.asyncio
@patch("monitor.boto3.resource")
async def test_lambda_handler_db_call(mock_boto):
    from monitor import lambda_handler

    mock_table = MagicMock()
    mock_boto.return_value.Table.return_value = mock_table

    with respx.mock:
        # Mock the specific URLs you are testing
        respx.get("https://www.google.com").mock(return_value=httpx.Response(200))
        respx.get("https://www.github.com").mock(return_value=httpx.Response(200))
        respx.get("https://www.wikipedia.org").mock(return_value=httpx.Response(200))

        # Now we can safely await the handler
        await lambda_handler({}, None)

    assert mock_table.put_item.called
