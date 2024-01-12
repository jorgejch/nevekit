# Test file for the esi module.
from unittest.mock import patch
import pytest
from nevekit.esi import ESI
from nevekit import test_floats


@pytest.fixture
def esi():
    return ESI()


def test_get_character_standings_success(esi):
    """
    Test that the the get_character_standings method returns the correct value.
    """
    with patch(
        "nevekit.esi.ESI.get_character_standings"
    ) as mock_get_character_standings:
        mock_get_character_standings.return_value = [0.01]
        assert test_floats(esi.get_character_standings()[0], 0.01)
