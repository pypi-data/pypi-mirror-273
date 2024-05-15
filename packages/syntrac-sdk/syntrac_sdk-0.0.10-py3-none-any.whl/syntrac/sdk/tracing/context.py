from typing import Optional
from opentelemetry.context import attach, set_value, get_value


class ContextKeys:
    CORRELATION_ID = "correlation_id"
    ASSOCIATION_PROPERTIES = "association_properties"
    WORKFLOW_NAME = "workflow_name"
    # Prompts
    PROMPT_KEY = "prompt_key"
    PROMPT_VERSION = "prompt_version"
    PROMPT_VERSION_NAME = "prompt_version_name"
    PROMPT_VERSION_HASH = "prompt_version_hash"
    PROMPT_TEMPLATE_VARIABLES = "prompt_template_variables"
    # Models
    MODEL_KEY = "model_key"
    MODEL_VERSION = "model_version"
    MODEL_VERSION_NAME = "model_version_name"
    MODEL_VERSION_HASH = "model_version_hash"

    # Toggle flag
    OVERRIDE_ENABLE_CONTENT_TRACING = "override_enable_content_tracing"


def set_association_properties(properties: dict) -> None:
    attach(set_value(ContextKeys.ASSOCIATION_PROPERTIES, properties))


def set_workflow_name(workflow_name: str) -> None:
    attach(set_value(ContextKeys.WORKFLOW_NAME, workflow_name))


def set_prompt_tracing_context(
    key: Optional[str] = None,
    version: Optional[str] = None,
    version_name: Optional[str] = None,
    version_hash: Optional[str] = None,
    template_variables: Optional[dict] = None,
) -> None:
    if key is not None:
        attach(set_value(ContextKeys.PROMPT_KEY, key))
    if version is not None:
        attach(set_value(ContextKeys.PROMPT_VERSION, version))
    if version_name is not None:
        attach(set_value(ContextKeys.PROMPT_VERSION_NAME, version_name))
    if version_hash is not None:
        attach(set_value(ContextKeys.PROMPT_VERSION_HASH, version_hash))
    if template_variables is not None:
        attach(set_value(ContextKeys.PROMPT_TEMPLATE_VARIABLES, template_variables))


def set_override_enable_context_tracing(val: bool) -> None:
    attach(set_value(ContextKeys.WORKFLOW_NAME, val))


def get_workflow_name():
    return get_value(ContextKeys.WORKFLOW_NAME)


def get_correlation_id():
    return get_value(ContextKeys.CORRELATION_ID)


def get_association_properties():
    return get_value(ContextKeys.ASSOCIATION_PROPERTIES)


def get_prompt_key():
    return get_value(ContextKeys.PROMPT_KEY)


def get_prompt_version():
    return get_value(ContextKeys.PROMPT_VERSION)


def get_prompt_version_name():
    return get_value(ContextKeys.PROMPT_VERSION_NAME)


def get_prompt_version_hash():
    return get_value(ContextKeys.PROMPT_VERSION_HASH)


def get_prompt_template_variables():
    return get_value(ContextKeys.PROMPT_TEMPLATE_VARIABLES)
