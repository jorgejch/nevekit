# Test file for the esi module.
from nevekit import 
from esi import ESI


def test_get_character_standings_success():
    """
    Test that the the get_character_standings method returns the correct value.
    """
    esi = ESI()
    assert np.esi.get_character_standings()[0]