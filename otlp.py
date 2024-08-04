import logging
from opentelemetry import trace
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPSpanGrpcExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import (BatchSpanProcessor, ConsoleSpanExporter)


func_name = "demo_func"
resource = Resource(attributes={ SERVICE_NAME: func_name })
# NOTE: OTEL_EXPORTER_OTLP_ENDPOINT env var should be defined to export logs
# i.e. `http://10.20.30.11:4417`
span_processor = BatchSpanProcessor(OTLPSpanGrpcExporter())
trace_provider = TracerProvider(resource=resource, active_span_processor=span_processor)
trace.set_tracer_provider(trace_provider)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s [%(levelname)s] %(message)s')
logger_provider = LoggerProvider(resource=Resource.create(
  {
    "service.name": func_name,
  })
)

# NOTE: OTEL_EXPORTER_OTLP_TRACES_ENDPOINT env var should be defined to export logs
# i.e. `http://10.20.30.11:4317/v1/traces`
logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)


logger = logging.getLogger(func_name)
tracer = trace.get_tracer(func_name)
