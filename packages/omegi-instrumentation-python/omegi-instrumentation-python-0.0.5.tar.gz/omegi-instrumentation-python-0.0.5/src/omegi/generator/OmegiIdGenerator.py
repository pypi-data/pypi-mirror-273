from opentelemetry.sdk.trace import IdGenerator
import os


class HexIdGenerator(IdGenerator):
    def generate_trace_id(self) -> str:
        trace_id = os.urandom(16).hex()
        return trace_id

    def generate_span_id(self) -> str:
        span_id = os.urandom(8).hex()
        return span_id