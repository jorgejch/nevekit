# Test file for the sde module.
from unittest.mock import patch
import pytest
from nevekit.sde import SDE

# Constants for testing
SDE_DB_NAME = "sde.db"

# Create a set of unit tests for the sde module.
# These should provide 100% code coverage.


@pytest.fixture
def sde():
    return SDE()


def test_init_success(sde):
    """
    Test that the SDE object is initialized correctly.
    """
    # Patch the _download_db method.
    with patch("nevekit.sde.SDE._download_db") as mock_download_db:
        mock_download_db.return_value = "sqlite:///sde.db"
        # Initialize the SDE object.
        sde.init()
    assert sde.db_conn_str is not None


def test_init_failure(sde):
    """
    Test that the SDE object is initialized correctly.
    """
    # Patch the _download_db method.
    with patch("nevekit.sde.SDE._download_db") as mock_download_db:
        mock_download_db.side_effect = IOError("Error")
        # Initialize the SDE object.
        with pytest.raises(IOError):
            sde.init()
    assert sde.db_conn_str is None
