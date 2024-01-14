import os
import logging
import numpy as np


def _init_logger():
    """
    Initialize a logger object.
    """
    logger = logging.getLogger("nevekit")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler("nevekit.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def get_nevekit_home():
    """
    Get full path to ~/.nevekit.
    """
    return os.path.expanduser("~/.nevekit")


def are_two_floats_equal(actual, expected, tol=1e-08) -> bool:
    """
    Test that two floats are equal within a tolerance.
    """
    return np.isclose([actual], [expected], atol=tol)[0]


logger = _init_logger()
