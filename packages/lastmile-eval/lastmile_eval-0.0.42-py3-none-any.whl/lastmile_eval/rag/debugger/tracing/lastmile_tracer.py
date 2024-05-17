"""
File to define the LastMileTracer class that implements the LastMileTracerAPI.
This class should not be instantiated directly. Instead, use the the method
`get_lastmile_tracer()` from the `lastmile_eval.rag.debugger.tracing` module
"""

from functools import wraps
import inspect
import json
import os
from contextlib import contextmanager
import logging
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    Optional,
    ParamSpec,
    Sequence,
    Union,
)
from urllib.parse import urlencode

import requests
from opentelemetry import context as context_api
from opentelemetry import trace as trace_api
from opentelemetry.trace import SpanContext
from opentelemetry.trace.span import INVALID_SPAN, Span
from opentelemetry.util import types
from requests import Response
from requests.adapters import HTTPAdapter, Retry

from lastmile_eval.rag.debugger.api import (
    LastMileTracer as LastMileTracerAPI,
    RAGIngestionEvent,
    RAGQueryEvent,
    RAGTraceEventResult,
)
from .sdk_utils.endpoints import (
    read_key_value_pair,
    store_key_value_pair,
)

from lastmile_eval.rag.debugger.tracing.decorators import (
    _try_log_input,
    _try_log_output,
)

from ..common.core import IndexingTraceID
from ..common.utils import raise_for_status, get_lastmile_api_token
from .trace_data_singleton import TraceDataSingleton
from .utils import (
    set_trace_data,
    convert_int_id_to_hex_str,
    convert_to_context,
)

T_ParamSpec = ParamSpec("T_ParamSpec")


