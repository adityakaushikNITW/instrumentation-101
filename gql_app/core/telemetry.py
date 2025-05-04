from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from ariadne.types import Extension
import logging
import os
import time

class GraphQLMetricsExtension(Extension):
    def __init__(self):
        self.meter = metrics.get_meter(__name__)
        # Create metrics
        self.query_counter = self.meter.create_counter(
            "graphql.queries.total",
            description="Total number of GraphQL queries"
        )
        self.mutation_counter = self.meter.create_counter(
            "graphql.mutations.total",
            description="Total number of GraphQL mutations"
        )
        self.error_counter = self.meter.create_counter(
            "graphql.errors.total",
            description="Total number of GraphQL errors"
        )
        self.duration_histogram = self.meter.create_histogram(
            "graphql.operation.duration",
            description="Duration of GraphQL operations in seconds",
            unit="s"
        )
        self.start_time = None

    def request_started(self, context):
        self.start_time = time.time()
        # Get the operation type from the context
        operation_type = context.get("operation_type")
        if operation_type == "query":
            self.query_counter.add(1)
        elif operation_type == "mutation":
            self.mutation_counter.add(1)

    def format(self, context):
        if self.start_time:
            duration = time.time() - self.start_time
            self.duration_histogram.record(duration)
            self.start_time = None

        if context.get("errors"):
            self.error_counter.add(len(context["errors"]))

def setup_telemetry():
    # Configure resource
    resource = Resource.create({
        "service.name": os.getenv("OTEL_SERVICE_NAME", "parking-lot-gql"),
        "service.version": "1.0.0"
    })

    # Configure trace provider
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    trace.set_tracer_provider(tracer_provider)

    # Configure metric provider
    metric_exporter = OTLPMetricExporter()
    metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Configure logging
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter())
    )
    set_logger_provider(logger_provider)
    
    # Configure Python logging
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO) 