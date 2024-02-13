import json
from json import JSONDecodeError
from typing import Any, Callable

import openai

__all__ = ["generate_constant", "generate_function", "generate_any"]

EXCEPTION_RESPONSE_EXCERPT_SIZE = 20

CONSTANT_INIT_MESSAGES = [
    {
        "role": "system",
        "content": "You are a helpful assistant that writes JavaScript constants in JSON format. Use null instead of undefined."
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


class GenerationException(Exception):
    def __init__(self, query: str, openai_response: str):
        excerpt = openai_response
        if len(excerpt) > EXCEPTION_RESPONSE_EXCERPT_SIZE + 1:
            excerpt = excerpt[:EXCEPTION_RESPONSE_EXCERPT_SIZE] + "…"

        super().__init__("Cannot generate code for %r: %r" % (query, excerpt))
        self.query = query
        self.openai_response = openai_response


def complete(*, init_messages: list[dict], message: str, model="gpt-3.5-turbo") -> str:
    response = openai.chat.completions.create(
        model=model,
        messages=init_messages + [
            {"role": "user", "content": message}
        ],
    )

    return response.choices[0].message.content


def generate_constant(name: str) -> str | int | float | bool | list | dict[str, Any] | None:
    openai_response = complete(
        init_messages=CONSTANT_INIT_MESSAGES,
        message=f"{name} = ",
    )

    try:
        return json.loads(openai_response)
    except JSONDecodeError as e:
        raise GenerationException(
            query=name,
            openai_response=openai_response,
        ) from e


def generate_function(name: str) -> Callable:
    pass  # TODO


def generate_any(name: str):
    if name.upper():
        return generate_constant(name)

    return generate_function(name)
