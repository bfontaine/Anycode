import sys
from typing import Any, TextIO

from .client import set_openai_api_key, set_openai_api_key_from_env

__version__ = "0.1.2"

set_openai_api_key_from_env(force=False)

__this = sys.modules[__name__]
__generated: dict[str, Any] = {}


def __getattr__(name: str):
    from .generation import generate_any

    value = generate_any(name)
    setattr(__this, name, value)
    __generated[name] = value
    return value


def clear():
    """
    Clear all generated values.
    """
    for name in list(__generated):
        if name in __this.__dict__:
            delattr(__this, name)
        del __generated[name]


def dump(f: TextIO):
    """
    Dump all generated values on a file-like text writer.
    Example:

        with open("code.py", "w") as f:
            anycode.dump(f)
    """
    for name, value in __generated.items():
        if name not in __this.__dict__:  # skip deleted items
            continue

        if hasattr(value, "_openai_response"):
            # noinspection PyProtectedMember
            f.write(value._openai_response)
            f.write("\n\n")
        else:
            f.write(f"{name} = {value}\n\n")


def dumps():
    """
    Dump all generated values as a string.
    """
    import io

    w = io.StringIO()
    dump(w)
    return w.getvalue()
