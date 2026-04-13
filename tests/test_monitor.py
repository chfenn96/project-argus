import pytest
import respx
import httpx
import os
from unittest.mock import MagicMock, patch
from app.monitor import check_uptime, run_monitor

# Set this to tell our app code to skip the heavy Jaeger export
os.environ["ARGUS_LOCAL"] = "true"


@pytest.mark.asyncio
@respx.mock
# Patch the tracer so it doesn't try to export to Jaeger during tests
@patch("app.monitor.tracer")
async def test_check_uptime_success(mock_tracer):
    url = "https://google.com"
    respx.get(url).mock(return_value=httpx.Response(200))
    async with httpx.AsyncClient() as client:
        result = await check_uptime(client, url)
    assert result["status"] == "UP"


@pytest.mark.asyncio
@respx.mock
@patch("app.monitor.tracer")
async def test_check_uptime_retry_logic(mock_tracer):
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
# Patch boto3.resource AND boto3.client directly in the monitor module
@patch("app.monitor.boto3.resource")
@patch("app.monitor.boto3.client")
async def test_run_monitor_db_and_sns(mock_sns_factory, mock_db_factory):
    # 1. Setup Mock DynamoDB Table
    mock_table = MagicMock()
    mock_db_factory.return_value.Table.return_value = mock_table

    # 2. Setup Mock SNS Client
    mock_sns_client = MagicMock()
    mock_sns_factory.return_value = mock_sns_client

    # 3. Use respx to mock the URLs run_monitor pings
    with respx.mock:
        # Mock every URL in your default list
        respx.get("https://www.google.com").mock(return_value=httpx.Response(200))
        respx.get("https://www.github.com").mock(return_value=httpx.Response(200))
        respx.get("https://www.wikipedia.org").mock(return_value=httpx.Response(200))

        # 4. Run the function
        await run_monitor()

    # 5. Verify the DB was called
    assert mock_table.put_item.called
    # Optional: Verify SNS WAS NOT called (since sites are UP)
    assert not mock_sns_client.publish.called
