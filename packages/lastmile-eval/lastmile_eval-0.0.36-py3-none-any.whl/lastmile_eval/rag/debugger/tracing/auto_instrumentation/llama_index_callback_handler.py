import json
import logging
from time import time_ns
from typing import Any, Dict, Optional

from llama_index.core.callbacks import CBEventType, EventPayload
from openinference.instrumentation.llama_index._callback import (
    OpenInferenceTraceCallbackHandler,
    payload_to_semantic_attributes,
    _is_streaming_response,
    _flatten,
    _ResponseGen,
    _EventData,
)
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry import trace as trace_api
from opentelemetry import context as context_api
from opentelemetry.context import _SUPPRESS_INSTRUMENTATION_KEY
from typing_extensions import TypeAlias
from lastmile_eval.rag.debugger.tracing import get_lastmile_tracer
from ...common.utils import DEFAULT_PROJECT_NAME, LASTMILE_SPAN_KIND_KEY_NAME

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_EventId: TypeAlias = str
_ParentId: TypeAlias = str


class LlamaIndexCallbackHandler(OpenInferenceTraceCallbackHandler):
    """
    This is a callback handler for automatically instrumenting with
    LLamaIndex. Here's how to use it:

    ```
    from lastmile_eval.rag.debugger.tracing import LlamaIndexCallbackHandler
    llama_index.core.global_handler = LlamaIndexCallbackHandler()
    # Do regular LlamaIndex calls as usual
    ```
    """

    def __init__(self, project_name: Optional[str] = None):
        tracer = get_lastmile_tracer(
            project_name or DEFAULT_PROJECT_NAME,
            # output_filepath="/Users/rossdancraig/Projects/eval/src/lastmile_eval/rag/debugger/tracing/auto_instrumentation/ok_cool.txt",
        )
        super().__init__(tracer)

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        event_id = super().on_event_start(
            event_type, payload, event_id, parent_id, **kwargs
        )
        if event_id not in self._event_data:
            # OpenInferenceTraceCallbackHandler is acting on a
            # CBEventType.TEMPLATING event type that does not generate a span
            # so we should exit early and do the next one
            return event_id

        span = self._event_data[event_id].span
        span.set_attribute(LASTMILE_SPAN_KIND_KEY_NAME, event_type)

        if payload:
            serializable_payload: Dict[str, Any] = {}
            for key, value in payload.items():
                try:
                    json.dumps(value)
                except TypeError as _e:
                    serializable_value: list[Any] = []
                    if isinstance(value, list):
                        for item in value:
                            to_dict = getattr(item, "dict", None)
                            if callable(to_dict):
                                serializable_value.append(to_dict())
                        if len(serializable_value) > 0:
                            value = serializable_value
                    else:
                        to_dict = getattr(value, "dict", None)
                        if callable(to_dict):
                            value = to_dict()

                try:
                    json.dumps(value)
                    # self._tracer.register_param(key, value, span=span)
                except TypeError as e:
                    # TODO: Change to logger.warning()
                    # print(f"Error serializing value: {e}")
                    value = f"Error serializing LlamaIndex payload value: {repr(e)}"
                    # print("yo yo ma: not serializable: ")
                    # print(f"{event_type=}")
                    # print(f"{key=}")
                    # print(f"{value=}")
                    # print()
                    # pass
                finally:
                    # Parameter when saving to span attributes can only be as
                    # a string value
                    self._tracer.register_param(key, value, span=span)
                    serializable_payload[str(key)] = value

            event_type = str(event_type)
            if event_type != "EventPayload.SERIALIZED":
                # Remove "serialized" from the spans
                # We need to do this because this info stores the API keys and we
                # want to remove. Other pertinent data is stored in the span attributes
                # like model name and invocation params already
                self._tracer.add_rag_event_for_span(
                    event_name=str(event_type),
                    span=span,
                    event_data=serializable_payload,
                )
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        if context_api.get_value(_SUPPRESS_INSTRUMENTATION_KEY):
            return

        with self._lock:
            if event_type is CBEventType.TEMPLATING:
                if (
                    parent_id := self._templating_parent_id.pop(event_id, None)
                ) and payload:
                    if parent_id in self._templating_payloads:
                        self._templating_payloads[parent_id].append(payload)
                    else:
                        self._templating_payloads[parent_id] = [payload]
                return
            if not (event_data := self._event_data.pop(event_id, None)):
                return

        event_data.end_time = time_ns()
        is_dispatched = False

        if payload is not None:
            event_data.payloads.append(payload.copy())
            if isinstance(
                (exception := payload.get(EventPayload.EXCEPTION)), Exception
            ):
                event_data.exceptions.append(exception)
            try:
                event_data.attributes.update(
                    payload_to_semantic_attributes(
                        event_type, payload, is_event_end=True
                    ),
                )
            except Exception:
                logger.exception(
                    f"Failed to convert payload to semantic attributes. "
                    f"event_type={event_type}, payload={payload}",
                )
            if (
                _is_streaming_response(
                    response := payload.get(EventPayload.RESPONSE)
                )
                and response.response_gen is not None
            ):
                response.response_gen = _ResponseGen(
                    response.response_gen, event_data
                )
                is_dispatched = True

        if not is_dispatched:
            _finish_tracing(event_data)
        return


def _finish_tracing(event_data: _EventData) -> None:
    if not (span := event_data.span):
        return
    attributes = event_data.attributes
    if event_data.exceptions:
        status_descriptions: list[str] = []
        for exception in event_data.exceptions:
            span.record_exception(exception)
            # Follow the format in OTEL SDK for description, see:
            # https://github.com/open-telemetry/opentelemetry-python/blob/2b9dcfc5d853d1c10176937a6bcaade54cda1a31/opentelemetry-api/src/opentelemetry/trace/__init__.py#L588  # noqa E501
            status_descriptions.append(
                f"{type(exception).__name__}: {exception}"
            )
        status = trace_api.Status(
            status_code=trace_api.StatusCode.ERROR,
            description="\n".join(status_descriptions),
        )
    else:
        status = trace_api.Status(status_code=trace_api.StatusCode.OK)
    span.set_status(status=status)
    try:
        span.set_attributes(dict(_flatten(attributes)))

        # Remove "serialized" from the spans
        # We need to do this because this info stores the API keys and we
        # want to remove. Other pertinent data is stored in the span attributes
        # like model name and invocation params already
        if (
            isinstance(span, ReadableSpan)
            and span._attributes is not None
            and "serialized" in span._attributes
        ):
            del span._attributes["serialized"]
    except Exception:
        logger.exception(
            f"Failed to set attributes on span. event_type={event_data.event_type}, "
            f"attributes={attributes}",
        )
    span.end(end_time=event_data.end_time)
