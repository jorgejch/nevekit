# Test file for the esi.sso module.
from esi.sso import SSO

# Constants for testing
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
CALLBACK_URI = "callback_uri"


def test_base_url():
    """
    Test that the SSO object is initialized correctly.
    """
    assert SSO.BASE_URL == "https://login.eveonline.com"


def test_login_success():
    """
    Test that the SSO object is initialized correctly.
    """
    sso = SSO(CLIENT_ID, CLIENT_SECRET, CALLBACK_URI)
    assert sso.client_id == CLIENT_ID
    assert sso.client_secret == CLIENT_SECRET
    assert sso.callback_uri == CALLBACK_URI


def test_get_character_id_success():
    """
    Test that the SSO object is initialized correctly.
    """
    sso = SSO(CLIENT_ID, CLIENT_SECRET, CALLBACK_URI)
    assert sso.get_character_id() == 0


def test_get_character_id_failure():
    """
    Test that the SSO object is initialized correctly.
    """
    sso = SSO(CLIENT_ID, CLIENT_SECRET, CALLBACK_URI)
    assert sso.get_character_id() != 0
