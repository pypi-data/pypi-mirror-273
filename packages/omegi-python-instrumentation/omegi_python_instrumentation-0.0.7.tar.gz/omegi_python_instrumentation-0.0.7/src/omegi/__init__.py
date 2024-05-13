from typing import Collection

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import unwrap

from .OmegiSpanExporter import OmegiKafkaSpanExporter
from .OmegiUtil import wrap_functions


class OmegiInstrumentor(BaseInstrumentor):

    def instrumentation_dependencies(self) -> Collection[str]:
        return []

    def _instrument(self, **kwargs):
        tracer = trace.get_tracer(__name__)
        wrap_functions(tracer)

    def _uninstrument(self, **kwargs):
        return unwrap(kwargs)