# Test file for the sde module.
import subprocess
from unittest.mock import patch
import pytest
from sde import SDE

# Constants for testing
SDE_DB_NAME = "sde.db"

# Create a set of unit tests for the sde module.
# These should provide 100% code coverage.


@pytest.fixture
def sde():
    return SDE()


def before_all():
    """
    Run once before all tests.
    """
    # Install the library locally in editable mode.
    # This allows us to import the library.
    subprocess.check_call(["pip", "install", "-e", "."])


def test_init_success(sde):
    """
    Test that the SDE object is initialized correctly.
    """
    # Patch the _download_db method.
    with patch("sde.SDE._download_db") as mock_download_db:
        mock_download_db.return_value = "sqlite:///sde.db"
        # Initialize the SDE object.
        sde.init()
    assert sde.db_conn_str is not None
