import logging

from config.logging_config import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Parameters
    ----------
    name : str
        Usually __name__.

    Returns
    -------
    logging.Logger
    """
    return logging.getLogger(name)
