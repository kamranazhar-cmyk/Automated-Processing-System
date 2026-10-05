from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from core.application import APSApplication
from core.logger import get_logger
from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen


logger = get_logger("Main")


def main() -> int:

    logger.info(
        "APS main entry point started."
    )

    application = APSApplication(
        sys.argv
    )

    splash = SplashScreen()
    splash.show()

    application.processEvents()

    logger.info(
        "Splash screen displayed."
    )

    window = MainWindow()

    splash.finish(
        window
    )

    window.show()

    logger.info(
        "Main window displayed."
    )

    return application.exec()


if __name__ == "__main__":
    sys.exit(
        main()
    )