class LastMileTracer(
    LastMileTracerAPI,
):
    """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer`"""

    def __init__(
        self,
        lastmile_api_token: str,
        tracer_implementor: trace_api.Tracer,
        tracer_name: str,
        # TODO: Don't make params Any type
        # Global params are the parameters that are saved with every trace
        global_params: Optional[dict[str, Any]],
    ):
        self.lastmile_api_token = lastmile_api_token
        TraceDataSingleton(global_params=global_params)
        self.tracer_implementor: trace_api.Tracer = tracer_implementor

        self.project_name = tracer_name
        self.project_id: str
        self.set_project()

        # TODO: Add ability to suppress printing to stdout in default logger
        # TODO: Put this logic in helper method
        self.logger: logging.Logger = logging.getLogger(self.project_name)

        log_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-5.5s]  %(message)s"
        )
        logger_filepath = os.path.join(
            os.getcwd(), "logs", f"{self.project_name}.log"
        )
        if not os.path.exists(os.path.dirname(logger_filepath)):
            os.mkdir(os.path.dirname(logger_filepath))
        open(logger_filepath, "w", encoding="utf-8").close()
        file_handler = logging.FileHandler(logger_filepath)
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

    def trace_function(
        self,
        name: Optional[str] = None,
        context: Optional[Union[context_api.Context, SpanContext, str]] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Optional[Sequence[trace_api.Link]] = None,
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        TODO: async
        Decorator that provides the same functionality as
        LastMileTracer.start_as_current_span except that it also logs the wrapped
        function's input and output values as attributes on the span.
        """

        def decorator(func: Callable[..., Any]):
            f_sig = inspect.signature(func)

            @wraps(func)
            def _wrap(
                *f_args: T_ParamSpec.args, **f_kwargs: T_ParamSpec.kwargs
            ):

                with self.start_as_current_span(
                    name if name is not None else func.__name__,
                    context,
                    kind,
                    attributes,
                    links,
                    start_time,
                    record_exception,
                    set_status_on_exception,
                    end_on_exit,
                ) as span:
                    _try_log_input(span, f_sig, f_args, f_kwargs)
                    return_value = func(*f_args, **f_kwargs)
                    _try_log_output(span, return_value)
                    return return_value

            return _wrap

        return decorator

    @contextmanager
    # pylint: disable=too-many-arguments
    def start_as_current_span(
        self,
        name: str,
        context: Optional[Union[context_api.Context, SpanContext, str]] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Optional[Sequence[trace_api.Link]] = None,
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Iterator[Span]:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.start_as_current_span()`"""
        context = convert_to_context(context)
        with self.tracer_implementor.start_as_current_span(
            name,
            context,
            kind,
            attributes,
            links,
            start_time,
            record_exception,
            set_status_on_exception,
            end_on_exit,
        ) as span:
            set_trace_data(span=span, project_id=self.project_id)
            yield span

    # pylint: disable=too-many-arguments
    def start_span(
        self,
        name: str,
        context: Optional[Union[context_api.Context, SpanContext, str]] = None,
        kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
        attributes: types.Attributes = None,
        links: Sequence[trace_api.Link] = (),
        start_time: Optional[int] = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
    ) -> Span:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.start_span()`"""
        context = convert_to_context(context)
        span = self.tracer_implementor.start_span(
            name,
            context,
            kind,
            attributes,
            links,
            start_time,
            record_exception,
            set_status_on_exception,
        )
        set_trace_data(span=span, project_id=self.project_id)
        return span

    def mark_rag_ingestion_trace_event(
        self,
        event: RAGIngestionEvent,
        span: Optional[Span] = None,
    ) -> RAGTraceEventResult:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.mark_rag_ingestion_trace_event()`"""
        current_span: Span = span or trace_api.get_current_span()
        if current_span == INVALID_SPAN:
            return RAGTraceEventResult(
                is_success=False,
                message=f"No span to log RAGIngestionEvent: {event}",
            )

        # Store event so we can log it to RagIngestionTrace table after the trace
        # has ended
        trace_data_singleton = TraceDataSingleton()
        trace_data_singleton.add_rag_ingestion_event(event)

        # TODO: Add event to current span once we have defined ingestion events

        return RAGTraceEventResult(
            is_success=True,
            message=f"Logged RAGIngestionEvent {event} to span id '{convert_int_id_to_hex_str(current_span.get_span_context().span_id)}'",
        )

    def mark_rag_query_trace_event(
        self,
        event: RAGQueryEvent,
        indexing_trace_id: Optional[str] = None,
        span: Optional[Span] = None,
    ) -> RAGTraceEventResult:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.mark_rag_query_trace_event()`"""
        if indexing_trace_id is not None:
            indexing_trace_id = IndexingTraceID(indexing_trace_id)

        current_span: Span = span or trace_api.get_current_span()
        if current_span == INVALID_SPAN:
            return RAGTraceEventResult(
                is_success=False,
                message=f"No span to log RAGQueryEvent: {event}",
            )

        # Store event so we can log it to RagQueryTrace table after the trace
        # has ended
        trace_data_singleton = TraceDataSingleton()
        trace_data_singleton.add_rag_query_event(event)

        # Add event to current span
        current_span.add_event(
            type(event).__name__,
            attributes={
                "rag_query_event": event.model_dump_json(),
                # types.AttributeValue does not contain None so have to cast to str
                # "test_set_id": str(test_set_id),
                "indexing_trace_id": str(
                    indexing_trace_id  # TODO: Use hex value of TraceID
                ),
            },
        )

        return RAGTraceEventResult(
            is_success=True,
            message=f"Logged RAGQueryEvent {event} to span id '{convert_int_id_to_hex_str(current_span.get_span_context().span_id)}'",
        )

    def add_rag_event_for_span(
        self,
        event_name: str,
        span: Optional[Span] = None,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[dict[Any, Any]] = None,
    ) -> None:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.add_rag_event_for_span()`"""
        if input is not None and output is None:
            raise ValueError(
                "If you pass in input, you must also define an output value for this event"
            )
        if input is None and output is not None:
            raise ValueError(
                "If you pass in output, you must also define an input value for this event"
            )

        if input is None and output is None:
            if event_data is None:
                raise ValueError(
                    "If input and output are not set, you must pass in event_data"
                )

        current_span: Span = span or trace_api.get_current_span()
        if current_span == INVALID_SPAN:
            raise ValueError(
                "Could not find a valid span to connect a RAG event to. Either pass in a span argument directly or use the `LastMileTracer.start_as_current_span` method to ensure that `trace_api.get_current_span()` returns a valid span"
            )

        span_id = convert_int_id_to_hex_str(
            current_span.get_span_context().span_id
        )
        trace_data_singleton = TraceDataSingleton()
        try:
            # Check if args are JSON serializable, otherwise won't be able to
            # export trace data in the collector
            json.dumps(event_data)
            json.dumps(input)
            json.dumps(output)
        except TypeError as e:
            raise TypeError(
                f"Error JSON serializing input, output and event_data arguments for (trace_id, span_id): ({trace_data_singleton.trace_id}, {span_id})"
            ) from e

        try:
            event_payload = {
                "event_name": event_name,
                "span_id": span_id,
                "input": input or "",
                "output": output or "",
                "event_data": event_data or {},
            }
            trace_data_singleton = TraceDataSingleton()
            trace_data_singleton.add_rag_event_for_span(event_payload)
        except Exception as e:
            raise RuntimeError(
                f"Error adding rag event for (trace_id, span_id): ({trace_data_singleton.trace_id}, {span_id})"
            ) from e

    # # I have no idea wtf chunking does, so just going to exclude it
    # # See reference in this trace to see inputs and outputs
    # def add_chunking_event_for_span(
    #     self,
    #     span: Optional[Span] = None,
    # ) -> None:
    #     # self.add_rag_event_for_span(event_name=str(CBEventType.CHUNKING), span, input=None, output=None, event_data=None)
    #     self.add_rag_event_for_span(
    #         event_name=str(CBEventType.CHUNKING),
    #         span=span,
    #         input=None,
    #         output=None,
    #         event_data=None,
    #     )

    # def add_retrieve_event_for_span(
    #     self,
    #     span: Optional[Span] = None,
    #     input_query: str,
    #     retrieved_docs: list[str],
    # )

    #     event_name: str,
    #     span: Optional[Span] = None,
    #     # TODO: Have better typing for JSON for input, output, event_data
    #     input: Any = None,
    #     output: Any = None,
    #     event_data: Optional[dict[Any, Any]] = None,
    # CHUNKING = "chunking"
    # NODE_PARSING = "node_parsing"
    # EMBEDDING = "embedding"
    # LLM = "llm"
    # QUERY = "query"
    # RETRIEVE = "retrieve"
    # SYNTHESIZE = "synthesize"
    # TREE = "tree"
    # SUB_QUESTION = "sub_question"
    # TEMPLATING = "templating"
    # FUNCTION_CALL = "function_call"
    # RERANKING = "reranking"
    # EXCEPTION = "exception"
    # AGENT_STEP = "agent_step"

    def add_rag_event_for_trace(
        self,
        event_name: str,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[dict[Any, Any]] = None,
    ) -> None:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.add_rag_event_for_trace()`"""
        if input is not None and output is None:
            raise ValueError(
                "If you pass in input, you must also define an output value for this event"
            )
        if input is None and output is not None:
            raise ValueError(
                "If you pass in output, you must also define an input value for this event"
            )

        if input is None and output is None:
            if event_data is None:
                raise ValueError(
                    "If input and output are not set, you must pass in event_data"
                )

        trace_data_singleton = TraceDataSingleton()
        try:
            # Check if args are JSON serializable, otherwise won't be able to
            # export trace data in the collector
            json.dumps(event_data)
            json.dumps(input)
            json.dumps(output)
        except TypeError as e:
            raise TypeError(
                f"Error JSON serializing input, output and event_data arguments for trace_id: {trace_data_singleton.trace_id}"
            ) from e

        try:
            event_payload = {
                "event_name": event_name,
                "input": input or "",
                "output": output or "",
                "event_data": event_data or {},
            }
            trace_data_singleton = TraceDataSingleton()
            trace_data_singleton.add_rag_event_for_trace(event_payload)
        except Exception as e:
            raise RuntimeError(
                f"Error adding rag event for trace id: {trace_data_singleton.trace_id}"
            ) from e

    # TODO: Don't make params Any type
    def get_params(self) -> dict[str, Any]:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.get_params()`"""
        trace_data_singleton = TraceDataSingleton()
        return trace_data_singleton.get_params()

    def register_param(
        self,
        key: str,
        value: Any,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.register_param()`"""

        trace_data_singleton = TraceDataSingleton()
        try:
            # Check if value is JSON serializable, otherwise won't be able to
            # export trace data in the collector
            json.dumps(value)
        except TypeError as e:
            raise TypeError(
                f"Error registering parameter to trace {trace_data_singleton.trace_id}"
            ) from e

        trace_data_singleton.register_param(key, value)

        # Log this also in the current span to help with debugging if needed
        if should_also_save_in_span:
            current_span: Span = span or trace_api.get_current_span()
            if current_span != INVALID_SPAN:
                if isinstance(value, (dict, Dict)):
                    value = json.dumps(value)
                current_span.set_attribute(
                    key,
                    value,
                )

    def register_params(
        self,
        params: dict[str, Any],
        should_overwrite: bool = False,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.register_params()`"""
        if should_overwrite:
            self.clear_params(should_clear_global_params=False)

        for k, v in params.items():
            self.register_param(
                k,
                v,
                should_also_save_in_span=should_also_save_in_span,
                span=span,
            )

    def clear_params(self, should_clear_global_params: bool = False) -> None:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.clear_params()`"""
        trace_data_singleton = TraceDataSingleton()
        trace_data_singleton.clear_params(should_clear_global_params)

    def log(self, data: Any, logger: Optional[logging.Logger] = None) -> None:
        """See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer.log()`"""
        if logger is None:
            logger = self.logger
        TraceDataSingleton().log_data(data, logger)

    def log_feedback(
        self,
        feedback: str | dict[str, Any],
        trace_id: Optional[Union[str, int]] = None,
        span_id: Optional[Union[str, int]] = None,
        # TODO: Create macro for default timeout value
        timeout: int = 60,
    ) -> None:
        """
        Feedback is a string and optionally a free-form JSON serializable object that can be
        Specify a trace_id to link the feedback to a specific trace.
        Specify a span_id AND trace_id to link the feedback to a specific span.
        If neither are specified, the feedback is linked to the project.
        """
        lastmile_endpoint = (
            "https://lastmileai.dev/api/evaluation_feedback/create"
        )
        payload = {
            "feedback": {"text": feedback},
            "projectId": self.project_id,
        }

        if span_id is not None:
            if isinstance(span_id, str):
                span_id = int(span_id)
            if isinstance(trace_id, str):
                trace_id = int(trace_id)

            if trace_id is None:
                raise ValueError(
                    "If you specify a span_id, you must also specify a trace_id"
                )

            payload["traceId"] = convert_int_id_to_hex_str(trace_id)
            payload["spanId"] = convert_int_id_to_hex_str(span_id)
        elif trace_id is not None:
            if isinstance(trace_id, str):
                trace_id = int(trace_id)
            payload["traceId"] = convert_int_id_to_hex_str(trace_id)

        response: Response = requests.post(
            lastmile_endpoint,
            headers={"Authorization": f"Bearer {self.lastmile_api_token}"},
            json=payload,
            timeout=timeout,
        )
        raise_for_status(
            response,
            f"Error logging feedback for project {self.project_name} (payload={json.dumps(payload)})",
        )

        return response.json()

    def set_project(self) -> None:
        """
        Gets the project or creates a new one if it doesn't exist.
        TODO: allow user to specify project visibility to allow personal project in an org
        """

        list_project_endpoint = f"https://lastmileai.dev/api/evaluation_projects/list?{urlencode({'name': self.project_name})}"
        response = requests.get(
            list_project_endpoint,
            headers={"Authorization": f"Bearer {self.lastmile_api_token}"},
            timeout=60,
        )
        raise_for_status(
            response, f"Error fetching projects with name {self.project_name}"
        )
        evaluation_projects = response.json()["evaluationProjects"]
        project_exists = len(evaluation_projects) > 0

        if not project_exists:
            # TODO: Make wrapper function to handle retries automatically
            # in all our request calls
            create_project_endpoint = (
                "https://lastmileai.dev/api/evaluation_projects/create"
            )
            request_session = requests.Session()
            retries = Retry(
                total=1,
                backoff_factor=1,  # 0s, 2s, 4s, 8s, 16s
                # status_forcelist=[ 502, 503, 504 ]
            )
            request_session.mount("https://", HTTPAdapter(max_retries=retries))
            response = request_session.post(
                create_project_endpoint,
                headers={"Authorization": f"Bearer {self.lastmile_api_token}"},
                json={
                    "name": self.project_name,
                },
                timeout=60,  # TODO: Remove hardcoding
            )
            raise_for_status(
                response, f"Error creating project {self.project_name}"
            )
            self.project_id = response.json()["id"]
        else:
            self.project_id = evaluation_projects[0]["id"]

    def store_trace_id(
        self,
        key: str,
        trace_id: int,
        span_id: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = None,
        value_override: Any = None,  # TODO: restrict or remove
    ) -> None:
        if self.project_id is None:  # type: ignore[has type]
            raise ValueError(
                "Project ID must be set before storing key-value pairs. Try re-initializing the tracer object"
            )

        store_key_value_pair(
            self.project_id,
            key,
            span_id,
            trace_id,
            metadata,
            value_override,
        )

    def read_trace_id(
        self,
        key: str,
    ) -> tuple[str, str]:
        if self.project_id is None:  # type: ignore[has type]
            raise ValueError(
                "Project ID must be set before storing key-value pairs. Try re-initializing the tracer object"
            )
        return read_key_value_pair(self.project_id, key)

    def read_key_value_pair(
        self,
        key: str,
    ) -> tuple[str, str]:
        """
        Returns a pair of (TraceID, SpanID). If span_id is not found, span_id will be None

        Read a key-value pair from remote storage. This is useful for retrieving
        a span or trace later on when performing online feedback or debugging.
        """
        api_token = get_lastmile_api_token(None)
        query_params = {
            "projectId": self.project_id,
            "key": key,
        }
        endpoint = f"https://lastmileai.dev/api/evaluation_key_value_store/read?{urlencode(query_params)}"
        response = requests.get(
            endpoint,
            headers={"authorization": f"Bearer {api_token}"},
            timeout=60,  # TODO: remove hardcoded value
        )
        if not response.ok:
            raise ValueError(f"Error reading key-value pair: {response.text}")
        try:
            span_id = response.json().get("value")
            trace_id = response.json().get("metadata", {}).get("trace_id")
            return (trace_id, span_id)

        except KeyError as e:
            raise KeyError("Could not find key in remote storage") from e
