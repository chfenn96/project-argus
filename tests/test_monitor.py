import pytest
import respx
import httpx
from unittest.mock import MagicMock, patch
from app.monitor import check_uptime, run_monitor


@pytest.mark.asyncio
@respx.mock
@patch("app.monitor.tracer")
async def test_check_uptime_success(mock_tracer):
    url = "https://google.com"
    respx.get(url).mock(return_value=httpx.Response(200))
    async with httpx.AsyncClient() as client:
        result = await check_uptime(client, url)

    assert result["status"] == "UP"
    assert result["status_code"] == 200
    assert "response_time_ms" in result
    assert "timestamp" in result


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
@patch("app.monitor.boto3.resource")
@patch("app.monitor.boto3.client")
async def test_run_monitor_db_save(mock_sns_factory, mock_db_factory):
    """Verifies that results are saved to DynamoDB on a normal run."""
    mock_table = MagicMock()
    mock_db_factory.return_value.Table.return_value = mock_table

    with respx.mock:
        # Mock all URLs to return 200
        respx.get(url__regex=r"https://.*").mock(return_value=httpx.Response(200))
        await run_monitor()

    assert mock_table.put_item.called


@pytest.mark.asyncio
@patch("app.monitor.boto3.resource")
@patch("app.monitor.boto3.client")
@patch("app.monitor.SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789:ArgusAlerts")
async def test_run_monitor_failure_triggers_sns(mock_sns_factory, mock_db_factory):
    """
    CRITICAL TEST: Verifies that if a site is DOWN, an SNS alert is published.
    This is the core business value of Project Argus.
    """
    # Setup Mocks
    mock_sns_client = MagicMock()
    mock_sns_factory.return_value = mock_sns_client
    mock_db_factory.return_value.Table.return_value = MagicMock()

    with respx.mock:
        # Simulate Google being UP but GitHub being DOWN (500 error)
        respx.get("https://www.google.com").mock(return_value=httpx.Response(200))
        respx.get("https://www.github.com").mock(return_value=httpx.Response(500))
        respx.get("https://www.wikipedia.org").mock(return_value=httpx.Response(200))

        await run_monitor()

    # VERIFICATION: SNS publish should have been called because GitHub failed
    assert mock_sns_client.publish.called

    # Check that the message contains the failed URL
    call_args = mock_sns_client.publish.call_args
    assert "https://www.github.com" in call_args.kwargs["Message"]
    assert "⚠️ Argus Outage Report" in call_args.kwargs["Subject"]
