import json
from copy import deepcopy
from typing import Any, Dict, Optional, get_args

from enum import Enum
import requests
from requests import Response

from lastmile_eval.rag.debugger.api import RAGIngestionEvent, RAGQueryEvent

from ..common.core import ParamInfoKey, RAGTraceType, RagQueryEventName
from ..common.utils import Singleton, SHOW_DEBUG

ALLOWED_RAG_QUERY_EVENTS = get_args(RagQueryEventName)


class TraceDataSingleton(Singleton):
    """
    Singleton object to store trace-level data. By delegating the state
    management to this class, we also ensure that it is not out of sync
    when shared across multiple classes.

    For example, this is used to reference the same data in
    LastMileOTLSpanExporter and _LastMileTracer
    """

    _is_already_initialized = False

    def __init__(self, global_params: Optional[dict[str, Any]] = None):
        if self._is_already_initialized:
            return

        super().__init__()

        # This connects to dict global_params, which will get updated whenever trace is not defined (which is what we want)
        if global_params is not None:
            self.global_params = {
                ParamInfoKey(k): v for (k, v) in global_params.items()
            }
        else:
            self.global_params = {}

        self.trace_specific_params = deepcopy(self.global_params)

        self.rag_events: dict[str, Any] = {}
        # TODO: Change type from dict to class with explicit field and schema
        self.rag_event_sequence: list[dict[str, Any]] = []
        self._added_spans: set[str] = set()
        self._rag_event_for_trace: Optional[dict[str, Any]] = None

        self._rag_trace_type: Optional[RAGTraceType] = None

        # To populate later when we first create a span using one of
        # these two methods:
        #   1) `lastmile_tracer.start_as_current_span()`
        #   2) `lastmile_tracer.start_span()`
        # See opentelemetry.sdk.trace for their SDK API
        self._trace_id: Optional[str] = None

        self._is_already_initialized = True

    # TODO: Centralize this with `add_rag_query_event` once we
    # have defined ingestion events and can share nearly all logic
    def add_rag_ingestion_event(self, _event: RAGIngestionEvent) -> None:
        """
        Add RagIngestionEvent to the trace-level data
        """
        if self._rag_trace_type == "Query":
            raise ValueError(
                "You have already marked a RAGQueryEvent in this trace. Please check for other calls to `mark_rag_query_trace_event()` within the same trace and either remove them, or do not implement `mark_rag_ingestion_trace_event()`"
            )
        if self.trace_id is None:
            raise ValueError(
                "You must be inside of a trace in order to log a RagQueryEvent"
            )

        # TODO: Add event validation checks once we have ingestion event types
        # event_class_name = type(event).__name__
        event_class_name = "MockIngestionEventPerformed"
        # if event_class_name not in ALLOWED_RAG_QUERY_EVENTS:
        #     raise ValueError(
        #         f"You must log a defined RagQueryEvent type. You are trying to log '{event_class_name}'. Acceptable event types are: {ALLOWED_RAG_QUERY_EVENTS}"
        #     )

        # TODO: Check if we've already stored this event type in the trace
        # and raise ValueError if we have

        # TODO: Use .model_dump_json() once we have ingestion events
        # event_json = event.model_dump_json()
        event_json = json.dumps({"data": "Mock ingestion event data"})
        self.rag_events[event_class_name] = event_json
        self._rag_trace_type = "Ingestion"

    def add_rag_query_event(self, event: RAGQueryEvent) -> None:
        """
        Add RagQueryEvent to the trace-level data
        """
        # TODO: Implement Enum instead of string literal
        if self._rag_trace_type == "Ingestion":
            raise ValueError(
                "You have already marked a RAGIngestionEvent in this trace. Please check for other calls to `mark_rag_ingestion_trace_event()` within the same trace and either remove them, or do not implement `mark_rag_query_trace_event()`"
            )

        if self.trace_id is None:
            raise ValueError(
                "You must be inside of a trace in order to log a RagQueryEvent"
            )

        event_class_name = type(event).__name__
        if event_class_name not in ALLOWED_RAG_QUERY_EVENTS:
            raise ValueError(
                f"You must log a defined RagQueryEvent type. You are trying to log '{event_class_name}'. Acceptable event types are: {ALLOWED_RAG_QUERY_EVENTS}"
            )
        # TODO: Check if we've already stored this event type in the trace
        # and raise ValueError if we have
        event_json = event.model_dump_json()
        self.rag_events[event_class_name] = event_json
        self._rag_trace_type = "Query"

    def add_rag_event_for_span(
        self,
        # TODO: Explicit schema for event_payload
        event_payload: dict[str, Any],
    ) -> None:
        """
        Add RagEvent to the trace-level data. Duplicate from
        add_rag_query_event for now just to get unblocked
        """
        span_id = event_payload.get("span_id")
        if span_id is None:
            raise ValueError("Could not extract span_id from event payload")
        if span_id in self._added_spans:
            raise ValueError(
                f"You have already added an event for span id '{span_id}'. Please check for other calls to `add_rag_event_for_span()` within the same span and either remove them, or explicitly pass the `span_id` argument in `add_rag_event_for_span()`."
            )
        if self.trace_id is None:
            raise ValueError(
                "Unable to detect current trace_id. You must be inside of a trace in order to log a RagEvent"
            )

        self._added_spans.add(span_id)
        self.rag_event_sequence.append(event_payload)

    def add_rag_event_for_trace(
        self,
        # TODO: Explicit schema for event_payload
        event_payload: dict[str, Any],
    ) -> None:
        """
        Add RagEvent to the trace-level data. Same functionality as
        `add_rag_event_for_span` except this is used for the overall
        trace-level data instead of at the span level.
        """
        if self.trace_id is None:
            raise ValueError(
                "Unable to detect current trace_id. You must be inside of a trace in order to log a RagEvent"
            )
        if self._rag_event_for_trace is not None:
            raise ValueError(
                f"You have already added an event for trace id '{self.trace_id}'. Please check for other calls to `add_rag_event_for_trace()` within the same trace."
            )
        self._rag_event_for_trace = event_payload

    def get_params(self) -> dict[str, Any]:
        """
        Get the parameters saved in the trace-level data (which is the same as
        global if no trace exists)
        """
        return {str(k): v for (k, v) in self.trace_specific_params.items()}

    def register_param(self, key: str, value: Any) -> None:
        """
        Register a parameter to the trace-level data (and global params if no
        trace is defined). If the key is already defined, create a new key
        which is "key-1", "key-2", etc.
        """
        # Use string literals instead of enums because if we have the same key
        # we want to be able to differentiate them more easily
        # (ex: "chunks" vs. "chunks-1") instead of comparing enums
        # (ex: "EventPayload.CHUNKS" vs. "chunks-1")
        if isinstance(key, Enum):
            key = key.value

        param_key = ParamInfoKey(key)
        should_write_to_global = False
        if self.trace_id is None:
            should_write_to_global = True

        # Even if trace_id is None (not in a trace), we still need to update
        # trace_specific_params so it's not out of sync with global_params

        # For auto-instrumentation, we have tons of events with the same
        # event_name so adding more specific parameters there
        if param_key in self.trace_specific_params:
            i = 1
            while param_key + "-" + str(i) in self.trace_specific_params:
                i += 1
            param_key = ParamInfoKey(param_key + "-" + str(i))
        self.trace_specific_params[param_key] = value

        if should_write_to_global:
            param_key = ParamInfoKey(key)
            if param_key in self.global_params:
                i = 1
                while param_key + "-" + str(i) in self.global_params:
                    i += 1
                param_key = ParamInfoKey(param_key + "-" + str(i))
            self.global_params[param_key] = value

    def clear_params(
        self,
        should_clear_global_params: bool = False,
    ) -> None:
        """
        Clear the parameters saved in the trace-level data, as well as
        global params if `should_clear_global_params` is true.
        """
        self.trace_specific_params.clear()
        if should_clear_global_params:
            self.global_params.clear()

    def log_to_rag_traces_table(self, lastmile_api_token: str) -> Response:
        """
        Log the trace-level data to the RagIngestionTraces or RagQueryTraces
        table via the respective LastMile endpoints. This logs data that
        was added to the singleton via one of these methods:
            1. `add_rag_query_event`
            2. `add_rag_ingestion_event`
            3. `add_rag_event_for_trace`

        @param lastmile_api_token (str): Used for authentication.
            Create one from the "API Tokens" section from this website:
            https://lastmileai.dev/settings?page=tokens

        @return Response: The response from the LastMile endpoint
        """
        if self.trace_id is None:
            raise ValueError(
                "Unable to detect trace id. Please create a root span using `tracer.start_as_current_span()`"
            )

        payload: dict[str, Any] = {}
        if self._rag_event_for_trace is not None:
            payload["input"] = self._rag_event_for_trace.get("input") or ""
            payload["output"] = self._rag_event_for_trace.get("output") or ""
            payload["eventData"] = (
                self._rag_event_for_trace.get("event_data") or {}
            )

        if self._rag_trace_type == "Ingestion":
            payload.update(
                {
                    "traceId": self.trace_id,
                    "paramSet": self.get_params(),
                    # TODO: Add fields below
                    # projectId
                    # metadata
                    # orgId
                    # visibility
                }
            )
            if SHOW_DEBUG:
                print(f"TraceDataSingleton.log_to_traces_table: {payload=}")

            response = requests.post(
                "https://lastmileai.dev/api/rag_ingestion_traces/create",
                headers={"Authorization": f"Bearer {lastmile_api_token}"},
                json=payload,
                timeout=60,  # TODO: Remove hardcoding
            )
            return response

        # Default to RAGQueryTraces if RagEventType is unspecified
        query = self._get_rag_query_event("QueryReceived") or json.dumps({})
        context_retrieved = self._get_rag_query_event(
            "ContextRetrieved"
        ) or json.dumps({})
        fully_resolved_prompt = self._get_rag_query_event(
            "PromptResolved"
        ) or json.dumps({})
        output = (
            # Prioritize structured data over unstructured
            self._get_rag_query_event("LLMOutputReceived")
            or payload.get("output")
            or ""
        )

        payload.update(
            {
                "traceId": self.trace_id,
                "query": query,
                "context": context_retrieved,
                "fullyResolvedPrompt": fully_resolved_prompt,
                "output": output,
                "paramSet": self.get_params(),
                # TODO: Add fields below
                # ragInjectionTraceId
                # metadata
                # orgId
                # visibility
            }
        )

        if SHOW_DEBUG:
            print(f"TraceDataSingleton.log_to_rag_traces_table {payload=}")

        response: Response = requests.post(
            "https://lastmileai.dev/api/rag_query_traces/create",
            headers={"Authorization": f"Bearer {lastmile_api_token}"},
            json=payload,
            timeout=60,  # TODO: Remove hardcoding
        )
        return response

    def log_span_rag_events(self, lastmile_api_token: str) -> None:
        if not self.rag_event_sequence:
            return

        if self.trace_id is None:
            raise ValueError(
                "Unable to detect trace id. Please create a root span using `tracer.start_as_current_span()`"
            )

        for event_payload in self.rag_event_sequence:
            # TODO: Schematize event data payload
            payload = {
                # Required fields by user (or auto-instrumentation)
                "eventName": event_payload["event_name"] or "",
                "input": event_payload["input"] or {},
                "output": event_payload["output"] or {},
                "eventData": event_payload["event_data"] or {},
                "metadata": {} or "",  # TODO: Allow user to define metadata
                # Required but get this from our data when marking event
                "traceId": self.trace_id,
                "spanId": event_payload["span_id"],
                # TODO: Add fields below
                # projectId
                # orgId
                # visibility
            }
            if SHOW_DEBUG:
                print(f"TraceDataSingleton.log_span_rag_events: {payload=}")

            requests.post(
                "https://lastmileai.dev/api/rag_events/create",
                headers={"Authorization": f"Bearer {lastmile_api_token}"},
                json=payload,
                timeout=60,  # TODO: Remove hardcoding
            )
            # TODO: Add error handling
        return None

    def reset(self) -> None:
        """
        Reset the trace-level data
        """
        self.trace_specific_params = deepcopy(self.global_params)
        self.trace_id = None
        self.rag_events.clear()
        self.rag_event_sequence = []
        self._added_spans.clear()
        self._rag_trace_type = None
        self._rag_event_for_trace = None

    @property
    def trace_id(  # pylint: disable=missing-function-docstring
        self,
    ) -> Optional[str]:
        return self._trace_id

    @trace_id.setter
    def trace_id(self, value: Optional[str]) -> None:
        self._trace_id = value

    def _get_rag_query_event(self, event_class_name: str) -> Optional[str]:
        """
        Get the JSON string representation of the RagQueryEvent for a given
        RagQueryEventName. If RagQueryEventName is not registered in the
        rag_query_events, we return None
        """
        if event_class_name not in ALLOWED_RAG_QUERY_EVENTS:
            raise ValueError(
                f"Unable to detect RAGQueryEvent from '{event_class_name}'. Acceptable event types are: {ALLOWED_RAG_QUERY_EVENTS}"
            )
        return self.rag_events.get(event_class_name)
