from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.version import APP_NAME, VERSION, BUILD


# ============================================================
# APPLICATION ROOT
# ============================================================

ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# APPLICATION DIRECTORIES
# ============================================================

CONFIG_DIR = ROOT / "config"
LOG_DIR = ROOT / "logs"
BACKUP_DIR = ROOT / "backups"
DOCUMENT_DIR = ROOT / "customer_documents"
DATABASE_DIR = ROOT / "database"
ASSETS_DIR = ROOT / "assets"


# ============================================================
# APPLICATION FILES
# ============================================================

CONFIG_FILE = CONFIG_DIR / "aps_settings.json"
DATABASE_FILE = DATABASE_DIR / "aps.db"
LOG_FILE = LOG_DIR / "aps.log"


# ============================================================
# DEFAULT SETTINGS
# ============================================================

DEFAULT_SETTINGS: dict[str, Any] = {
    "application": {
        "name": APP_NAME,
        "version": VERSION,
        "build": BUILD,
        "environment": "development",
    },
    "storage": {
        "database_directory": str(DATABASE_DIR),
        "document_directory": str(DOCUMENT_DIR),
        "backup_directory": str(BACKUP_DIR),
        "log_directory": str(LOG_DIR),
    },
    "database": {
        "filename": DATABASE_FILE.name,
        "schema_version": 0,
    },
    "system": {
        "auto_backup_enabled": True,
        "logging_enabled": True,
    },
}


# ============================================================
# DIRECTORY INITIALIZATION
# ============================================================

def ensure_directories() -> None:
    """
    Create all directories required by the application.
    Existing directories are left unchanged.
    """

    directories = [
        CONFIG_DIR,
        LOG_DIR,
        BACKUP_DIR,
        DOCUMENT_DIR,
        DATABASE_DIR,
        ASSETS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# ============================================================
# SETTINGS FILE
# ============================================================

def save_settings(settings: dict[str, Any]) -> None:
    """
    Save application settings to the JSON configuration file.
    """

    ensure_directories()

    temporary_file = CONFIG_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(
            settings,
            file,
            indent=4,
            ensure_ascii=False,
        )

    temporary_file.replace(CONFIG_FILE)


def load_settings() -> dict[str, Any]:
    """
    Load application settings.

    If the configuration file does not exist or is invalid,
    the default configuration is recreated.
    """

    ensure_directories()

    if not CONFIG_FILE.exists():
        settings = DEFAULT_SETTINGS.copy()
        save_settings(settings)
        return settings

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            settings = json.load(file)

        if not isinstance(settings, dict):
            raise ValueError("Configuration root must be an object.")

        return settings

    except (OSError, json.JSONDecodeError, ValueError):
        settings = DEFAULT_SETTINGS.copy()
        save_settings(settings)
        return settings


# ============================================================
# APPLICATION PATH INFORMATION
# ============================================================

def get_application_paths() -> dict[str, Path]:
    """
    Return the important APS application paths.
    """

    return {
        "root": ROOT,
        "config": CONFIG_DIR,
        "logs": LOG_DIR,
        "backups": BACKUP_DIR,
        "documents": DOCUMENT_DIR,
        "database": DATABASE_DIR,
        "assets": ASSETS_DIR,
        "database_file": DATABASE_FILE,
        "log_file": LOG_FILE,
        "config_file": CONFIG_FILE,
    }


# ============================================================
# STARTUP INITIALIZATION
# ============================================================

ensure_directories()