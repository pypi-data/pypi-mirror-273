"""
File to describe the APIs and SDKs that users can use in code, see example
folder for example on how it can be implemented
"""

import json
import os
from contextlib import contextmanager
import logging
from typing import Any, Dict, Iterator, Optional, Sequence, Union
from urllib.parse import urlencode

import requests
from opentelemetry import context as context_api
from opentelemetry import trace as trace_api
from opentelemetry.context import Context
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.trace import SpanContext
from opentelemetry.trace.span import INVALID_SPAN, Span, TraceFlags, TraceState
from opentelemetry.util import types
from requests import Response
from requests.adapters import HTTPAdapter, Retry

from lastmile_eval.rag.debugger.api import (
    LastMileTracer,
    RAGIngestionEvent,
    RAGQueryEvent,
    RAGTraceEventResult,
)

from ..common.core import IndexingTraceID
from ..common.utils import SHOW_DEBUG, get_lastmile_api_token
from .exporter import LastMileOTLPSpanExporter
from .trace_data_singleton import TraceDataSingleton

SHOW_RAG_TRACE_IDS = False


class _LastMileTracerProvider(TracerProvider):
    """
    Subclass of TracerProvider that defines the connection between LastMile
    Jaeger collector endpoint to the _LastMileTracer
    """

    def __init__(
        self,
        lastmile_api_token: str,
        output_filepath: Optional[str] = None,
    ):
        super().__init__()

        self._already_defined_tracer_provider = False
        self._tracers: Dict[str, "_LastMileTracer"] = {}

        # If output_filepath is defined, then save trace data to that file
        # instead of forwarding to an OpenTelemetry collector. This is useful
        # for debugging and demo purposes but not recommended for production.
        if output_filepath is not None:
            output_destination = open(output_filepath, "w", encoding="utf-8")
            exporter = ConsoleSpanExporter(out=output_destination)
        else:
            exporter = LastMileOTLPSpanExporter(
                log_rag_query_func=lambda: _log_all_trace_events_and_reset_trace_state(
                    lastmile_api_token
                ),
                endpoint="https://lastmileai.dev/api/trace/create",
                headers={
                    "authorization": f"Bearer {lastmile_api_token}",
                    "Content-Type": "application/json",
                },
                # TODO: Add timeout argument and have default here
            )

        # We need to use SimpleSpanProcessor instead of BatchSpanProcessor
        # because BatchSpanProcessor does not call the exporter.export()
        # method until it is finished batching, but we need to call it at the
        # end of each span to reset the trace-level data otherwise we can
        # error.

        # The future workaround is to make all the trace-level data checks and
        # trace-data resetting occur OUTSIDE of the exporter.export() method,
        # and simply do those. Then we can have a state-level manager dict
        # where we keep track of traceId, and the state corresponding to that
        # so that when we call the callback log_rag_query_func(), it will take
        # in a trace_id arg to know which trace data to log
        span_processor = SimpleSpanProcessor(exporter)
        self.add_span_processor(span_processor)

    def get_tracer_from_name(
        self,
        token: str,
        tracer_name: str,
        global_params: Optional[dict[str, Any]],
    ) -> "_LastMileTracer":
        """
        Get the tracer object from the tracer_name. If the tracer object is
        already defined, then return that. Otherwise, create a new tracer
        """
        if tracer_name in self._tracers:
            return self._tracers[tracer_name]

        if not self._already_defined_tracer_provider:
            trace_api.set_tracer_provider(self)
            self._already_defined_tracer_provider = True

        tracer_implementor: trace_api.Tracer = trace_api.get_tracer(
            tracer_name
        )
        tracer = _LastMileTracer(
            token,
            tracer_implementor,
            tracer_name,
            global_params,
        )
        self._tracers[tracer_name] = tracer
        return tracer


