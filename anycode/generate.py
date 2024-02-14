import inspect
import json
from json import JSONDecodeError
import string
from typing import Any, Callable, List, Dict, cast, Union, Protocol

from openai.types.chat import ChatCompletionMessageParam

from anycode.client import openai_client

__all__ = ["generate_constant", "generate_function", "generate_any", "GeneratedFunction"]

EXCEPTION_RESPONSE_EXCERPT_SIZE = 20

CONSTANT_INIT_MESSAGES = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant that writes JavaScript constants in JSON format."
            " Use null instead of undefined."
        )
    },
    {"role": "user", "content": "PI ="},
    {"role": "assistant", "content": "3.14159265359"},
    {"role": "user", "content": "DIGITS ="},
    {"role": "assistant", "content": "\"0123456789\""},
    {"role": "user", "content": "UPPERCASE_LETTERS ="},
    {"role": "assistant", "content": '"ABCDEFGHIJKLMNOPQRSTUVWXYZ"'},
    {"role": "user", "content": "TRUE ="},
    {"role": "assistant", "content": "true"},
    {"role": "user", "content": "NONE ="},
    {"role": "assistant", "content": "null"},
]

FUNCTION_INIT_MESSAGES = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant that writes Python functions."
            " Use the exact name provided by the user."
            " Don’t explain your assumptions and write the full code."
            " Don’t use any external module except requests."
        ),
    },
    {"role": "user", "content": "def hello_world():"},
    {"role": "assistant", "content": "def hello_world():\n    print(\"Hello, World!\")\n"},
    {"role": "user", "content": "def add(a, b):"},
    {"role": "assistant", "content": "def add(a, b):\n    return a + b\n"},
]
FUNCTION_ATTR_NAME = "_openai_fn"


class GeneratedFunction(Protocol):
    _openai_response: str
    _openai_fn: Callable
    # We cannot subclass Callable so we have to add these by ourselves
    __name__: str
    __doc__: str

    def __call__(self, *args, **kwargs): ...


class GenerationException(Exception):
    def __init__(self, query: str, openai_response: str):
        excerpt = openai_response
        if len(excerpt) > EXCEPTION_RESPONSE_EXCERPT_SIZE + 1:
            excerpt = excerpt[:EXCEPTION_RESPONSE_EXCERPT_SIZE] + "…"

        super().__init__("Cannot generate code for %r: %r" % (query, excerpt))
        self.query = query
        self.openai_response = openai_response


def complete(*, init_messages: List[dict], message: str, model="gpt-3.5-turbo") -> str:  # pragma: nocover
    # Since we circumvent OpenAI’s API key check in the constructor, we have to do it by ourselves when we call the API
    # otherwise we get a cryptic "Connection error".
    assert openai_client.api_key != "", ("The OpenAI API key must be set!"
                                         " Use anycode.set_openai_api_key or anycode.set_openai_api_key_from_env.")

    response = openai_client.chat.completions.create(
        model=model,
        messages=cast(
            # https://github.com/openai/openai-python/issues/911#issuecomment-1834547461
            List[ChatCompletionMessageParam],
            init_messages + [
                {"role": "user", "content": message},
            ]
        ),
    )

    return cast(str, response.choices[0].message.content)


def generate_constant(name: str) -> Union[str, int, float, bool, list, Dict[str, Any], None]:
    message = f"{name} = "
    openai_response = complete(
        init_messages=CONSTANT_INIT_MESSAGES,
        message=message,
    )

    try:
        return json.loads(openai_response)
    except JSONDecodeError as e:
        raise GenerationException(
            query=message,
            openai_response=openai_response,
        ) from e


def _generate_args_string(args, kwargs) -> str:
    args_string_fragments: List[str] = []

    arg_names = [c for c in string.ascii_lowercase if c not in kwargs]
    arg_name_index = 0

    for _ in args:
        arg_name = arg_names[arg_name_index]
        arg_name_index += 1

        args_string_fragments.append(arg_name)

    args_string_fragments.extend(kwargs)

    return ", ".join(args_string_fragments)


def generate_function(name: str) -> GeneratedFunction:
    def fn(*args, **kwargs):
        if not hasattr(fn, FUNCTION_ATTR_NAME):
            args_string = _generate_args_string(args, kwargs)
            function_signature = f"def {name}({args_string}):"

            openai_response = complete(
                init_messages=FUNCTION_INIT_MESSAGES,
                message=function_signature,
            )

            try:
                code = compile(openai_response, "<string>", mode="exec")
            except SyntaxError as e:
                raise GenerationException(
                    function_signature,
                    openai_response=openai_response,
                ) from e

            scope = dict(inspect.stack()[0].frame.f_globals)
            previous_scope_keys = set(scope)
            exec(code, scope)  # YOLO
            new_scope_keys = set(scope) - previous_scope_keys

            if name in scope:
                openai_fn = scope[name]
            elif len(new_scope_keys) == 1:
                openai_fn = scope[new_scope_keys.pop()]
            else:
                raise GenerationException(
                    function_signature,
                    openai_response=openai_response,
                )

            setattr(fn, FUNCTION_ATTR_NAME, openai_fn)
            setattr(fn, "_openai_response", openai_response)

        return getattr(fn, FUNCTION_ATTR_NAME)(*args, **kwargs)

    fn.__name__ = name
    return cast(GeneratedFunction, fn)


def generate_any(name: str):
    if name.isupper():
        return generate_constant(name)

    return generate_function(name)
