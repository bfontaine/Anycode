import pytest

# noinspection PyProtectedMember
from anycode.generate import _generate_args_string


@pytest.mark.parametrize("args,kwargs,expected", (
        ([], {}, ""),
        ([1, 2, 3], {"a": 4}, "b, c, d, a"),
))
def test_generate_args_string(args, kwargs, expected):
    assert _generate_args_string(args, kwargs) == expected
