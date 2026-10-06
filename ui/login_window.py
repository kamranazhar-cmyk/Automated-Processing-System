from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.authentication import authentication_service
from core.logger import get_logger
from core.session import session


logger = get_logger("LoginWindow")


class LoginWindow(QWidget):
    """
    APS authentication window.

    The LoginWindow is responsible only for collecting
    credentials and initiating authentication.

    Authentication is delegated to AuthenticationService.

    A successful authentication creates the application
    session through UserSession.
    """

    authenticated = Signal()
    login_cancelled = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(
            "APS - Login"
        )

        self.setFixedSize(
            460,
            360,
        )

        self._build_ui()

    def _build_ui(self) -> None:
        """
        Build the login interface.
        """

        outer_layout = QVBoxLayout(
            self
        )

        outer_layout.setContentsMargins(
            35,
            30,
            35,
            30,
        )

        outer_layout.setSpacing(
            15
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = QLabel(
            "AUTOMATED PROCESSING SYSTEM"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            color: #D4AF37;
            """
        )

        outer_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Secure User Authentication"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        subtitle.setStyleSheet(
            """
            color: #AAAAAA;
            font-size: 11px;
            """
        )

        outer_layout.addWidget(
            subtitle
        )

        # ----------------------------------------------------
        # LOGIN CARD
        # ----------------------------------------------------

        card = QFrame()

        card.setStyleSheet(
            """
            QFrame {
                background: #1E1E1E;
                border: 1px solid #333333;
                border-radius: 12px;
            }
            """
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        card_layout.setSpacing(
            10
        )

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        username_label = QLabel(
            "Username"
        )

        username_label.setStyleSheet(
            """
            color: #D4AF37;
            font-weight: bold;
            """
        )

        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText(
            "Enter username"
        )

        self.username_input.setClearButtonEnabled(
            True
        )

        self.username_input.returnPressed.connect(
            self._handle_login
        )

        card_layout.addWidget(
            username_label
        )

        card_layout.addWidget(
            self.username_input
        )

        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        password_label = QLabel(
            "Password"
        )

        password_label.setStyleSheet(
            """
            color: #D4AF37;
            font-weight: bold;
            """
        )

        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Enter password"
        )

        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        self.password_input.returnPressed.connect(
            self._handle_login
        )

        card_layout.addWidget(
            password_label
        )

        card_layout.addWidget(
            self.password_input
        )

        # ----------------------------------------------------
        # STATUS MESSAGE
        # ----------------------------------------------------

        self.status_label = QLabel()

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        self.status_label.setWordWrap(
            True
        )

        self.status_label.setMinimumHeight(
            35
        )

        card_layout.addWidget(
            self.status_label
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        button_layout = QHBoxLayout()

        self.login_button = QPushButton(
            "LOGIN"
        )

        self.login_button.clicked.connect(
            self._handle_login
        )

        self.cancel_button = QPushButton(
            "EXIT"
        )

        self.cancel_button.clicked.connect(
            self._handle_cancel
        )

        button_layout.addWidget(
            self.login_button
        )

        button_layout.addWidget(
            self.cancel_button
        )

        card_layout.addLayout(
            button_layout
        )

        outer_layout.addWidget(
            card
        )

        outer_layout.addStretch()

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = QLabel(
            "APS Financial Solutions"
        )

        footer.setAlignment(
            Qt.AlignCenter
        )

        footer.setStyleSheet(
            """
            color: #666666;
            font-size: 9px;
            """
        )

        outer_layout.addWidget(
            footer
        )

        self.username_input.setFocus()

    def _handle_login(self) -> None:
        """
        Authenticate the entered credentials.
        """

        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username:
            self._show_error(
                "Please enter your username."
            )

            self.username_input.setFocus()

            return

        if not password:
            self._show_error(
                "Please enter your password."
            )

            self.password_input.setFocus()

            return

        self.login_button.setEnabled(
            False
        )

        self.status_label.clear()

        try:
            result = authentication_service.authenticate(
                username,
                password,
            )

            if not result.success:
                self._show_error(
                    result.message
                )

                self.password_input.clear()
                self.password_input.setFocus()

                return

            if result.user_id is None:
                logger.error(
                    "Authentication succeeded without a user ID."
                )

                self._show_error(
                    "Authentication error. Please contact the administrator."
                )

                return

            if result.full_name is None:
                logger.error(
                    "Authentication succeeded without a full name."
                )

                self._show_error(
                    "Authentication error. Please contact the administrator."
                )

                return

            if result.role is None:
                logger.error(
                    "Authentication succeeded without a role."
                )

                self._show_error(
                    "Authentication error. Please contact the administrator."
                )

                return

            session.start(
                user_id=result.user_id,
                username=result.username,
                full_name=result.full_name,
                role=result.role,
            )

            logger.info(
                "Login window authentication completed for '%s'.",
                result.username,
            )

            self.status_label.setText(
                "Login successful."
            )

            self.status_label.setStyleSheet(
                """
                color: #7CFC00;
                font-weight: bold;
                """
            )

            self.authenticated.emit()

        except RuntimeError as exc:
            logger.error(
                "Unable to establish user session: %s",
                exc,
            )

            self._show_error(
                "A user session is already active."
            )

        except Exception:
            logger.exception(
                "Unexpected login window error."
            )

            self._show_error(
                "An unexpected error occurred. Please contact the administrator."
            )

        finally:
            self.login_button.setEnabled(
                True
            )

    def _handle_cancel(self) -> None:
        """
        Cancel the login operation and request application exit.
        """

        logger.info(
            "Login cancelled by user."
        )

        self.login_cancelled.emit()

        self.close()

    def _show_error(
        self,
        message: str,
    ) -> None:
        """
        Display a login error message.
        """

        self.status_label.setText(
            message
        )

        self.status_label.setStyleSheet(
            """
            color: #FF6B6B;
            font-weight: bold;
            """
        )

    def clear_credentials(self) -> None:
        """
        Clear credentials from the login form.
        """

        self.username_input.clear()
        self.password_input.clear()

        self.status_label.clear()

        self.username_input.setFocus()