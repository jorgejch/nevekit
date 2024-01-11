# Tests the parent package shared utilities.

from src import get_nevekit_home, logger


def test_get_nevekit_home():
    """
    Test that the nevekit home directory is correct.
    """
    assert get_nevekit_home().endswith(".nevekit")


def test_init_logger():
    """
    Test that the logger is initialized correctly.
    """
    assert logger is not None
    assert len(logger.handlers) == 2
    assert logger.handlers[0].__class__.__name__ == "FileHandler"
    assert logger.handlers[1].__class__.__name__ == "StreamHandler"
    assert logger.name == "nevekit"
    assert logger.propagate is True
    assert logger.disabled is False
    assert logger.filters == []
