import re
from unittest.mock import Mock

import anycode


def test_version():
    assert re.match(r"^\d+\.\d+\.\d+", anycode.__version__)


def test_constant(complete_fn_mock: Mock):
    complete_fn_mock.return_value = '{"hello": "world"}'
    assert anycode.DICT == {"hello": "world"}
    complete_fn_mock.assert_called_once()

    assert anycode.DICT == {"hello": "world"}
    complete_fn_mock.assert_called_once()


def test_function(complete_fn_mock: Mock):
    complete_fn_mock.return_value = 'def a(b, c):\n    return b + c\n'
    assert anycode.foo.__name__ == "foo"
    complete_fn_mock.assert_not_called()

    assert anycode.foo(1, 2) == 3
    complete_fn_mock.assert_called_once()

    assert anycode.foo("foo", "bar") == "foobar"
    complete_fn_mock.assert_called_once()

    del anycode.foo

    assert anycode.foo("foo", "bar") == "foobar"
    assert complete_fn_mock.call_count == 2
