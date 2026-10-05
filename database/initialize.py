from __future__ import annotations

from datetime import datetime, timezone

from core.logger import get_logger
from database.connection import database
from database.models import DATABASE_SCHEMA_VERSION, SCHEMA_SQL


logger = get_logger("DatabaseInitializer")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def initialize_database() -> None:
    """
    Create and initialize the APS database schema.
    """

    logger.info("Starting APS database initialization.")

    with database.session() as connection:

        connection.executescript(
            SCHEMA_SQL
        )

        current_time = utc_now()

        metadata = {
            "application": "Automated Processing System",
            "schema_version": str(
                DATABASE_SCHEMA_VERSION
            ),
            "database_status": "initialized",
            "last_schema_update": current_time,
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
        "APS database schema version %s initialized.",
        DATABASE_SCHEMA_VERSION,
    )


def get_database_schema_version() -> int:
    """
    Return the installed APS database schema version.
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
        return 0

    try:
        return int(
            result["value"]
        )
    except (
        TypeError,
        ValueError,
    ):
        return 0