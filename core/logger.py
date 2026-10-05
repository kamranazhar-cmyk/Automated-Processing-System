from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from core.settings import LOG_FILE, ensure_directories


LOGGER_NAME = "APS"

MAX_LOG_FILE_SIZE = 5 * 1024 * 1024
BACKUP_LOG_COUNT = 5


def configure_logging() -> logging.Logger:
    """
    Configure the central APS application logger.
    """

    ensure_directories()

    logger = logging.getLogger(LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_FILE_SIZE,
        backupCount=BACKUP_LOG_COUNT,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return the central APS logger or a named child logger.
    """

    logger = configure_logging()

    if name:
        return logger.getChild(name)

    return logger


logger = configure_logging()