class _LastMileTracer(
    LastMileTracer,
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
            _set_trace_data(span=span, project_id=self.project_id)
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
        _set_trace_data(span=span, project_id=self.project_id)
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
            message=f"Logged RAGIngestionEvent {event} to span id '{_convert_int_id_to_hex_str(current_span.get_span_context().span_id)}'",
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
            message=f"Logged RAGQueryEvent {event} to span id '{_convert_int_id_to_hex_str(current_span.get_span_context().span_id)}'",
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

        span_id = _convert_int_id_to_hex_str(
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

            payload["traceId"] = _convert_int_id_to_hex_str(trace_id)
            payload["spanId"] = _convert_int_id_to_hex_str(span_id)
        elif trace_id is not None:
            if isinstance(trace_id, str):
                trace_id = int(trace_id)
            payload["traceId"] = _convert_int_id_to_hex_str(trace_id)

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

    def store_key_value_pair(
        self,
        key: str,
        span_id: Optional[int] = None,
        trace_id: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = {},
        value_override: Any = None,  # TODO: Figure out if this should be restricted or removed
    ) -> None:
        """
        Store a key-value pair in remote storage. This is useful for retrieving
        a span or trace later on when performing online feedback or debugging.
        """
        endpoint = (
            "https://lastmileai.dev/api/evaluation_key_value_store/create"
        )

        if self.project_id is None:
            raise ValueError(
                "Project ID must be set before storing key-value pairs. Try re-initializing the tracer object"
            )

        if span_id is not None and trace_id is None:
            raise ValueError(
                "If you specify a span_id, you must also specify a trace_id"
            )

        if value_override is not None and trace_id is not None:
            raise ValueError(
                "If you specify a value_override, you cannot specify a trace_id or a span_id"
            )

        # expect value to be span id, and metadata to contain traceID
        # TODO: update data model to have traceID and spanID as separate fields
        metadata["trace_id"] = str(trace_id)  # type: ignore

        payload = {
            "projectId": self.project_id,
            "metadata": metadata,
            "value": str(span_id) or value_override,
            "key": key,
        }

        api_token = get_lastmile_api_token(None)
        response = requests.post(
            endpoint,
            json=payload,
            headers={"authorization": f"Bearer {api_token}"},
            timeout=60,  # TODO: remove hardcoded value
        )
        if not response.ok:
            raise ValueError(
                f"Error storing key-value pair: {response.json()}"
            )
        return response.json()

    def read_key_value_pair(
        self,
        key: str,
    ) -> tuple[str, str]:
        """
        Returns a pair of (TraceID, SpanID). If span_id is not found, span_id will be None

        Read a key-value pair from remote storage. This is useful for retrieving
        a span or trace later on when performing online feedback or debugging.
        """

        if self.project_id is None:
            raise ValueError(
                "Project ID must be set before storing key-value pairs. Try re-initializing the tracer object"
            )

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


def get_lastmile_tracer(
    tracer_name: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Don't make params Any type
    initial_params: Optional[dict[str, Any]] = None,
    output_filepath: Optional[str] = None,
    # TODO: Better typing later
) -> Any:
    """
    Return a tracer object that uses the OpenTelemetry SDK to instrument
    tracing in your code as well as other functionality such as logging
    the RAGQueryEvent data and registered parameters.

    See `lastmile_eval.rag.debugger.api.tracing.LastMileTracer for available
    APIs and more details

    @param tracer_name Optional(str): The name of the tracer to be used
    @param lastmile_api_token (str): Used for authentication.
        Create one from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens
    @param initial_params Optional(dict[str, Any]): The K-V pairs to be
        registered and saved with ALL traces created using the returned tracer
        object. Defaults to None (empty dict).
    @param output_filepath Optional(str): By default, trace data is exported to
        an OpenTelemetry collector and saved into a hosted backend storage such
        as ElasticSearch. However if an output_filepath is defined,
        then the trace data is saved to that file instead. This is useful for
        debugging and demo purposes, but not recommened for production use.

    @return LastMileTracer: The tracer object to log OpenTelemetry data.
    """
    token = get_lastmile_api_token(lastmile_api_token)
    provider = _LastMileTracerProvider(token, output_filepath)
    return provider.get_tracer_from_name(token, tracer_name, initial_params)


def get_trace_data(
    trace_id: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the raw trace and span data from the trace_id

    @param trace_id (str): The trace_id to get the trace data from. This is
        often the hexadecmial string representation of the trace_id int from
        the OpenTelemetry SDK.
        Ex: int_id = 123456789 -> hex value = 0x75BCD15 --> str = "75BCD15"
    @param lastmile_api_token (str): Used for authentication.
        Create one from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The trace data from the trace_id
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/trace/read?id={trace_id}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response, f"Error fetching trace data for trace_id {trace_id}"
    )
    return response.json()


def list_ingestion_trace_events(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the list of ingestion trace events. TODO: Add more filtering options

    @param take (int): The number of trace events to take. Defaults to 10
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the ingestion trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_ingestion_traces/list?pageSize={str(take)}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response,
        "Error fetching ingestion trace events for project {self.project_name}, pageSize={take}",
    )
    return response.json()


def get_latest_ingestion_trace_id(
    lastmile_api_token: Optional[str] = None,
) -> str:
    """
    Convenience function to get the latest ingestion trace id.
    You can pass in this ID into the `mark_rag_query_trace_event` method to
    link a query trace with an ingestion trace

    @param lastmile_api_token Optional(str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return str: The trace id corresponding to ingestion trace data
    """
    ingestion_traces: dict[str, Any] = list_ingestion_trace_events(
        take=1, lastmile_api_token=lastmile_api_token
    )
    # TODO: Handle errors
    ingestion_trace_id: str = ingestion_traces["ingestionTraces"][0]["traceId"]
    return ingestion_trace_id


def get_query_trace_event(
    query_trace_event_id: str,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the query trace event from the query_trace_event_id

    @param query_trace_event_id (str): The ID for the table row under which
        this RAG query trace event is stored
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the query trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_query_traces/read?id={query_trace_event_id}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response,
        f"Error fetching query trace event for id {query_trace_event_id}",
    )
    return response.json()


def list_query_trace_events(
    take: int = 10,
    lastmile_api_token: Optional[str] = None,
    # TODO: Create macro for default timeout value
    timeout: int = 60,
    # TODO: Allow a verbose option so I don't have to keep setting SHOW_DEBUG
    # to true. If we do this, we'll also have to move print statement to logger
    # ones. This is P3 imo
) -> dict[str, Any]:  # TODO: Define eplicit typing for JSON response return
    """
    Get the list of query trace events. TODO: Add more filtering options

    @param take (int): The number of trace events to take. Defaults to 10
    @param lastmile_api_token (str): Used for authentication. If not
        defined, will try to get the token from the LASTMILE_API_TOKEN
        environment variable.
        You can create a token from the "API Tokens" section from this website:
        https://lastmileai.dev/settings?page=tokens

    @return dict[str, Any]: The JSON response of the query trace events
    """
    token = get_lastmile_api_token(lastmile_api_token)
    lastmile_endpoint = f"https://lastmileai.dev/api/rag_query_traces/list?pageSize={str(take)}"
    response: Response = requests.get(
        lastmile_endpoint,
        headers={"Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    raise_for_status(
        response,
        "Error fetching query trace events for project {self.project_name}, pageSize={take}",
    )
    return response.json()


## Helper functions
def _set_trace_data(project_id: str, span: Optional[Span] = None):
    """
    Helper function to initialize trace data for a new trace.

    Helper function to set the trace_id if it hasn't
    already been initialized. This should only happen when we first start a
    new trace (create new span without a parent span attached to it)

    Also attaches the project_id to the TraceDataSingleton
    if it has not been set already. The project_id is used to log the trace data
    to the correct project in the RAG traces table.

    Args:
        span (Optional[Span]): The current span. If provided, the trace_id will
            be retrieved from the span's context.
        project_id (Optional[str]): The project ID associated with the trace.
            If provided, it will be set in the TraceDataSingleton.

    Returns:
        None
    """
    trace_data_singleton = TraceDataSingleton()
    if SHOW_DEBUG:
        trace_id_before = trace_data_singleton.trace_id
        print(f"{trace_id_before=}")

    if trace_data_singleton.trace_id is None:
        # We need to pass in a span object directly sometimes because if
        # tracer.start_span() is run as the root span without context manager
        # (with statement or annotation), it will create a new span
        # and get_current_span is not linked to the get_current_span().
        # current_span WON'T have the id of the span created by start_span
        current_span: Span = span or trace_api.get_current_span()
        trace_data_singleton.trace_id = _convert_int_id_to_hex_str(
            current_span.get_span_context().trace_id
        )
        if trace_data_singleton.project_id is None:
            trace_data_singleton.project_id = project_id
            current_span.set_attribute("projectId", project_id)

    if SHOW_DEBUG:
        trace_id_after = trace_data_singleton.trace_id
        print(f"{trace_id_after=}")


def _convert_int_id_to_hex_str(int_id: int) -> str:
    """
    Helper function to convert an integer id to a hex string. This is
    needed because Jaeger does trace and span queries using hex strings
    instead of integer values.

    Ex: int_id = 123456789 -> hex value = 0x75BCD15 --> str = "75BCD15"

    @param int_id (int): The integer id to convert to a hex string

    @return str: The hex string representation of the integer id
    """
    return str(hex(int_id)).split("x")[1]


def _log_trace_rag_events(
    lastmile_api_token: str,
    # TODO: Allow user to specify the type of rag trace (Ingestion vs. Query)
) -> Response:
    """
    Log the trace-level data to the relevant rag traces table (ingestion or
    query). This is for both structured and unstructured RAG events
    """
    # TODO: Add error handling for response
    trace_data_singleton = TraceDataSingleton()
    response = trace_data_singleton.log_to_rag_traces_table(lastmile_api_token)
    if SHOW_DEBUG:
        print("Results from rag traces create endpoint:")
        print(response.json())
    return response


def _log_span_rag_events(
    lastmile_api_token: str,
) -> None:
    """
    Log the span-level unstructured rag events
    """
    # TODO: Add error handling for response
    trace_data_singleton = TraceDataSingleton()
    trace_data_singleton.log_span_rag_events(lastmile_api_token)
    # TODO: move within internal function
    # if SHOW_DEBUG:
    #     print("Results from rag events create endpoint:")
    #     print(response.json())
    return None


def _export_log_data(lastmile_api_token: str) -> None:
    """
    Export the log data from .log() API calls to S3 and LastMile DB
    """
    trace_data_singleton = TraceDataSingleton()
    trace_data_singleton.upload_log_data(lastmile_api_token)
    return None
    # for path in self.logger_filepaths:
    #     print(path)


def _log_all_trace_events_and_reset_trace_state(
    lastmile_api_token: str,
    # TODO: Allow user to specify the type of rag trace (Ingestion vs. Query)
) -> None:
    """
    Log all the event data for both the trace and span levels.

    The trace data gets logged to the relevent trace table (RagIngestionTrace
    or RagQueryTrace) and can include both unstructured and structured data
    formats.

    The span data gets logged to the RagEvents table and is unstructured.

    After this is finished, we reset the trace state
    """

    _log_trace_rag_events(lastmile_api_token)
    _log_span_rag_events(lastmile_api_token)
    _export_log_data(lastmile_api_token)
    # TODO: Export logs

    # Reset current trace data so we can start a
    # new trace in a fresh state
    trace_data_singleton = TraceDataSingleton()
    trace_data_singleton.reset()
    return


def convert_to_context(
    context: Union[SpanContext, Context, str, None]
) -> Union[Context, None]:
    """
    Converts a SpanContext or Context object into a Context object.

    @param context (Union[SpanContext, Context, str]): The context to normalize
    """
    if isinstance(context, str):
        try:
            span_context_dict = json.loads(context)
            span_context_dict["trace_state"] = TraceState.from_header(
                span_context_dict["trace_state"]
            )
            span_context_dict["trace_flags"] = TraceFlags(
                span_context_dict["trace_flags"]
            )
            span_context = SpanContext(**span_context_dict)
            context = span_context  # handle Span Context below
        except Exception as exc:
            raise ValueError(
                f"Malformed context string {context}. Please pass in a valid deserialized SpanContext object by calling `export_span()`"
            ) from exc

    if context is None:
        return
    if isinstance(context, SpanContext):
        non_recording_span = trace_api.NonRecordingSpan(context)
        return trace_api.set_span_in_context(non_recording_span)
    return context


def export_span(span: Span) -> str:
    """
    Return a serialized representation of the span that can be used to start subspans in other places. See `Span.start_span` for more details.
    """
    span_context = span.get_span_context()
    span_context_dict = {
        "trace_id": span_context.trace_id,
        "span_id": span_context.span_id,
        "trace_flags": span_context.trace_flags,
        "trace_state": span_context.trace_state.to_header(),
        "is_remote": span_context.is_remote,
    }

    return json.dumps(span_context_dict)


def get_span_id(span: Optional[Span] = None) -> int:
    """
    Get the span ID from the provided span object.

    If no span object is provided, the span ID is retrieved from the current span.

    Args:
        span: The span object to retrieve the span ID from. Defaults to None.

    Returns:
        The span ID as an integer.
    """
    if span:
        return span.get_span_context().span_id

    current_span: Span = trace_api.get_current_span()
    return current_span.get_span_context().span_id


def get_trace_id(span: Optional[Span] = None) -> int:
    """
    Get the trace ID from the provided span object.

    If no span object is provided, the trace ID is retrieved from the current span.

    Args:
        span: The span object to retrieve the trace ID from. Defaults to None.

    Returns:
        The trace ID as an integer.
    """
    if span:
        return span.get_span_context().trace_id

    current_span: Span = trace_api.get_current_span()
    return current_span.get_span_context().trace_id


def raise_for_status(response: Response, message: str) -> None:
    """
    Raise an HTTPError exception if the response is not successful
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(f"{message}: {response.content}") from e
