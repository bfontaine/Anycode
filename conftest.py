from unittest.mock import Mock

from pytest import fixture


@fixture
def complete_fn_mock(mocker) -> Mock:
    return mocker.patch('anycode.generation.complete')


@fixture(autouse=True)
def clear_context():
    yield
    import anycode
    anycode.clear()
