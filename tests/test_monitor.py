import pytest
import respx
import httpx
from unittest.mock import MagicMock, patch

# UPDATED: Import from the 'app' package
from app.monitor import check_uptime, run_monitor


@pytest.mark.asyncio
@respx.mock
async def test_check_uptime_success():
    url = "https://google.com"
    respx.get(url).mock(return_value=httpx.Response(200))
    async with httpx.AsyncClient() as client:
        result = await check_uptime(client, url)
    assert result["status"] == "UP"


@pytest.mark.asyncio
@respx.mock
async def test_check_uptime_retry_logic():
    url = "https://github.com"
    route = respx.get(url)
    # Simulate 2 failures and then a success
    route.side_effect = [
        httpx.ConnectError("Failing 1"),
        httpx.ConnectError("Failing 2"),
        httpx.Response(200),
    ]
    async with httpx.AsyncClient() as client:
        result = await check_uptime(client, url)

    assert result["status"] == "UP"
    assert route.call_count == 3


@pytest.mark.asyncio
# UPDATED: The patch target must match the new package path
@patch("app.monitor.boto3.resource")
@patch("app.monitor.boto3.client")
async def test_run_monitor_db_and_sns(mock_sns_client, mock_db_resource):
    # Mock DynamoDB
    mock_table = MagicMock()
    mock_db_resource.return_value.Table.return_value = mock_table

    # Mock SNS
    mock_sns = MagicMock()
    mock_sns_client.return_value = mock_sns

    with respx.mock:
        # Mock all URLs in your env
        respx.get("https://www.google.com").mock(return_value=httpx.Response(200))
        respx.get("https://www.github.com").mock(return_value=httpx.Response(200))
        respx.get("https://www.wikipedia.org").mock(return_value=httpx.Response(200))

        # We test run_monitor() directly to avoid the asyncio.run() loop conflict
        await run_monitor()

    assert mock_table.put_item.called
