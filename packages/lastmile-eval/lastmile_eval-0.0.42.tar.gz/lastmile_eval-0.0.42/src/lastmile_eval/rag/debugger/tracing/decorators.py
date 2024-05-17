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
