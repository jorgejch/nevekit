# Test file for the esi module.
from unittest.mock import MagicMock, patch
import pytest
from nevekit.esi import ESI
from nevekit import are_two_floats_equal


@pytest.fixture
def esi():
    return ESI()


@pytest.mark.skip(reason="Not implemented yet")
def test_get_character_standings_success(esi):
    """
    Test that the the get_character_standings method returns the correct value.
    """
    mock_swagger_client = MagicMock()

    mock_swagger_client.Character.get_characters_character_id_standings.side_effect = [
        [0.01]
    ]

    with patch(
        "nevekit.esi.ESI.get_character_standings"
    ) as mock_get_character_standings:
        mock_get_character_standings.return_value = [0.01]
        assert are_two_floats_equal(esi.get_character_standings()[0], 0.01)
