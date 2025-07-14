from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from src.core.config import settings
from src.core.database import engine

def setup_tracing(service_name: str):
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })

    # tracing
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    trace_exporter = OTLPSpanExporter(
        endpoint=settings.OTLP_EXPORTER_ENDPOINT,
        insecure=True
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

    return trace.get_tracer(service_name)


def setup_metrics(service_name: str):
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })

    # metrics
    metric_exporter = OTLPMetricExporter(
        endpoint=settings.OTLP_EXPORTER_ENDPOINT,
        insecure=True
    )

    reader = PeriodicExportingMetricReader(metric_exporter)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)

    return metrics.get_meter(service_name)

def instrument_fastapi(app):
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)
    RedisInstrumentor().instrument()
