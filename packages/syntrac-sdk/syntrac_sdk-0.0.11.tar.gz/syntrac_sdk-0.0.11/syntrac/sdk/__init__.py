import os
import sys

from typing import Optional, Set
from colorama import Fore
from opentelemetry import trace
from opentelemetry.sdk.trace import SpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.sdk.metrics.export import MetricExporter
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.propagators.textmap import TextMapPropagator
from opentelemetry.util.re import parse_env_headers
from syntrac_opentelemetry.semconv.ai import SpanAttributes

from syntrac.sdk.metrics.metrics import MetricsWrapper
from syntrac.sdk.telemetry import Telemetry
from syntrac.sdk.instruments import Instruments
from syntrac.sdk.config import (
    is_content_tracing_enabled,
    is_tracing_enabled,
    is_metrics_enabled,
)
from syntrac.sdk.fetcher import Fetcher
from syntrac.sdk.tracing.tracing import (
    TracerWrapper,
)
from syntrac.sdk.tracing.context import (
    set_association_properties,
)
from typing import Dict


class Syntrac:
    __tracer_wrapper: TracerWrapper
    __fetcher: Fetcher

    @staticmethod
    def init(
        app_name: Optional[str] = sys.argv[0],
        api_endpoint: str = "https://analytics-api.syntrac.dev",
        api_key: Optional[str] = None,
        headers: Dict[str, str] = {},
        disable_batch=False,
        exporter: Optional[SpanExporter] = None,
        metrics_exporter: Optional[MetricExporter] = None,
        metrics_headers: Dict[str, str] = {},
        processor: Optional[SpanProcessor] = None,
        propagator: Optional[TextMapPropagator] = None,
        syntrac_sync_enabled: bool = True,
        resource_attributes: dict = {},
        instruments: Optional[Set[Instruments]] = None,
        create_new_provider: bool = False
    ) -> None:
        Telemetry()

        api_endpoint = os.getenv("SYNTRAC_BASE_URL") or api_endpoint
        api_key = os.getenv("SYNTRAC_API_KEY") or api_key

        if (
            syntrac_sync_enabled
            and api_key
            and not exporter
            and not processor
        ):
            Syntrac.__fetcher = Fetcher(base_url=api_endpoint, api_key=api_key)

        if not is_tracing_enabled():
            print(Fore.YELLOW + "Tracing is disabled" + Fore.RESET)
            return

        enable_content_tracing = is_content_tracing_enabled()

        if exporter or processor:
            print(Fore.GREEN + "Syntrac exporting traces to a custom exporter")

        headers = os.getenv("SYNTRAC_HEADERS") or headers

        if isinstance(headers, str):
            headers = parse_env_headers(headers)

        if not exporter and not processor and headers:
            print(
                Fore.GREEN
                + f"Syntrac exporting traces to {api_endpoint}, authenticating with custom headers"
            )

        if api_key and not exporter and not processor and not headers:
            print(
                Fore.GREEN
                + f"Syntrac exporting traces to {api_endpoint} authenticating with bearer token"
            )
            headers = {
                "Authorization": f"Bearer {api_key}",
            }

        print(Fore.RESET)

        # Tracer init
        resource_attributes.update({SERVICE_NAME: app_name})
        TracerWrapper.set_static_params(
            resource_attributes, enable_content_tracing, api_endpoint, headers
        )
        Syntrac.__tracer_wrapper = TracerWrapper(
            disable_batch=disable_batch,
            processor=processor,
            propagator=propagator,
            exporter=exporter,
            instruments=instruments,
            create_new_provider=create_new_provider,
        )

        # Metrics init: disabled for Syntrac as we don't have a metrics endpoint (yet)
        if api_endpoint.find("syntrac.dev") != -1 or not is_metrics_enabled():
            if not is_metrics_enabled():
                print(Fore.YELLOW + "OpenTelemetry metrics are disabled" + Fore.RESET)
            return

        if metrics_exporter:
            print(Fore.GREEN + "Syntrac exporting metrics to a custom exporter")

        metrics_endpoint = os.getenv("SYNTRAC_METRICS_ENDPOINT")
        metrics_headers = os.getenv("SYNTRAC_METRICS_HEADERS") or metrics_headers

        MetricsWrapper.set_static_params(
            resource_attributes, metrics_endpoint, metrics_headers
        )
        Syntrac.__metrics_wrapper = MetricsWrapper(exporter=metrics_exporter)

    @staticmethod
    def set_association_properties(properties: dict) -> None:
        set_association_properties(properties)

    @staticmethod
    def report_score(
        id: Optional[str],
        score: float,
    ):
        """Apply score to all llm steps belongs to action
        id: action_id or unique id linked by associate_trace method
        """
        if not Syntrac.__fetcher:
            print(
                Fore.RED
                + "Error: Cannot report score. Missing Syntrac API key,"
                + " go to https://app.syntrac.com/settings/api-keys to create one"
            )
            print("Set the SYNTRAC_API_KEY environment variable to the key")
            print(Fore.RESET)
            return

        Syntrac.__fetcher.patch(
            f"actions/{id}/score",
            {
                "score": score,
            },
        )

    @staticmethod
    def associate_trace(id: str, span_id: Optional[str]):
        """Associate trace and space with a unique id
        id: unique id linked with trace
        span_id: unique id linked with span
        """
        span = trace.get_current_span()
        span.set_attribute(
          f"{SpanAttributes.SYNTRAC_ASSOCIATION_PROPERTIES}.trace_alias",
          id
        )
        if span_id:
            span.set_attribute(
              f"{SpanAttributes.SYNTRAC_ASSOCIATION_PROPERTIES}.span_alias",
              span_id
            )

    @staticmethod
    def update_span(id: str, body: Dict[str, str]):
        """Update span value with data if processed asynchronously
        id: span_id or unique id linked with span
        """
        if not Syntrac.__fetcher:
            print(
                Fore.RED
                + "Error: Cannot report score. Missing Syntrac API key,"
                + " go to https://app.syntrac.com/settings/api-keys to create one"
            )
            print("Set the SYNTRAC_API_KEY environment variable to the key")
            print(Fore.RESET)
            return

        Syntrac.__fetcher.patch(
            f"steps/{id}",
            body,
        )
