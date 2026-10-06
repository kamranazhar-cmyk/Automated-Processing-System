from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from core.application import APSApplication
from core.logger import get_logger
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.splash_screen import SplashScreen


logger = get_logger("Main")


def main() -> int:
    """
    APS application entry point.

    Startup flow:

        APSApplication
            ↓
        SplashScreen
            ↓
        LoginWindow
            ↓
        Authentication
            ↓
        MainWindow
    """

    logger.info(
        "APS main entry point started."
    )

    application = APSApplication(
        sys.argv
    )

    # --------------------------------------------------------
    # SPLASH SCREEN
    # --------------------------------------------------------

    splash = SplashScreen()

    splash.show()

    application.processEvents()

    logger.info(
        "Splash screen displayed."
    )

    # Give the splash screen an opportunity to display
    # application initialization information before
    # moving to authentication.
    application.processEvents()

    splash.close()

    logger.info(
        "Splash screen closed."
    )

    # --------------------------------------------------------
    # LOGIN WINDOW
    # --------------------------------------------------------

    login_window = LoginWindow()

    login_window.show()

    application.processEvents()

    logger.info(
        "Login window displayed."
    )

    # --------------------------------------------------------
    # MAIN WINDOW HOLDER
    # --------------------------------------------------------

    main_window: MainWindow | None = None

    def show_main_window() -> None:
        """
        Display the main application window after
        successful authentication.
        """

        nonlocal main_window

        logger.info(
            "Authentication successful."
        )

        main_window = MainWindow()

        main_window.show()

        login_window.close()

        logger.info(
            "Main window displayed."
        )

    def cancel_login() -> None:
        """
        Exit the application when the user cancels login.
        """

        logger.info(
            "Login cancelled. Application will exit."
        )

        application.quit()

    login_window.authenticated.connect(
        show_main_window
    )

    login_window.login_cancelled.connect(
        cancel_login
    )

    # --------------------------------------------------------
    # APPLICATION LOOP
    # --------------------------------------------------------

    return application.exec()


if __name__ == "__main__":
    sys.exit(
        main()
    )