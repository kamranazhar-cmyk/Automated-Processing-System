from __future__ import annotations

import sys
import traceback
from typing import Type

from PySide6.QtWidgets import QMessageBox, QApplication

from core.logger import get_logger


logger = get_logger("ErrorHandler")


def handle_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback,
) -> None:
    """
    Global handler for uncaught application exceptions.
    """

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(
            exc_type,
            exc_value,
            exc_traceback,
        )
        return

    error_text = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback,
        )
    )

    logger.critical(
        "Unhandled application exception:\n%s",
        error_text,
    )

    application = QApplication.instance()

    if application is not None:
        QMessageBox.critical(
            None,
            "Application Error",
            (
                "An unexpected application error occurred.\n\n"
                "The error has been recorded in the APS log file.\n\n"
                f"Error: {exc_value}"
            ),
        )


def install_exception_handler() -> None:
    """
    Install APS global exception handling.
    """

    sys.excepthook = handle_exception

    logger.info("Global exception handler installed.")