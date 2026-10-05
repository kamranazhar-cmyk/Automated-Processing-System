from __future__ import annotations

from datetime import datetime, timezone

from core.logger import get_logger
from database.connection import database


logger = get_logger("DatabaseInitializer")


DATABASE_SCHEMA_VERSION = 0


def initialize_database() -> None:
    """
    Initialize the APS SQLite database infrastructure.

    APS-001B intentionally creates only the system metadata
    structure. Business tables will be implemented in APS-002.
    """

    logger.info("Starting database initialization.")

    with database.session() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS system_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        current_time = datetime.now(timezone.utc).isoformat()

        metadata = {
            "application": "Automated Processing System",
            "schema_version": str(DATABASE_SCHEMA_VERSION),
            "database_status": "initialized",
        }

        for key, value in metadata.items():

            connection.execute(
                """
                INSERT INTO system_metadata (
                    key,
                    value,
                    updated_at
                )
                VALUES (?, ?, ?)
                ON CONFLICT(key)
                DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (
                    key,
                    value,
                    current_time,
                ),
            )

    logger.info(
        "Database initialization completed successfully."
    )


def get_database_schema_version() -> int:
    """
    Return the currently installed database schema version.
    """

    with database.session() as connection:

        result = connection.execute(
            """
            SELECT value
            FROM system_metadata
            WHERE key = 'schema_version'
            """
        ).fetchone()

    if result is None:
        return DATABASE_SCHEMA_VERSION

    try:
        return int(result["value"])
    except (TypeError, ValueError):
        return DATABASE_SCHEMA_VERSION