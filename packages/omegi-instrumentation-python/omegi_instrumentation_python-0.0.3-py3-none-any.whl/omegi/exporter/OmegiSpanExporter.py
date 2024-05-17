import json
import os
import logging
from typing import Sequence

from kafka import KafkaProducer
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.trace import Span, StatusCode

from omegi.util.OmegiErrorSpanFormatter import format_error_spans
from omegi.util.OmegiSamplerSpanFormatter import format_sampler_spans
from omegi.util.UtilFunction import decide_export


class OmegiKafkaSpanExporter(SpanExporter):
    def __init__(self):
        self.kafka_servers = os.environ.get('OMEGI_KAFKA_SERVER', 'localhost:9092').split(',')
        self.error_topic = os.environ.get('OMEGI_KAFKA_TOPIC_ERROR', 'error')
        self.flow_topic = os.environ.get('OMEGI_KAFKA_TOPIC_FLOW', 'flow')
        self.token = os.environ.get('OMEGI_TOKEN', "your_token")
        self.flow_rate = 1 / int(os.environ.get('OMEGI_FLOW_RATE', 5))
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_servers)

    def export(self, spans: Sequence[Span]):
        self._process_sampler_spans(spans)
        self._process_error_spans(spans)

    def _process_sampler_spans(self, spans: Sequence[Span]):
        if decide_export(spans[0].get_span_context().trace_id, rate=self.flow_rate):
            processed_trace = format_sampler_spans(spans, self.token)
            logging.info(f'[OmegiKafkaSpanExporter] _process_sampler_spans -> {processed_trace}')
            self._send_to_kafka(processed_trace, self.flow_topic)

    def _process_error_spans(self, spans: Sequence[Span]):
        is_error = False
        for span in spans:
            if(span.status.status_code == StatusCode.ERROR):
                is_error = True
                break
        if is_error:
            processed_trace = format_error_spans(spans, self.token)
            logging.info(f'[OmegiKafkaSpanExporter] _process_error_spans -> {processed_trace}')
            self._send_to_kafka(processed_trace, self.error_topic)

    def _send_to_kafka(self, data, topic):
        message = json.dumps(data).encode('utf-8')
        self.producer.send(topic, message)

    def shutdown(self):
        self.producer.flush()
        self.producer.close()
