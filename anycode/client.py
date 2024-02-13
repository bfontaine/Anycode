from os import environ

from dotenv import load_dotenv

from openai import OpenAI

__all__ = ["openai_client", "set_openai_api_key", "set_openai_api_key_from_env"]

DEFAULT_ENV_VAR_NAME = "OPENAI_API_KEY"

load_dotenv()

openai_client = OpenAI(
    # Default to "" so this doesn't raise if it’s not set;
    # the OpenAI object needs it only when it makes a call to the API, not on initialization.
    api_key=environ.get(DEFAULT_ENV_VAR_NAME, ""),
)


def set_openai_api_key(api_key: str, force=True):
    if not force or not openai_client.api_key:
        openai_client.api_key = api_key


def set_openai_api_key_from_env(variable_name=DEFAULT_ENV_VAR_NAME, *, force=True):
    from os import environ
    if api_key := environ.get(variable_name):
        set_openai_api_key(api_key, force=force)
