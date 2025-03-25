import os
from openlayer.lib.integrations import langchain_callback
from openlayer.lib import trace, trace_openai


def get_openlayer_handler():
    """Returns an Openlayer handler for LangChain callbacks."""
    if (
        "OPENLAYER_API_KEY" in os.environ
        and "OPENLAYER_INFERENCE_PIPELINE_ID" in os.environ
    ):
        return langchain_callback.OpenlayerHandler()
    return None


def trace_function(func=None, context_kwarg=None):
    """Wrapper for the Openlayer trace decorator that checks if Openlayer is configured."""
    if (
        "OPENLAYER_API_KEY" in os.environ
        and "OPENLAYER_INFERENCE_PIPELINE_ID" in os.environ
    ):
        return (
            trace(context_kwarg=context_kwarg)(func)
            if func
            else trace(context_kwarg=context_kwarg)
        )

    # Return identity function if Openlayer not configured
    def identity_decorator(f):
        return f

    return identity_decorator if func is None else identity_decorator(func)
