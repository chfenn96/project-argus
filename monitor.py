import boto3
import requests
import time
from datetime import datetime

# A list of websites to monitor
URLS_TO_MONITOR = [
    "https://www.google.com",
    "https://www.github.com",
    "https://this-website-is-fake-and-will-fail.com",  # Included to test failure handling!
]


def check_uptime(url):
    """
    Pings a URL and returns a dictionary with the status, response time, and timestamp.
    """
    result = {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "DOWN",
        "response_time_ms": 0,
        "status_code": None,
    }

    try:
        # Start the timer
        start_time = time.time()

        # Make the request with a 5-second timeout
        response = requests.get(url, timeout=5)

        # Calculate how long it took in milliseconds
        end_time = time.time()
        result["response_time_ms"] = round((end_time - start_time) * 1000)

        # Record the status code (e.g., 200 for OK, 404 for Not Found)
        result["status_code"] = response.status_code

        # If the status code is 200-299, we consider it UP
        if response.ok:
            result["status"] = "UP"

    except requests.exceptions.RequestException as e:
        # If there's a timeout, DNS failure, etc., it will fall here and remain "DOWN"
        print(f"Error checking {url}: {e}")

    return result


def lambda_handler(event, context):
    """
    AWS Lambda calls this function when it starts.
    'event' contains the trigger data (we'll use this later).
    'context' contains info about the runtime.
    """
    print("Lambda handler started...")

    # Initialize the database connection
    db = boto3.resource("dynamodb")
    table = db.Table("ArgusMetrics")

    results = []
    for url in URLS_TO_MONITOR:
        metrics = check_uptime(url)

        # New Step: Save to database
        print(f"Saving results for {url} to DynamoDB...")
        table.put_item(Item=metrics)
        results.append(metrics)

    # Returning this tells Lambda "I'm done and I succeeded"
    return {"statusCode": 200, "body": results}


# CRITICAL: Do NOT call main() or lambda_handler() down here!
# To test locally, use:
# if __name__ == "__main__":
#     lambda_handler(None, None)
