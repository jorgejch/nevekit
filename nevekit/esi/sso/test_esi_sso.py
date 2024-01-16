import pytest
from unittest.mock import patch, MagicMock, ANY
from nevekit.esi.sso import SSO, TOKEN_ENDPOINT
from datetime import datetime, timedelta


@pytest.fixture()
def sso():
    return SSO("client_id", "client_secret", "callback_uri")


def test_init_success(sso):
    """
    Test that the SSO object is initialized correctly.
    """
    assert sso.client_id == "client_id"
    assert sso.client_secret == "client_secret"
    assert sso.callback_uri == "callback_uri"
    assert sso.scopes == ["publicData"]
    assert sso.character_id is None
    assert sso.access_token is None
    assert sso.oauth is None
    assert sso.state is None
    assert sso.code_verifier is None


def test__init(sso):
    """
    Test the _init method of the SSO object.
    """
    with patch("nevekit.esi.sso.secrets.token_urlsafe") as mock_token_urlsafe:
        mock_token_urlsafe.return_value = "code_verifier"

        sso._init()

        assert sso.oauth is not None
        assert sso.code_verifier == "code_verifier"


def test__get_auth_url(sso):
    """
    Test the _get_auth_url method of the SSO object.
    """
    oauth_mock = MagicMock()
    oauth_mock.create_authorization_url.return_value = ("auth_url", "state")
    sso.oauth = oauth_mock

    auth_url = sso._get_auth_url()

    assert auth_url == "auth_url"
    assert sso.state == "state"


def test__is_token_expired(sso):
    """
    Test the _is_token_expired method of the SSO object.
    """
    # Set the access token expiration time in the future.
    sso.access_token_expires_at = datetime.utcnow() + timedelta(seconds=1200)
    assert sso._is_token_expired() is False

    # Set the access token expiration time in the past.
    sso.access_token_expires_at = datetime.utcnow() - timedelta(seconds=1200)
    assert sso._is_token_expired() is True


def test__refresh_token(sso):
    """
    Test the _refresh_token method of the SSO object.
    """

    oauth_mock = MagicMock()
    oauth_mock.refresh_token.return_value = {
        "access_token": "new_token",
        "refresh_token": "refresh_token",
        "expires_at": 1200,
    }
    _update_token_expires_at_mock = MagicMock()
    sso._update_token_expires_at = _update_token_expires_at_mock
    sso.oauth = oauth_mock
    sso.access_token = {
        "access_token": "old_token",
        "refresh_token": "refresh_token",
        "expires_at": 1200,
    }

    sso._refresh_token()
    assert sso.access_token == {
        "access_token": "new_token",
        "refresh_token": "refresh_token",
        "expires_at": 1200,
    }
    assert oauth_mock.refresh_token.call_count == 1
    assert oauth_mock.refresh_token.call_args[0][0] == TOKEN_ENDPOINT
    assert oauth_mock.refresh_token.call_args[1]["refresh_token"] == "refresh_token"
    assert oauth_mock.refresh_token.call_args[1]["code_verifier"] == ANY
    assert _update_token_expires_at_mock.call_count == 1
    assert _update_token_expires_at_mock.call_args[0][0] == ANY


def test_start_auth_process(sso):
    """
    Test the start_auth_process method of the SSO object.
    """
    with patch("threading.Thread.start") as mock_thread_start:
        with patch("webbrowser.open") as mock_webbrowser_open:
            sso.start_auth_process()

            mock_thread_start.assert_called_once()
            mock_webbrowser_open.assert_called_with("http://localhost:5000/login")


def test_get_access_token(sso):
    """
    Test the get_access_token method of the SSO object.
    """
    sso.access_token = {"access_token": "token"}
    sso.access_token_expires_at = datetime.utcnow() + timedelta(seconds=1200)

    assert sso.get_access_token() == {"access_token": "token"}


def test_get_character_id(sso):
    """
    Test the get_character_id method of the SSO object.
    """
    sso.character_id = 12345

    assert sso.get_character_id() == 12345


def test_login(sso):
    """
    Test the login method of the SSO object.
    """
    with patch("nevekit.esi.sso.redirect") as mock_redirect:
        oauth = MagicMock()
        oauth.create_authorization_url.return_value = ("auth_url", "state")
        sso.oauth = oauth
        sso.login()
        mock_redirect.assert_called_with(sso._get_auth_url())


@pytest.mark.skip(
    reason="TODO: Hard, the implementation of this test is. Do it later, you must."
)
def test_oauth_callback(sso):
    """
    Test the oauth_callback method of the SSO object.
    """
