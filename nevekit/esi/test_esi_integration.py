# Integration test file for the sde module.
import pytest
import os
from nevekit import get_nevekit_home
from nevekit.esi import ESI, SWAGGER_CLIENT_FILE_NAME

try:
    is_skip_test = os.environ["SKIP_INTEGRATION_TESTS"]
except KeyError:
    is_skip_test = True


@pytest.fixture()
def esi():
    # Remove the SwaggerClient pickle file if it exists.
    try:
        os.remove(f"{get_nevekit_home()}/{SWAGGER_CLIENT_FILE_NAME}")
    except FileNotFoundError:
        pass

    return ESI()


@pytest.mark.skipif(is_skip_test, reason="Skipping the test")
def test_init_success(esi):
    """
    Test that the ESI object is initialized correctly.
    """
    esi.init()
    assert esi.get_client() is not None
