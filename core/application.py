from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from core.error_handler import install_exception_handler
from core.logger import get_logger
from core.settings import ensure_directories, load_settings
from core.version import APP_NAME, BUILD, VERSION
from database.initialize import initialize_database


logger = get_logger("Application")


class APSApplication(QApplication):
    """
    Main QApplication implementation for the Automated
    Processing System.
    """

    def __init__(self, args: list[str]):
        super().__init__(args)

        self.settings = None

        self._initialize_application()

        self.aboutToQuit.connect(
            self._shutdown
        )

    def _initialize_application(self) -> None:
        """
        Perform all application-level startup tasks.
        """

        logger.info(
            "=================================================="
        )

        logger.info(
            "Starting %s | Version %s | Build %s",
            APP_NAME,
            VERSION,
            BUILD,
        )

        ensure_directories()

        logger.info(
            "Application directories verified."
        )

        self.settings = load_settings()

        logger.info(
            "Application configuration loaded."
        )

        initialize_database()

        logger.info(
            "Database infrastructure initialized."
        )

        install_exception_handler()

        self.setApplicationName(APP_NAME)
        self.setApplicationVersion(VERSION)
        self.setOrganizationName("APS Financial Solutions")

        self._apply_global_style()

        logger.info(
            "Application startup completed."
        )

    def _apply_global_style(self) -> None:
        """
        Apply the APS global visual theme.
        """

        self.setStyleSheet(
            """
            QWidget {
                background: #111111;
                color: white;
                font-family: "Segoe UI";
                font-size: 10pt;
            }

            QPushButton {
                background: #D4AF37;
                color: black;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton:hover {
                background: #E6C55A;
            }

            QPushButton:pressed {
                background: #B8962E;
            }

            QFrame {
                background: #1E1E1E;
                border-radius: 12px;
            }

            QLineEdit,
            QComboBox,
            QSpinBox,
            QDoubleSpinBox,
            QTextEdit {
                background: #181818;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 5px;
            }

            QStatusBar {
                background: #0B0B0B;
                color: #D4AF37;
            }

            QMenuBar {
                background: #111111;
                color: white;
            }

            QMenuBar::item:selected {
                background: #D4AF37;
                color: black;
            }

            QMenu {
                background: #1E1E1E;
                color: white;
            }

            QMenu::item:selected {
                background: #D4AF37;
                color: black;
            }
            """
        )

    def _shutdown(self) -> None:
        """
        Perform application shutdown logging.
        """

        logger.info(
            "Application shutdown initiated."
        )

        logger.info(
            "Application shutdown completed."
        )

        logger.info(
            "=================================================="
        )


def run_application() -> int:
    """
    Convenience entry point for the APS application.
    """

    application = APSApplication(sys.argv)

    return application.exec()