"""
Module to manage the context of the CLI.
"""

from pathlib import Path
import json
from skylock_cli.model.context import Context
from skylock_cli.scripts.setup_config import create_config_file
from skylock_cli.config import CONFIG_DIR, CONFIG_FILE_NAME


class ContextManager:
    """Context manager class."""

    context_file_path = Path(CONFIG_DIR) / CONFIG_FILE_NAME

    @classmethod
    def ensure_context_file_exists(cls) -> None:
        """Ensure that the context file exists."""
        if not cls.context_file_path.exists():
            create_config_file()

    @classmethod
    def get_context(cls) -> Context:
        """Extract context from the JSON file."""
        cls.ensure_context_file_exists()
        with cls.context_file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return Context(**data.get("context", {}))

    @classmethod
    def save_context(cls, context: Context) -> None:
        """Save context to the JSON file."""
        cls.ensure_context_file_exists()
        with cls.context_file_path.open("w", encoding="utf-8") as file:
            json.dump({"context": context.model_dump()}, file, indent=4)
