# Test file for the sde module.
import subprocess
import pytest
from unittest.mock import patch, MagicMock, mock_open
from sde import SDE

# Constants for testing
SDE_DB_NAME = "sde.db"

# Create a set of unit tests for the sde module.
# These should provide 100% code coverage.
# The

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

def test_get_nevekit_home(sde):
    assert sde.get_nevekit_home() == "~/.nevekit"