import json
from functools import wraps
from typing import Optional, Callable, Unpack

from syntrac_opentelemetry.semconv.ai import SpanAttributes, SyntracSpanKindValues

from syntrac.sdk.tracing import get_tracer, set_workflow_name
from syntrac.sdk.tracing.tracing import TracerWrapper
from syntrac.sdk.utils import camel_to_snake, serialise_to_json
from syntrac.sdk.decorators.helper import _should_send_prompts, SharedKwargs, SharedKwargsWithHooks, add_extra_spans


def workflow(
    name: Optional[str] = None,
    method_name: Optional[str] = None,
    correlation_id: Optional[str] = None,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    if method_name is None:
        return workflow_method(name=name, correlation_id=correlation_id, **kwargs)
    else:
        return workflow_class(
            name=name, method_name=method_name, correlation_id=correlation_id, **kwargs
        )


def workflow_method(
    name: Optional[str] = None,
    correlation_id: Optional[str] = None,
    input_serializer: Optional[Callable] = None,
    output_serializer: Optional[Callable] = None,
    **wkwargs: Unpack[SharedKwargs]
):
    def decorate(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            if not TracerWrapper.verify_initialized():
                return fn(*args, **kwargs)

            workflow_name = name or fn.__name__
            set_workflow_name(workflow_name)
            span_name = f"{workflow_name}.workflow"

            with get_tracer(flush_on_exit=True) as tracer:
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute(
                        SpanAttributes.SYNTRAC_SPAN_KIND,
                        SyntracSpanKindValues.WORKFLOW.value,
                    )
                    span.set_attribute(SpanAttributes.SYNTRAC_ENTITY_NAME, name)
                    if correlation_id:
                        span.set_attribute(
                            SpanAttributes.SYNTRAC_CORRELATION_ID, correlation_id
                        )

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
                                SpanAttributes.SYNTRAC_ENTITY_OUTPUT, output
                            )
                    except TypeError:
                        pass  # Some outputs might not be serializable

                    return res

        return wrap

    return decorate


def workflow_class(
    name: Optional[str],
    method_name: str,
    correlation_id: Optional[str] = None,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    def decorator(cls):
        workflow_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(
            cls,
            method_name,
            workflow_method(name=workflow_name, correlation_id=correlation_id, **kwargs)(method),
        )
        return cls

    return decorator


def aworkflow(
    name: Optional[str] = None,
    method_name: Optional[str] = None,
    correlation_id: Optional[str] = None,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    if method_name is None:
        return aworkflow_method(name=name, correlation_id=correlation_id, **kwargs)
    else:
        return aworkflow_class(
            name=name, method_name=method_name, correlation_id=correlation_id, **kwargs
        )


def aworkflow_method(
    name: Optional[str] = None,
    correlation_id: Optional[str] = None,
    input_serializer: Optional[Callable] = None,
    output_serializer: Optional[Callable] = None,
    **wkwargs: Unpack[SharedKwargs]
):
    def decorate(fn):
        @wraps(fn)
        async def wrap(*args, **kwargs):
            if not TracerWrapper.verify_initialized():
                return await fn(*args, **kwargs)

            workflow_name = name or fn.__name__
            set_workflow_name(workflow_name)
            span_name = f"{workflow_name}.workflow"

            with get_tracer(flush_on_exit=True) as tracer:
                with tracer.start_as_current_span(span_name) as span:
                    span.set_attribute(
                        SpanAttributes.SYNTRAC_SPAN_KIND,
                        SyntracSpanKindValues.WORKFLOW.value,
                    )
                    span.set_attribute(SpanAttributes.SYNTRAC_ENTITY_NAME, name)
                    add_extra_spans(span, **wkwargs)

                    if correlation_id:
                        span.set_attribute(
                            SpanAttributes.SYNTRAC_CORRELATION_ID, correlation_id
                        )

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
                                SpanAttributes.SYNTRAC_ENTITY_OUTPUT, output
                            )
                    except TypeError:
                        pass  # Some args might not be serializable

                    return res

        return wrap

    return decorate


def aworkflow_class(
    name: Optional[str],
    method_name: str,
    correlation_id: Optional[str] = None,
    **kwargs: Unpack[SharedKwargsWithHooks]
):
    def decorator(cls):
        workflow_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(
            cls,
            method_name,
            aworkflow_method(name=workflow_name, correlation_id=correlation_id, **kwargs)(method),
        )
        return cls

    return decorator
