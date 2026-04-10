import asyncio
import httpx
import boto3
import json
import time
import os
from datetime import datetime

# 1. Configuration from environment
URLS_ENV = os.getenv(
    "URLS_TO_MONITOR",
    "https://www.google.com,https://www.github.com,https://www.wikipedia.org",
)
URLS_TO_MONITOR = [url.strip() for url in URLS_ENV.split(",")]
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")  # Re-added for alerting


async def check_uptime(client, url, retries=3):
    """Pings a URL with browser headers and retry logic."""
    result = {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "DOWN",
        "response_time_ms": 0,
        "status_code": None,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for attempt in range(retries):
        try:
            start_time = time.time()
            response = await client.get(
                url, timeout=5.0, headers=headers, follow_redirects=True
            )

            result["response_time_ms"] = round((time.time() - start_time) * 1000)
            result["status_code"] = response.status_code

            if 200 <= response.status_code < 300:
                result["status"] = "UP"
                return result

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                # Exponential backoff: 0.1s, 0.2s, 0.4s...
                await asyncio.sleep(0.1 * (2**attempt))

    return result


async def run_monitor():
    """Core logic: Pings sites, saves to DB, and sends alerts."""
    # Explicitly set region for all clients
    db = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = db.Table("ArgusMetrics")
    sns = boto3.client("sns", region_name=AWS_REGION)

    async with httpx.AsyncClient() as client:
        tasks = [check_uptime(client, url) for url in URLS_TO_MONITOR]
        results = await asyncio.gather(*tasks)

        for metrics in results:
            # CRITICAL: json.dumps ensures double quotes for CloudWatch Filters
            print(json.dumps(metrics))
            try:
                table.put_item(Item=metrics)
            except Exception as e:
                print(f"❌ DB SAVE FAILURE: {e}")

        # --- RE-ADDED ALERTING LOGIC ---
        failures = [r["url"] for r in results if r["status"] == "DOWN"]
        if failures and SNS_TOPIC_ARN:
            print(f"🚨 Found {len(failures)} failures. Sending SNS Alert...")
            failure_list = "\n- ".join(failures)
            message = f"Project Argus detected outages:\n\n- {failure_list}\n\nTimestamp: {datetime.utcnow().isoformat()}"
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN, Subject="⚠️ Argus Alert", Message=message
                )
                print("📧 Alert sent.")
            except Exception as e:
                print(f"❌ SNS FAILURE: {e}")
        # -------------------------------

    return results


def lambda_handler(event, context):
    """AWS Lambda entry point: Standard sync wrapper for async work."""
    print("Lambda handler started...")
    # This executes the async work and WAITS for the real list result
    output = asyncio.run(run_monitor())

    return {"statusCode": 200, "body": output}


if __name__ == "__main__":
    print("Running local verification...")
    final_output = lambda_handler(None, None)
    print("\n--- FINAL OUTPUT TO AWS ---")
    print(json.dumps(final_output, indent=2))
