from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from core.settings import DATABASE_FILE
from core.version import APP_NAME, BUILD, VERSION


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            f"{APP_NAME} {VERSION}"
        )

        self.resize(
            1400,
            850,
        )

        self._build_ui()

    def _build_ui(self) -> None:

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout(
            central
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QLabel(
            APP_NAME
        )

        header.setAlignment(
            Qt.AlignCenter
        )

        header.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            color: #D4AF37;
            """
        )

        layout.addWidget(
            header
        )

        version_label = QLabel(
            f"Version {VERSION}  |  {BUILD}"
        )

        version_label.setAlignment(
            Qt.AlignCenter
        )

        version_label.setStyleSheet(
            """
            color: #999999;
            font-size: 10px;
            """
        )

        layout.addWidget(
            version_label
        )

        # ----------------------------------------------------
        # DASHBOARD CARDS
        # ----------------------------------------------------

        grid = QGridLayout()

        cards = [
            "Affiliated Banks",
            "User Performance",
            "Approval Rate",
            "Decline Rate",
            "Fraud Detection",
            "Agency Performance",
            "Market News",
            "Administrator Messages",
        ]

        row = 0
        col = 0

        for title in cards:

            frame = QFrame()

            box = QVBoxLayout(
                frame
            )

            label = QLabel(
                title
            )

            label.setAlignment(
                Qt.AlignCenter
            )

            label.setStyleSheet(
                """
                color: #D4AF37;
                font-weight: bold;
                font-size: 13px;
                """
            )

            value = QLabel(
                "Coming Soon"
            )

            value.setAlignment(
                Qt.AlignCenter
            )

            value.setStyleSheet(
                """
                color: #CCCCCC;
                font-size: 11px;
                """
            )

            box.addWidget(
                label
            )

            box.addStretch()

            box.addWidget(
                value
            )

            box.addStretch()

            frame.setMinimumHeight(
                160
            )

            grid.addWidget(
                frame,
                row,
                col,
            )

            col += 1

            if col == 4:
                col = 0
                row += 1

        layout.addLayout(
            grid
        )

        # ----------------------------------------------------
        # STATUS INFORMATION
        # ----------------------------------------------------

        self.statusBar().showMessage(
            f"System Ready | Database: {DATABASE_FILE.name}"
        )

        self._add_footer(
            layout
        )

    def _add_footer(
        self,
        layout: QVBoxLayout,
    ) -> None:

        footer = QLabel(
            "APS Financial Solutions | Automated Processing System"
        )

        footer.setAlignment(
            Qt.AlignCenter
        )

        footer.setStyleSheet(
            """
            color: #777777;
            font-size: 9px;
            padding: 8px;
            """
        )

        layout.addWidget(
            footer
        )