import json
from functools import wraps
from typing import Optional, Callable, Unpack

from syntrac_opentelemetry.semconv.ai import SpanAttributes, SyntracSpanKindValues

from syntrac.sdk.tracing import get_tracer
from syntrac.sdk.tracing.tracing import TracerWrapper
from syntrac.sdk.utils import camel_to_snake, serialise_to_json

from syntrac.sdk.decorators.helper import (
    _should_send_prompts,
    SharedKwargs,
    SharedKwargsWithHooks,
    add_extra_spans
)


def task(
    name: Optional[str] = None,
    method_name: Optional[str] = None,
    tlp_span_kind: Optional[SyntracSpanKindValues] = SyntracSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    if method_name is None:
        return task_method(
            name=name,
            tlp_span_kind=tlp_span_kind,
            **kwargs
        )
    else:
        return task_class(
            name=name,
            method_name=method_name,
            tlp_span_kind=tlp_span_kind,
            **kwargs
        )


def task_method(
    name: Optional[str] = None,
    tlp_span_kind: Optional[SyntracSpanKindValues] = SyntracSpanKindValues.TASK,
    input_serializer: Optional[Callable] = None,
    output_serializer: Optional[Callable] = None,
    **wkwargs: Unpack[SharedKwargs]
):
    def decorate(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            if not TracerWrapper.verify_initialized():
                return fn(*args, **kwargs)

            span_name = (
                f"{name}.{tlp_span_kind.value}"
                if name
                else f"{fn.__name__}.{tlp_span_kind.value}"
            )
            with get_tracer() as tracer:
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute(
                        SpanAttributes.SYNTRAC_SPAN_KIND, tlp_span_kind.value
                    )
                    span.set_attribute(SpanAttributes.SYNTRAC_ENTITY_NAME, name)
                    add_extra_spans(span, **wkwargs)

                    try:
                        if _should_send_prompts():
                            if input_serializer:
                                input = input_serializer(*args, **kwargs)
                            else:
                                input = serialise_to_json({"args": args, "kwargs": kwargs})
                            span.set_attribute(
                                SpanAttributes.SYNTRAC_ENTITY_INPUT,
                                input,
                            )
                    except TypeError:
                        pass  # Some args might not be serializable

                    res = fn(*args, **kwargs)

                    try:
                        if _should_send_prompts():
                            output = output_serializer(res) if output_serializer else json.dumps(res)
                            span.set_attribute(
                                SpanAttributes.SYNTRAC_ENTITY_OUTPUT,
                                output
                            )
                    except TypeError:
                        pass  # Some outputs might not be serializable

                    return res

        return wrap

    return decorate


def task_class(
    name: Optional[str],
    method_name: str,
    tlp_span_kind: Optional[SyntracSpanKindValues] = SyntracSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    def decorator(cls):
        task_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(
            cls,
            method_name,
            task_method(name=task_name, tlp_span_kind=tlp_span_kind, **kwargs)(method),
        )
        return cls

    return decorator


# Async Decorators
def atask(
    name: Optional[str] = None,
    method_name: Optional[str] = None,
    tlp_span_kind: Optional[SyntracSpanKindValues] = SyntracSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    if method_name is None:
        return atask_method(name=name, tlp_span_kind=tlp_span_kind, **kwargs)
    else:
        return atask_class(
            name=name, method_name=method_name, tlp_span_kind=tlp_span_kind, **kwargs
        )


def atask_method(
    name: Optional[str] = None,
    tlp_span_kind: Optional[SyntracSpanKindValues] = SyntracSpanKindValues.TASK,
    input_serializer: Optional[Callable] = None,
    output_serializer: Optional[Callable] = None,
    **wkwargs: Unpack[SharedKwargs]
):
    def decorate(fn):
        @wraps(fn)
        async def wrap(*args, **kwargs):
            if not TracerWrapper.verify_initialized():
                return await fn(*args, **kwargs)

            span_name = (
                f"{name}.{tlp_span_kind.value}"
                if name
                else f"{fn.__name__}.{tlp_span_kind.value}"
            )
            with get_tracer() as tracer:
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute(
                        SpanAttributes.SYNTRAC_SPAN_KIND, tlp_span_kind.value
                    )
                    span.set_attribute(SpanAttributes.SYNTRAC_ENTITY_NAME, name)
                    add_extra_spans(span, **wkwargs)

                    try:
                        if _should_send_prompts():
                            if input_serializer:
                                input = input_serializer(*args, **kwargs)
                            else:
                                input = serialise_to_json({"args": args, "kwargs": kwargs})
                            span.set_attribute(
                                SpanAttributes.SYNTRAC_ENTITY_INPUT,
                                input,
                            )
                    except TypeError:
                        pass  # Some args might not be serializable

                    res = await fn(*args, **kwargs)

                    try:
                        if _should_send_prompts():
                            output = output_serializer(res) if output_serializer else json.dumps(res)
                            span.set_attribute(
                                SpanAttributes.SYNTRAC_ENTITY_OUTPUT,
                                output,
                            )
                    except TypeError:
                        pass  # Some args might not be serializable

                    return res

        return wrap

    return decorate


def atask_class(
    name: Optional[str],
    method_name: str,
    tlp_span_kind: Optional[SyntracSpanKindValues] = SyntracSpanKindValues.TASK,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    def decorator(cls):
        task_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(
            cls,
            method_name,
            atask_method(name=task_name, tlp_span_kind=tlp_span_kind, **kwargs)(method),
        )
        return cls

    return decorator


def agent(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return task(
        name=name, method_name=method_name, tlp_span_kind=SyntracSpanKindValues.AGENT, **kwargs
    )


def tool(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return task(
        name=name, method_name=method_name, tlp_span_kind=SyntracSpanKindValues.TOOL, **kwargs
    )


def aagent(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return atask(
        name=name, method_name=method_name, tlp_span_kind=SyntracSpanKindValues.AGENT, **kwargs
    )


def atool(name: Optional[str] = None, method_name: Optional[str] = None, **kwargs: Unpack[SharedKwargsWithHooks]):
    return atask(
        name=name, method_name=method_name, tlp_span_kind=SyntracSpanKindValues.TOOL, **kwargs
    )
