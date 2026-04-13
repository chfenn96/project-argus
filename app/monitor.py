import asyncio
import httpx
import boto3
import json
import time
import os
from datetime import datetime

# --- OPENTELEMETRY IMPORTS ---
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource  # Removed RESOURCE_ATTRIBUTES
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor # Instant export for testing
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

# 1. Setup OTel with a simplified Resource definition
resource = Resource(attributes={
    "service.name": "project-argus-monitor"
})
provider = TracerProvider(resource=resource)

## Point to the central Jaeger collector in the istio-system namespace
processor = SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger-collector.istio-system.svc.cluster.local:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Auto-instrument all httpx clients
HTTPXClientInstrumentor().instrument()

# --- CONFIGURATION ---
URLS_ENV = os.getenv("URLS_TO_MONITOR", "https://www.google.com,https://www.github.com,https://www.wikipedia.org")
URLS_TO_MONITOR = [url.strip() for url in URLS_ENV.split(",")]
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")


async def check_uptime(client, url, retries=3):
    """Pings a URL with browser headers and retry logic."""
    with tracer.start_as_current_span(f"ping_{url}") as span:
        result = {
            "url": url,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "DOWN",
            "response_time_ms": 0,
            "status_code": None,
        }
        headers = {"User-Agent": "ArgusMonitor/v2.2.0 (SRE Portfolio Project)"}

        for attempt in range(retries):
            try:
                start_time = time.time()
                response = await client.get(url, timeout=5.0, headers=headers, follow_redirects=True)
                
                result["response_time_ms"] = round((time.time() - start_time) * 1000)
                result["status_code"] = response.status_code
                
                # Add metadata to the trace span
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("argus.attempt", attempt + 1)

                if 200 <= response.status_code < 300:
                    result["status"] = "UP"
                    return result

            except Exception as e:
                span.record_exception(e)
                if attempt < retries - 1:
                    await asyncio.sleep(0.1 * (2**attempt))
        return result


async def run_monitor():
    """Core logic: Pings sites, saves to DB, and sends alerts."""
    # Explicitly set region for all clients
    with tracer.start_as_current_span("run_monitor_loop"):
        db = boto3.resource("dynamodb", region_name=AWS_REGION)
        table = db.Table("ArgusMetrics")
        sns = boto3.client("sns", region_name=AWS_REGION)

        async with httpx.AsyncClient() as client:
            tasks = [check_uptime(client, url) for url in URLS_TO_MONITOR]
            results = await asyncio.gather(*tasks)

            for metrics in results:
                print(json.dumps(metrics))
                # Span for Database interaction
                with tracer.start_as_current_span("dynamodb_save"):
                    try:
                        table.put_item(Item=metrics)
                    except Exception as e:
                        print(f"❌ DB SAVE FAILURE: {e}")

            failures = [r["url"] for r in results if r["status"] == "DOWN"]
            if failures and SNS_TOPIC_ARN:
                with tracer.start_as_current_span("sns_alert"):
                    message = f"Project Argus detected outages:\n\n- " + "\n- ".join(failures)
                    sns.publish(TopicArn=SNS_TOPIC_ARN, Subject="⚠️ Argus Alert", Message=message)

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
