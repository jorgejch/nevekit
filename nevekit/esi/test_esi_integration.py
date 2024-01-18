# Integration test file for the sde module.
import pytest
import os
from nevekit import get_nevekit_home, logger
from nevekit.esi import ESI, SWAGGER_CLIENT_FILE_NAME

try:
    is_skip_test = os.environ["SKIP_INTEGRATION_TESTS"]
except KeyError:
    is_skip_test = True


# Constants
CHARACTER_ID = 2112002224


@pytest.fixture()
def esi():
    return ESI()


@pytest.mark.skipif(is_skip_test, reason="Skipping the test")
def test_init_success(esi):
    """
    Test that the ESI object is initialized correctly.
    """
    # Remove the SwaggerClient pickle file if it exists.
    try:
        os.remove(f"{get_nevekit_home()}/{SWAGGER_CLIENT_FILE_NAME}")
    except FileNotFoundError:
        pass

    esi.init()
    assert esi.get_client() is not None


@pytest.mark.skipif(is_skip_test, reason="Skipping the test")
def test_get_character_public_info(esi):
    """
    Test using the SwaggerClient object to get a character's public info.
    """

    # Initialize the SwaggerClient object.
    esi.init()

    # Get the character standings.
    character_public_info = (
        esi.get_client()
        .Character.get_characters_character_id(character_id=CHARACTER_ID)
        .result()
    )

    logger.debug(f"character id {CHARACTER_ID} public info: {character_public_info}")

    assert character_public_info is not None
    assert character_public_info["name"] is not None
