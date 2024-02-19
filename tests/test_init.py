import io
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
    assert 'foo' not in dir(anycode)

    assert anycode.foo("foo", "bar") == "foobar"
    assert complete_fn_mock.call_count == 2


def test_clear(complete_fn_mock: Mock):
    complete_fn_mock.return_value = '42'
    assert anycode.FOO == 42
    complete_fn_mock.return_value = '43'
    assert anycode.FOO == 42  # cached
    anycode.clear()
    assert anycode.FOO == 43
    complete_fn_mock.return_value = '44'
    del anycode.FOO
    anycode.clear()
    assert anycode.FOO == 44


def test_empty_dump(complete_fn_mock: Mock):
    w = io.StringIO()
    anycode.dump(w)
    assert w.getvalue() == ''
    assert anycode.dumps() == ''


def test_dump(complete_fn_mock: Mock):
    complete_fn_mock.return_value = 'def f():\n    return 42\n'
    assert anycode.f() == 42

    complete_fn_mock.return_value = '43'
    assert anycode.FOO == 43

    w = io.StringIO()
    anycode.dump(w)
    expected = 'def f():\n    return 42\n\n\nFOO = 43'
    assert w.getvalue().rstrip() == expected
    assert anycode.dumps().rstrip() == expected

    del anycode.f
    assert 'f' not in dir(anycode)

    expected = 'FOO = 43'
    w = io.StringIO()
    anycode.dump(w)
    assert w.getvalue().rstrip() == expected
    assert anycode.dumps().rstrip() == expected
