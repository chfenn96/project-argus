import asyncio
import httpx
import boto3
import time
import os
from datetime import datetime

# FIX: Get URLs from Environment Variables (No more hardcoding!)
URLS_ENV = os.getenv("URLS_TO_MONITOR", "https://www.google.com")
URLS_TO_MONITOR = [url.strip() for url in URLS_ENV.split(",")]


async def check_uptime(client, url, retries=3):
    """
    Pings a URL asynchronously with retry logic.
    """
    result = {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "DOWN",
        "response_time_ms": 0,
        "status_code": None,
    }

    for attempt in range(retries):
        try:
            start_time = time.time()
            # Asynchronous GET request
            response = await client.get(url, timeout=5.0)
            end_time = time.time()

            result["response_time_ms"] = round((end_time - start_time) * 1000)
            result["status_code"] = response.status_code

            if response.status_code >= 200 and response.status_code < 300:
                result["status"] = "UP"
                return result  # Success!

        except Exception as e:
            if attempt == retries - 1:
                print(f"Final failure for {url}: {e}")
            else:
                # Exponential backoff (wait longer each time)
                await asyncio.sleep(2**attempt)

    return result


async def run_monitor():
    db = boto3.resource("dynamodb", region_name="us-east-1")
    table = db.Table("ArgusMetrics")

    # Use a single client session for all pings
    async with httpx.AsyncClient() as client:
        # Create a list of tasks (one for each URL)
        tasks = [check_uptime(client, url) for url in URLS_TO_MONITOR]

        # MAGIC: Run all pings simultaneously
        results = await asyncio.gather(*tasks)

        # Save results to DynamoDB
        for metrics in results:
            print(f"Saving {metrics['url']} - {metrics['status']}")
            table.put_item(Item=metrics)

    return results


def lambda_handler(event, context):
    # Entry point for AWS Lambda
    return {"statusCode": 200, "body": asyncio.run(run_monitor())}
