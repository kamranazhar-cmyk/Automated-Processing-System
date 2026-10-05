from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from core.version import APP_NAME, BUILD, VERSION


class SplashScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
        )

        self.setFixedSize(
            520,
            320,
        )

        self._build_ui()

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        title = QLabel(APP_NAME)

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            color: #D4AF37;
            """
        )

        version = QLabel(
            f"Version {VERSION}"
        )

        version.setAlignment(
            Qt.AlignCenter
        )

        version.setStyleSheet(
            """
            color: white;
            font-size: 12px;
            """
        )

        build = QLabel(
            f"Build {BUILD}"
        )

        build.setAlignment(
            Qt.AlignCenter
        )

        build.setStyleSheet(
            """
            color: #AAAAAA;
            font-size: 10px;
            """
        )

        loading = QLabel(
            "Initializing System..."
        )

        loading.setAlignment(
            Qt.AlignCenter
        )

        loading.setStyleSheet(
            """
            color: #D4AF37;
            font-size: 14px;
            """
        )

        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(build)

        layout.addStretch()

        layout.addWidget(loading)

        layout.addStretch()

    def finish(self, window) -> None:
        """
        Close the splash screen after the main window
        has been prepared.
        """

        self.close()