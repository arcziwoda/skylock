"""
This file contains the configuration for the CLI.
"""

import appdirs

API_URL = "http://localhost:8000/api/v1"
API_HEADERS = {"Content-Type": "application/json"}
CONFIG_FILE_NAME = "skylock_config.json"
CONFIG_DIR = appdirs.user_config_dir("skylock")
