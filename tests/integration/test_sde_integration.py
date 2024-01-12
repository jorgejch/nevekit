# Integration test file for the sde module.
import pytest
import os
from nevekit import get_nevekit_home
from nevekit.sde import SDE, SDE_DB_NAME

try:
    is_skip_test = os.environ["SKIP_INTEGRATION_TESTS"]
except KeyError:
    is_skip_test = True


@pytest.fixture()
def sde():
    return SDE()


@pytest.mark.skipif(is_skip_test, reason="Skipping the test")
def test_init_success(sde):
    """
    Test that the SDE object is initialized correctly.
    """
    sde.init()
    assert sde.db_conn_str is not None
    assert os.path.exists(f"{get_nevekit_home()}/{SDE_DB_NAME}")
