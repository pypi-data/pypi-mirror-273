import logging
import os
from typing import Collection

from opentelemetry import trace, propagate
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from .exporter.OmegiSpanExporter import OmegiKafkaSpanExporter
from .util.OmegiDependencyInstrument import instrument_dependencies
from .util.OmegiTracingSetup import wrap_functions


class OmegiInstrumentor(BaseInstrumentor):
    def __init__(self, app=None):
        self.app = app
        self.project_root = os.getenv("OMEGI_PROJECT_ROOT", "/app")

    def instrumentation_dependencies(self) -> Collection[str]:
        return []

    def instrument(self):
        self._instrument()

    def _instrument(self):
        """
        SETTING UP INSTRUMENTATION
        1. Figure Custom TraceExporter and SpanProcessor
        TraceExporter exports spans to Kafka.
        Kafka server urls can be figured through environment variables
        2. Figure Other Instrumentations
        By installed libraries this library detects fast api, django, flask, elasticsearch
        detected library's instrumentation is enabled automatically
        3. Set Function tracing
        detect module's functions and wrap it in decorator to enable tracing
        """
        if self.project_root is None:
            logging.error("Please set Project root")
        # Setup Propagator, Custom Exporter, SpanProcessor
        propagator = TraceContextTextMapPropagator()
        propagate.set_global_textmap(propagator)
        span_processor = BatchSpanProcessor(self._set_exporter())
        trace.set_tracer_provider(TracerProvider(
            resource=Resource.create({"service.name": os.getenv("OMEGI_SERVICE_NAME", 'test-server')}),
        ))
        trace.get_tracer_provider().add_span_processor(span_processor)
        tracer = trace.get_tracer(__name__)
        # Setup Instrumentation
        if self.app is not None:
            self._start_depending_instrumentation(app=self.app)
        # Setup Tracing Functions
        wrap_functions(tracer, self.project_root)

    def _uninstrument(self, **kwargs):
        return unwrap(kwargs)

    def _start_depending_instrumentation(self, app):
        instrument_dependencies(self.app)

    def _set_exporter(self):
        exporter_kind = os.environ.get("OMEGI_EXPORTER_KIND", "kafka")
        if exporter_kind == 'kafka':
            return OmegiKafkaSpanExporter()
        elif exporter_kind == 'console':
            return ConsoleSpanExporter()
        else:
            return ConsoleSpanExporter()

