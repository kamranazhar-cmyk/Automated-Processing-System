from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from core.logger import get_logger
from core.settings import DATABASE_FILE, ensure_directories


logger = get_logger("Database")


class DatabaseConnection:
    """
    Central SQLite connection manager for APS.

    APS-001B establishes the database infrastructure.
    Actual business tables will be introduced in APS-002.
    """

    def __init__(self, database_path: Path | None = None):
        self.database_path = database_path or DATABASE_FILE

    def connect(self) -> sqlite3.Connection:
        """
        Create and configure a SQLite connection.
        """

        ensure_directories()

        connection = sqlite3.connect(
            self.database_path,
            timeout=30,
        )

        connection.row_factory = sqlite3.Row

        # Enforce relational integrity.
        connection.execute("PRAGMA foreign_keys = ON")

        # Improve reliability for future multi-operation workloads.
        connection.execute("PRAGMA busy_timeout = 30000")

        # WAL provides better read/write concurrency for SQLite.
        connection.execute("PRAGMA journal_mode = WAL")

        logger.debug(
            "Database connection opened: %s",
            self.database_path,
        )

        return connection

    @contextmanager
    def session(self) -> Iterator[sqlite3.Connection]:
        """
        Provide a managed database session.

        Successful operations are committed.
        Failed operations are rolled back.
        """

        connection = self.connect()

        try:
            yield connection
            connection.commit()

        except Exception:
            connection.rollback()

            logger.exception(
                "Database transaction failed."
            )

            raise

        finally:
            connection.close()

            logger.debug(
                "Database connection closed."
            )


database = DatabaseConnection()