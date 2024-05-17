from typing import Sequence

from opentelemetry.trace import Span, format_trace_id, format_span_id

from .UtilFunction import convert_nanoseconds_to_string


def format_sampler_spans(origin_spans: Sequence[Span], token):
    data = {"tracer": "omegi-tracer-python",
            "traceId": format_trace_id(origin_spans[0].get_span_context().trace_id),
            "token": token,
            "serviceName": origin_spans[0].resource.attributes["service.name"],
            "parentSpanId": format_span_id(origin_spans[len(origin_spans)-1].parent.span_id) if origin_spans[len(origin_spans)-1].parent else '0000000000000000',
            "spanId": format_span_id(origin_spans[0].get_span_context().span_id),
            "spanEnterTime": convert_nanoseconds_to_string(origin_spans[len(origin_spans)-1].start_time),
            "spanExitTime": convert_nanoseconds_to_string(origin_spans[0].end_time)
            }
    return data