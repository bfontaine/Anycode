import sys

from .client import set_openai_api_key, set_openai_api_key_from_env

__version__ = "0.1.1"

set_openai_api_key_from_env(force=False)

this = sys.modules[__name__]


def __getattr__(name: str):
    from .generate import generate_any

    value = generate_any(name)
    setattr(this, name, value)
    return value
