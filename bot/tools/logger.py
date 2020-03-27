"""
Contains code related to logging functionality.
"""

import logging


def get_logger(name, level=None):
    """ Create a logger for the given module and level

    level can be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
    """
    logger = logging.getLogger(name)
    if level:
        logger.setLevel(level)
    return logger
