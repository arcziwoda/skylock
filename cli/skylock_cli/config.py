"""
This file contains the configuration for the CLI.
"""

from pathlib import Path
import appdirs

API_URL = "http://localhost:8000/api/v1"

API_HEADERS = {"Content-Type": "application/json"}

CONFIG_FILE_NAME = "skylock_config.json"

CONFIG_DIR = appdirs.user_config_dir("skylock")

DOWNLOADS_DIR = Path.home() / "Downloads"

ROOT_PATH = Path("/")

EMPTY_CONTEXT = {
    "token": {
        "access_token": "",
        "token_type": "",
    },
    "cwd": {
        "path": "/",
        "name": "/",
    },
}
