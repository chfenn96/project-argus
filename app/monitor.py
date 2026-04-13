import asyncio
import httpx
import boto3
import json
import time
import os
import logging
from datetime import datetime

# --- OPENTELEMETRY IMPORTS ---
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

# --- GLOBAL CONFIGURATION ---
# Use constants for defaults, but allow environment overrides
URLS_TO_MONITOR = [
    url.strip()
    for url in os.getenv(
        "URLS_TO_MONITOR",
        "https://www.google.com,https://www.github.com,https://www.wikipedia.org",
    ).split(",")
]
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")
# Detection for CI/CD or Local environments to prevent telemetry hangs
IS_TEST_ENV = any(
    os.getenv(env) for env in ["PYTEST_CURRENT_TEST", "ARGUS_LOCAL", "GITHUB_ACTIONS"]
)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("project-argus")


def get_tracer():
    """
    Lazy-initializes Telemetry.
    Senior SRE Note: Encapsulating this prevents the 98s hang in GitHub Actions
    because we don't try to connect to a collector during 'import monitor'.
    """
    if IS_TEST_ENV:
        # Return a no-op tracer in test/local environments
        return trace.get_tracer(__name__)

    try:
        resource = Resource(attributes={"service.name": "project-argus-monitor"})
        provider = TracerProvider(resource=resource)

        # SimpleSpanProcessor sends spans immediately (best for CronJobs/Lambda)
        exporter = OTLPSpanExporter(
            endpoint="http://jaeger-collector.istio-system.svc.cluster.local:4317",
            insecure=True,
        )
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        trace.set_tracer_provider(provider)

        # Instrument HTTPX automatically
        HTTPXClientInstrumentor().instrument()
        return trace.get_tracer(__name__)
    except Exception as e:
        logger.warning(f"Telemetry failed to initialize: {e}. Falling back to default.")
        return trace.get_tracer(__name__)


# Single instance of tracer
tracer = get_tracer()


async def check_uptime(client: httpx.AsyncClient, url: str, retries: int = 3):
    """
    Core ping logic with retry and exponential backoff.
    Wrapped in an OTel span with rich metadata for Jaeger.
    """
    with tracer.start_as_current_span(f"ping_{url}") as span:
        headers = {"User-Agent": "ArgusMonitor/v2.3.4 (SRE Portfolio Project)"}

        for attempt in range(retries):
            try:
                start_time = time.time()
                # Timeout matches our Chaos Mesh experiment (5s)
                response = await client.get(
                    url, timeout=5.0, headers=headers, follow_redirects=True
                )
                latency = round((time.time() - start_time) * 1000)

                # Metadata for Distributed Tracing
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.url", url)
                span.set_attribute("argus.latency_ms", latency)
                span.set_attribute("argus.attempt", attempt + 1)

                if 200 <= response.status_code < 300:
                    return {
                        "url": url,
                        "status": "UP",
                        "status_code": response.status_code,
                        "response_time_ms": latency,
                        "timestamp": datetime.utcnow().isoformat(),
                    }

                logger.warning(
                    f"Attempt {attempt+1}: {url} returned {response.status_code}"
                )

            except Exception as e:
                span.record_exception(e)
                logger.error(
                    f"Attempt {attempt+1}: Connection failed for {url}: {str(e)}"
                )
                if attempt < retries - 1:
                    await asyncio.sleep(0.1 * (2**attempt))

        return {
            "url": url,
            "status": "DOWN",
            "status_code": 0,
            "response_time_ms": 0,
            "timestamp": datetime.utcnow().isoformat(),
        }


async def run_monitor():
    """
    Main orchestration loop.
    Handles AWS client lifecycle and concurrency.
    """
    with tracer.start_as_current_span("run_monitor_loop"):
        db = boto3.resource("dynamodb", region_name=AWS_REGION)
        table = db.Table("ArgusMetrics")
        sns = boto3.client("sns", region_name=AWS_REGION)

        async with httpx.AsyncClient() as client:
            tasks = [check_uptime(client, url) for url in URLS_TO_MONITOR]
            results = await asyncio.gather(*tasks)

            for metrics in results:
                # Log JSON for CloudWatch Metric Filters
                print(json.dumps(metrics))

                with tracer.start_as_current_span("dynamodb_save"):
                    try:
                        table.put_item(Item=metrics)
                    except Exception as e:
                        logger.error(f"DynamoDB Failure: {e}")

            # Alerting Logic
            failures = [r["url"] for r in results if r["status"] == "DOWN"]
            if failures and SNS_TOPIC_ARN:
                with tracer.start_as_current_span("sns_alert"):
                    failure_msg = "\n- ".join(failures)
                    message = f"Argus Alert: Multiple outages detected!\n\nFailed Sites:\n- {failure_msg}"
                    try:
                        sns.publish(
                            TopicArn=SNS_TOPIC_ARN,
                            Subject="⚠️ Argus Outage Report",
                            Message=message,
                        )
                    except Exception as e:
                        logger.error(f"SNS Failure: {e}")

    return results


def lambda_handler(event, context):
    """Entry point for AWS Lambda."""
    return {"statusCode": 200, "body": asyncio.run(run_monitor())}


if __name__ == "__main__":
    # Local execution entry point
    asyncio.run(run_monitor())
