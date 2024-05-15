from typing import Any
from syntrac_opentelemetry.semconv.ai import SpanAttributes
from syntrac.sdk.tracing.context import (
    get_prompt_key,
    get_prompt_template_variables,
    get_prompt_version,
    get_prompt_version_hash,
    get_prompt_version_name,
    get_workflow_name,
)


class PromptSpanAttributes:
    # Prompts
    SYNTRAC_PROMPT_KEY = "syntrac.prompt.key"
    SYNTRAC_PROMPT_VERSION = "syntrac.prompt.version"
    SYNTRAC_PROMPT_VERSION_NAME = "syntrac.prompt.version_name"
    SYNTRAC_PROMPT_VERSION_HASH = "syntrac.prompt.version_hash"
    SYNTRAC_PROMPT_TEMPLATE_VARIABLES = "syntrac.prompt.template_variables"


def set_workflow_name_from_context(span):
    workflow_name = get_workflow_name()
    if workflow_name is not None:
        span.set_attribute(SpanAttributes.SYNTRAC_WORKFLOW_NAME, workflow_name)


def set_prompt_attributes_from_context(span):
    prompt_key = get_prompt_key()
    if prompt_key is not None:
        span.set_attribute(PromptSpanAttributes.SYNTRAC_PROMPT_KEY, prompt_key)

    prompt_version = get_prompt_version()
    if prompt_version is not None:
        span.set_attribute(PromptSpanAttributes.SYNTRAC_PROMPT_VERSION, prompt_version)

    prompt_version_name = get_prompt_version_name()
    if prompt_version_name is not None:
        span.set_attribute(PromptSpanAttributes.SYNTRAC_PROMPT_VERSION_NAME, prompt_version_name)

    prompt_version_hash = get_prompt_version_hash()
    if prompt_version_hash is not None:
        span.set_attribute(PromptSpanAttributes.SYNTRAC_PROMPT_VERSION_HASH, prompt_version_hash)

    prompt_template_variables: Any = get_prompt_template_variables()
    if prompt_version_hash is not None:
        for key, value in prompt_template_variables.items():
            span.set_attribute(
                f"{PromptSpanAttributes.SYNTRAC_PROMPT_TEMPLATE_VARIABLES}.{key}", value
            )
