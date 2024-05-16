from typing import Sequence

from opentelemetry.trace import Span

from .UtilFunction import convert_nanoseconds_to_string


def format_error_spans(origin_spans: Sequence[Span], token):
    data = {}
    error = {}
    spans = []
    for idx, origin_span in enumerate(origin_spans):
        # 마지막 Span의 경우, error 부분을 파싱해 저장
        if idx == len(origin_spans) - 1:
            error["exception.type"] = origin_span.events[0].attributes["exception.type"]
            error["exception.message"] = origin_span.events[0].attributes["exception.message"]
            error["exception.flow"] = _extract_exception_flow(origin_span.events[0].attributes["exception.stacktrace"])
        spans.append({
          "name": origin_span.name,
          "spanId": origin_span.get_span_context().span_id,
          'parent_span_id': origin_span.parent.span_id if origin_span.parent else '0000000000000000',
          "kind": origin_span.kind.name,
          "span enter-time": convert_nanoseconds_to_string(origin_span.start_time),
          "span exit-time": convert_nanoseconds_to_string(origin_span.end_time),
          "attributes": {str(k): str(v) for k, v in origin_span.attributes.items()}
        })

    data["tracer"] = "omegi-tracer-python"
    data["traceId"] = origin_spans[0].get_span_context().trace_id
    data["token"] = token
    data["serviceName"] = origin_spans[0].resource.attributes["service.name"]
    data["error"] = error
    data["spans"] = spans
    return data


def _extract_exception_flow(stack_trace):
    flow_steps = {}
    error_stack = []
    lines = stack_trace.strip().split('\n')
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if 'File' in line:
            parts = line.split(', ')
            if len(parts) >= 2:
                file_path = parts[0].split('"')[1]
                file_path = file_path[1:]
                method_name = file_path.replace('/', '.').replace('.py', '')
                if 'in' in line:
                    in_parts = line.split(' in ')
                    if len(in_parts) >= 2:
                        method_name += f'.{in_parts[1].strip()}'
                error_stack.append(method_name)
    for idx, error in enumerate(error_stack, start=1):
        flow_steps[f'step.{idx}'] = error
    return {"exception.flow": flow_steps}

