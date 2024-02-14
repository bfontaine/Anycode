from unittest.mock import PropertyMock

from pytest import fixture

from anycode import set_openai_api_key, set_openai_api_key_from_env


@fixture
def mock_client(mocker):
    mock = mocker.patch('anycode.client.openai_client')
    mock.api_key = PropertyMock()
    yield mock


def test_set_openai_api_key(mock_client):
    set_openai_api_key("FOO")
    assert mock_client.api_key == "FOO"

    set_openai_api_key("BAR")
    assert mock_client.api_key == "BAR"

    set_openai_api_key("QUX", force=False)
    assert mock_client.api_key == "BAR"


def test_set_openai_api_key_from_env(mocker, mock_client):
    mocker.patch.dict('anycode.client.environ', {"VAR": "FOO", "VAR2": "BAR", "VAR3": "QUX"})

    set_openai_api_key_from_env("VAR")
    assert mock_client.api_key == "FOO"

    set_openai_api_key_from_env("VAR2")
    assert mock_client.api_key == "BAR"

    set_openai_api_key_from_env("VAR3", force=False)
    assert mock_client.api_key == "BAR"
