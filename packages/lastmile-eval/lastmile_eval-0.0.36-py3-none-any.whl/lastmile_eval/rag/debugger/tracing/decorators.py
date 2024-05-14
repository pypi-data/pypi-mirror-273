from functools import wraps
import inspect
import json
from typing import Any, Callable, Optional, Sequence, Union
from opentelemetry import context as context_api
from opentelemetry.trace import SpanContext
from opentelemetry.util import types
from opentelemetry import trace as trace_api
from ..api import LastMileTracer


def _check_json_serializable(event):
    try:
        return json.dumps(event)
    except TypeError as e:
        raise Exception(
            f"All logged values must be JSON-serializable: {event}"
        ) from e


def _try_log_input(span, f_sig, f_args, f_kwargs):
    input_serializable = _get_serializable_input(f_sig, f_args, f_kwargs)
    span.set_attribute("input", json.dumps(input_serializable))


def _get_serializable_input(signature, args, kwargs):
    bound_args = signature.bind(*args, **kwargs).arguments
    input_serializable = bound_args
    try:
        _check_json_serializable(bound_args)
    except Exception as e:
        input_serializable = "<input not json-serializable>: " + str(e)
    return input_serializable


def _try_log_output(span, output):
    output_serializable = _get_serializable_output(output)
    span.set_attribute("output", json.dumps(output_serializable))


def _get_serializable_output(output):
    output_serializable = output
    try:
        _check_json_serializable(output)
    except Exception as e:
        output_serializable = "<output not json-serializable>: " + str(e)
    return output_serializable


def traced(
    tracer: LastMileTracer,
    name: Optional[str] = None,
    context: Optional[Union[context_api.Context, SpanContext, str]] = None,
    kind: trace_api.SpanKind = trace_api.SpanKind.INTERNAL,
    attributes: types.Attributes = None,
    links: Optional[Sequence[trace_api.Link]] = None,
    start_time: Optional[int] = None,
    record_exception: bool = True,
    set_status_on_exception: bool = True,
    end_on_exit: bool = True,
):
    """
    Decorator that provides the same functionality as
    LastMileTracer.start_as_current_span except that it also logs the wrapped
    function's input and output values as attributes on the span.
    """

    def decorator(func: Callable[..., ...]):
        f_sig = inspect.signature(func)

        @wraps(func)
        def wrapper_sync(*f_args, **f_kwargs):
            with tracer.start_as_current_span(
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

        @wraps(func)
        async def wrapper_async(*f_args, **f_kwargs):
            with tracer.start_as_current_span(
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
                return_value = await func(*f_args, **f_kwargs)
                _try_log_output(span, return_value)
                return return_value

        if inspect.iscoroutinefunction(func):
            return wrapper_async
        else:
            return wrapper_sync

    return decorator
