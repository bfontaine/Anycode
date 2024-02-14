from unittest.mock import Mock

import pytest
from pytest import fixture

# noinspection PyProtectedMember
from anycode.generate import _generate_args_string, generate_constant, GenerationException, generate_function, \
    generate_any


@fixture
def complete_fn_mock(mocker) -> Mock:
    return mocker.patch('anycode.generate.complete')


def test_generate_constant(mocker, complete_fn_mock):
    complete_fn_mock.return_value = "42"
    assert generate_constant("FOO") == 42
    complete_fn_mock.assert_called_once()

    complete_fn_mock.return_value = "[1, true, null, {}]"
    assert generate_constant("FOO") == [1, True, None, {}]

    complete_fn_mock.return_value = "oh no!"
    with pytest.raises(GenerationException, match="Cannot generate code for 'FOO = ': 'oh no!'"):
        generate_constant("FOO")


@pytest.mark.parametrize("args,kwargs,expected", (
        ([], {}, ""),
        ([1, 2, 3], {"a": 4}, "b, c, d, a"),
))
def test_generate_args_string(args, kwargs, expected):
    assert _generate_args_string(args, kwargs) == expected


def test_generate_function(complete_fn_mock: Mock):
    openai_response = 'def do_stuff(a):\n    return "test-" + a\n'
    complete_fn_mock.return_value = openai_response
    fn = generate_function("do_stuff")
    assert fn.__name__ == "do_stuff"
    complete_fn_mock.assert_not_called()

    assert fn("foo") == "test-foo"
    complete_fn_mock.assert_called_once()

    assert fn._openai_response == openai_response
    assert fn._openai_fn("foo") == "test-foo"

    assert fn("bar") == "test-bar"
    complete_fn_mock.assert_called_once()


def test_generate_function_failure(complete_fn_mock: Mock):
    complete_fn_mock.return_value = "oh no!"
    f = generate_function("do_stuff")

    with pytest.raises(GenerationException):
        f()


def test_generate_function_name_mismatch(complete_fn_mock: Mock):
    complete_fn_mock.return_value = "def do_b():\n    return 42\n"
    f = generate_function("do_a")

    with pytest.raises(GenerationException):
        f()


def test_generate_any(complete_fn_mock: Mock):
    complete_fn_mock.return_value = "42"
    assert generate_any("FOO") == 42
    complete_fn_mock.assert_called_once()

    complete_fn_mock.return_value = "def f():\n    return 42\n"

    f = generate_any("f")
    assert f() == 42
