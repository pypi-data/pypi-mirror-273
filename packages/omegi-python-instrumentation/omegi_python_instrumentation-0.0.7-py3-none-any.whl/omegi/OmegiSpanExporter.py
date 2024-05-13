import json
import os
import re
from typing import Sequence

from kafka import KafkaProducer
from opentelemetry.sdk.trace.export import SpanExporter
from opentelemetry.trace import Span


class OmegiKafkaSpanExporter(SpanExporter):
    def __init__(self):
        kafka_config = os.environ.get('KAFKA_CONFIG', "localhost:9092").split()
        topic = os.environ.get('KAFKA_TOPIC', "error")
        token = os.environ.get('OMEGI_TOKEN', "ddddd")

        # self.producer = KafkaProducer(bootstrap_servers=kafka_config)
        self.topic = topic
        self.token = token

    def export(self, spans: Sequence[Span]):
        is_error = False
        for span in spans:
            print(span.get_span_context(), flush=True)
            if(span.name == 'exception'):
                is_error = True
                break
        if is_error:
            message = json.dumps(self.__format_spans__(spans)).encode('utf-8')
            print(message, flush=True)
            # self.producer.send(self.topic, message)

    def __format_spans__(self, origin_spans: Sequence[Span]):
        data = {}
        error = {}
        spans = []
        trace_id = None
        for origin_span in origin_spans:
            if origin_span.name == 'exception':
                error["exception.type"] = origin_span.attributes["exception.type"][8:-2]
                error["exception.message"] = origin_span.attributes["exception.message"]
                error["exception.flow"] = self.__extract_exception_flow__(origin_span.attributes["exception.stacktrace"])
            else:
                trace_id = origin_span.get_span_context().trace_id
                spans.append({
                  "name": origin_span.name,
                  "spanId": origin_span.get_span_context().span_id,
                  'parent_span_id': origin_span.parent.span_id if origin_span.parent else None,
                  "kind": origin_span.kind.name,
                  "span enter-time": origin_span.start_time,
                  "span exit-time": origin_span.end_time,
                  "attributes": {str(k): str(v) for k, v in origin_span.attributes.items()}
                })

        data["tracer"] = "omegi"
        data["traceId"] = trace_id
        data["error"] = error
        data["spans"] = spans
        return data

    def __extract_exception_flow__(self, stack_trace):
        flow_steps = {}
        lines = stack_trace.strip().split('\n')
        for i, line in enumerate(lines):
            if 'File "' in line:
                file_path, function_name = re.search(r'File "(.+)", line \d+, in (.+)', line).groups()
                module_name = '.'.join(file_path.split('/')[-1].split('.')[:-1])
                if 'site-packages' in file_path:
                    module_name = file_path.split('site-packages/')[1].split('/')[0] + '.' + module_name
                step_name = f"step.{i+1}"
                flow_steps[step_name] = f"{module_name}.{function_name}"
        return {"exception.flow": flow_steps}

    def shutdown(self):
        self.producer.flush()
        self.producer.close()
