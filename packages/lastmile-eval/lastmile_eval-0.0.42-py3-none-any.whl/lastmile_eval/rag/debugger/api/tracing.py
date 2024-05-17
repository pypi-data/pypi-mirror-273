import abc
from contextlib import contextmanager
from dataclasses import dataclass
from logging import Logger
from typing import Any, Callable, Iterator, Optional, Sequence, Union

from opentelemetry import context as context_api
from opentelemetry import trace as trace_api
from opentelemetry.trace import SpanContext
from opentelemetry.trace.span import Span
from opentelemetry.util import types

from ..common import query_trace_types

# Public API for logging


RAGQueryEvent = (
    query_trace_types.QueryReceived
    | query_trace_types.ContextRetrieved
    | query_trace_types.PromptResolved
    | query_trace_types.LLMOutputReceived
)

# TODO: Define later what the injestion_trace_types should be
RAGIngestionEvent = str | list[str]


@dataclass(frozen=True)
class RAGTraceEventResult:
    """
    Return type from marking a RAGQueryEvent or RAGIngestionEvent in a trace
    """

    is_success: bool
    message: str


class LastMileTracer(abc.ABC):
    """
    A tracer proxy around OpenTelemetry tracer. It has 3 main functionalities:

    1. Create span data and attach it to the tracer. This is the same API as
        OpenTelemetry's tracer:
            a. `start_as_current_span()`
            b. `start_span()`
    2. Mark RAG events and store their states (see `RAGQueryEvent` and
        `RAGIngestionEvent`) alongside the trace data. The methods for this are:
            a. `mark_rag_ingestion_trace_event`
            b. `mark_rag_query_trace_event`
    3. Register a dictionary of parameters to be logged and associated with
        the trace data. The methods for this are:
            a. `register_param()`
            b. `get_params()`
    """

    @abc.abstractmethod
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
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...

    @abc.abstractmethod
    @contextmanager
    def start_as_current_span(  # pylint: disable=too-many-locals
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
        """
        Same API as opentelemetry.trace.Tracer.start_as_current_span
        But also allows a SpanContext to be passed in as the context parameter.
        If context is a string, it is assumed to be a serialized SpanContext

        Just like the OpenTelemetry API, this method can be used as both a
        context manager and a decorator.
        ```
        from opentelemetry import trace as trace_api
        from lastmile_eval.rag.debugger.tracing import get_lastmile_tracer

        tracer: LastMileTracer = get_lastmile_tracer(
            tracer_name="<my-tracer-name>",
            lastmile_api_token="<my-api-token>"
        )

        # Context Manager
        with tracer.start_as_current_span("my-span") as span:
            span.set_attribute("<my-key>", "<my-value>")

        # Decorator
        @tracer.start_as_current_span("my-span")
        def my_function():
            span = trace_api.get_current_span()
            span.set_attribute("<my-key>", "<my-value>")
        ```

        If you are using this as a decorator instead of context manager, it's
        recommended to use `@traced(tracer)` instead since that also logs the
        wrapped method's inputs and outputs as span attributes:
        ```
        from lastmile_eval.rag.debugger.tracing.decorators import traced

        # Recommended way of decorating a function
        @traced(tracer)
        def my_function(my_arg: str):
            # my_arg is automatically added to the span attributes

            span = trace_api.get_current_span()
            span.set_attribute("<my-key>", "<my-value>")
            ...

            # output_value is automatically added to the span attributes too
            return output_value
        ```
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
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
        """
        Same API as opentelemetry.trace.Tracer.start_span
        But also allows a SpanContext to be passed in as the context parameter.
        If context is a string, it is assumed to be a serialized SpanContext
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    def mark_rag_ingestion_trace_event(
        self,
        event: RAGIngestionEvent,
        # TODO: Add ability to add metadata in the event attributes
    ) -> RAGTraceEventResult:
        """
        Mark a RAGIngestionEvent in your ingestion trace. Each trace can contain
        multiple events, but can only contain each type of RAGIngestionEvent at
        most once. If you try to mark the same type of event multiple times in
        the same trace, this method returns a ValueError.

        These events get logged into the database connected to the
        LastMileTracerProvider when the trace is finished (exiting its root
        span).

        None of the events are strictly required to be included in your trace.
        If any of the events from RAGIngestionEvent were not marked they will
        be stored as an empty JSON.

        @param event (RAGIngestionEvent): An event object containing data about
            the state of the RAG LLM system

        @return RAGTraceEventResult: Flag indicating whether the event was
            marked successfully
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    def mark_rag_query_trace_event(
        self,
        event: RAGQueryEvent,
        # TODO: Add ability to add metadata in the event attributes
        indexing_trace_id: str | None = None,
        # TODO: Allow test_set_id to be a list so we can save this trace to
        # multiple test sets if we want
        # TODO: Add ability to link to test_set_id once test set API is built.
        # See https://github.com/lastmile-ai/eval/issues/113
        # test_set_id: str | None = None,
    ) -> RAGTraceEventResult:
        """
        Mark a RAGQueryEvent in your retrieval trace. Each trace can contain
        multiple events, but can only contain each type of RAGQueryEvent at
        most once. If you try to mark the same type of event multiple times in
        the same trace, this method returns a ValueError.

        These events get logged into the database connected to the
        LastMileTracerProvider when the trace is finished (exiting its root
        span).

        None of the events are strictly required to be included in your trace.
        If any of the events from RAGQueryEvent were not marked they will be
        stored as an empty JSON.

        @param event (RAGQueryEvent): An event object containing data about
            the state of the RAG LLM system
        @param test_set_id Optional(str): If traces are to be evaluated in the
            future, they can be grouped together under a test set where each
            trace (along with its marked RAG events) represents a single test
            case in that test set. The test set can be used to run evaluation
            metrics on each trace, as well as run aggregated metric
            evaluations afterwards. Defaults to None.
        @param indexing_trace_id Optional(str): The trace ID of a trace that
            was logged when previously running the ingestion (indexing and
            data storage) process for the documents used in the RAG retrieval
            step. Defaults to None.

        @return RAGTraceEventResult: Flag indicating whether the event was
            marked successfully
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def get_params(self) -> dict[str, Any]:
        """
        Returns the params_dict that contains all the parameters that have been
        registered with a trace so far.

        If this is called outside of an active trace, it will return the
        global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def register_param(
        self,
        key: str,
        value: Any,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Define the parameter K-V pair to save for the current trace instance.

        If this is called outside of an active trace, it will save this into
        a global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)

        @param key (str): The name of the parameter to be saved
        @param value (Any): The value of the parameter to be saved
        @param should_also_save_in_span (bool): Whether to also save this K-V
            pair in the current span attributes data. Defaults to true
        @param span Optional(Span): The span to save the K-V pair in
            addition to regular paramSet. This can be helpful for debugging
            when going through the trace. Only has an effect if
            should_also_save_in_span is true. Defaults to
            `trace_api.get_current_span()` which is the most recent span
            generated by calling tracer.start_as_current_span
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def register_params(
        self,
        params: dict[str, Any],
        should_overwrite: bool = False,
        should_also_save_in_span: bool = True,
        span: Optional[Span] = None,
    ) -> None:
        """
        Helper function for individually calling `register_param`, with the
        added capability of clearing existing parameters if they exist.

        If this is called outside of an active trace, it will save these into
        a global params dict that contains K-V pairs that will be common in all
        future traces (if they haven't been cleared via `clear_params()`)

        @param params dict[str, Any]: The parameter K-V pairs to save
        @param should_also_save_in_span (bool): Whether to also save this K-V
            pair in the current span attributes data. Defaults to true
        @param should_overwrite (bool): Whether to clear existing parameters
            if they already exist. Defaults to false.
        @param span Optional(Span): The span to save the K-V pair in
            addition to regular paramSet. This can be helpful for debugging
            when going through the trace. Only has an effect if
            should_also_save_in_span is true. Defaults to
            `trace_api.get_current_span()` which is the most recent span
            generated by calling tracer.start_as_current_span

        Define the parameter K-V pair to save for the current trace instance
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def clear_params(
        self,
        should_clear_global_params: bool = False,
    ) -> None:
        """
        Clearing all existing parameters for the current trace instance.

        If this is called outside of an active trace, it will only clear the
        global params dict if `should_clear_global_params` is set to True.

        @param should_clear_global_params (bool): Whether to clear the global
        K-V pairs in addition to the current trace params. Defaults to false
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def add_rag_event_for_span(
        self,
        event_name: str,
        span: Optional[Span] = None,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[dict[Any, Any]] = None,
    ) -> None:
        """
        Add a RagEvent for a specific span within a trace. This event gets
        saved at the end of the trace to the RagEvents table, where you can use
        these events to generate test cases and run evaluation metrics on them.
        To run evaluations, you can either use the (`input`, `output`) data
        fields explicitly, or you can use the unstructured `event_data` JSON.

        If all three of those fields aren't included (`input`, `output`,
        `event_data`), an error will be thrown.

        You can only call this method once per span, otherwise it will raise
        an error.

        @param event_name (str): The name of the event
        @param span Optional(Span): The span to add the event to. If None, then
            we use the current span
        @param input Optional(dict[Any, Any]): The input data for the event
        @param output Optional(dict[Any, Any]): The output data for the event
        @param event_data Optional(dict[Any, Any]): The unstructured event data
            in JSON format where you can customize what fields you want to use
            later in your evaluation metrics
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def add_rag_event_for_trace(
        self,
        event_name: str,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[dict[Any, Any]] = None,
    ) -> None:
        """
        This is the same functionality as `add_rag_event_for_span()` except
        this is for recording events at the overall trace level. This is useful
        in case you want to run evaluations on the entire trace, rather than
        individual span events.

        You can only call this method once per trace, otherwise it will raise
        an error.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def log(
        self,
        data: Any,
        # TODO: Accept str argument for user to save locally to a local file
        # logger: Optional[Union[Logger, str]] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        """
        Pass in data to be logged into a separate logger. This is useful if you
        don't want to explicitly save data into span attributes, rag events, or
        param sets, but still want to log it anyways to look at later such as
        warnings, errors, or debugging info. These logs are saved to the
        LastMile database and can be accessed later when looking at trace data
        in the UI debugging tool.

        @param data (Any): The data to be logged. It gets converted to string
            format using the repr() function
        @param logger Optional(Union[Logger, str]): The logger to use for
            saving the data to. If it's a str, we assume it's the name of a
            filepath. You can have multiple loggers across different calls to
            save data to different places.
            If not defined, we use the default logger associated with
            the tracer and all the data from log calls get saved together.
        """
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
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
        raise NotImplementedError("Not implemented directly, this is an API")

    @abc.abstractmethod
    def store_trace_id(
        self,
        key: str,
        trace_id: int,
        span_id: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = None,
        value_override: Any = None,  # TODO: restrict or remove
    ) -> None:
        """
        Store a key-value pair in remote storage. This is useful for retrieving
        a span or trace later on when performing online feedback or debugging.
        """

    @abc.abstractmethod
    def read_trace_id(
        self,
        key: str,
    ) -> Any:
        """
        Read a key-value pair from remote storage. This is useful for retrieving
        a span or trace later on when performing online feedback or debugging.
        """
