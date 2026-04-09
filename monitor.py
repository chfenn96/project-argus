import asyncio
import httpx
import boto3
import time
import os
from datetime import datetime

# FIX: Get URLs from Environment Variables (No more hardcoding!)
URLS_ENV = os.getenv("URLS_TO_MONITOR", "https://www.google.com")
URLS_TO_MONITOR = [url.strip() for url in URLS_ENV.split(",")]

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")


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

    # ADD THIS LINE: Define a realistic User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for attempt in range(retries):
        try:
            start_time = time.time()
            # Asynchronous GET request
            response = await client.get(
                url, timeout=5.0, headers=headers, follow_redirects=True
            )
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
    sns = boto3.client('sns') # Initialized as you drafted

    async with httpx.AsyncClient() as client:
        tasks = [check_uptime(client, url) for url in URLS_TO_MONITOR]
        results = await asyncio.gather(*tasks)

        # 1. Save results to DynamoDB (Your existing working logic)
        for metrics in results:
            try:
                table.put_item(Item=metrics)
                print(f"✅ DB SAVE SUCCESS: {metrics['url']}")
            except Exception as e:
                print(f"❌ DB SAVE FAILURE: {metrics['url']} - Error: {e}")

        # 2. ALERTING LOGIC: Check for failures
        # We use a list comprehension to find any URLs that are marked "DOWN"
        failures = [r['url'] for r in results if r['status'] == "DOWN"]

        # Only send the email if the failures list is NOT empty
        if failures and SNS_TOPIC_ARN:
            print(f"🚨 Found {len(failures)} failures. Sending SNS Alert...")
            
            # Format a clean message for the email
            failure_list = "\n- ".join(failures)
            message = (
                f"Project Argus has detected that the following sites are DOWN:\n\n"
                f"- {failure_list}\n\n"
                f"Timestamp: {datetime.utcnow().isoformat()} UTC"
            )

            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="⚠️ CRITICAL: Project Argus Uptime Alert",
                    Message=message
                )
                print("📧 SNS Alert sent successfully.")
            except Exception as e:
                print(f"❌ FAILED to send SNS alert: {e}")

    return results


async def lambda_handler(event, context):
    """
    AWS Lambda natively supports 'async def'.
    Removing asyncio.run() prevents loop conflicts during testing and
    follows AWS best practices for async runtimes.
    """
    print("Lambda handler started...")

    # Just 'await' the coroutine directly
    results = await run_monitor()

    return {"statusCode": 200, "body": results}


if __name__ == "__main__":
    print("Running in Standalone Mode (Kubernetes/Docker)...")
    try:
        # This triggers the actual logic when NOT in Lambda
        asyncio.run(run_monitor())
        print("Monitoring cycle complete.")
    except Exception as e:
        print(f"Standalone execution failed: {e}")
