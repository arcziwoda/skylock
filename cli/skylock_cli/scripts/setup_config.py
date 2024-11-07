"""
Script to create the config file.
"""

from pathlib import Path
import json
from skylock_cli.config import (
    CONFIG_DIR,
    CONFIG_FILE_NAME,
    EMPTY_CONTEXT,
    DOWNLOADS_DIR,
)


def create_config_file() -> None:
    """Creates the config file."""

    config_dir_path = Path(CONFIG_DIR)
    config_file_path = config_dir_path / CONFIG_FILE_NAME

    config_dir_path.mkdir(parents=True, exist_ok=True)

    with config_file_path.open("w", encoding="utf-8") as f:
        json.dump({"context": EMPTY_CONTEXT}, f, indent=4)


def create_downloads_dir() -> None:
    """Creates the downloads directory."""
    if not DOWNLOADS_DIR.exists():
        DOWNLOADS_DIR.mkdir(parents=True)
