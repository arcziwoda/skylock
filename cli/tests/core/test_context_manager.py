"""
Test the ContextManager class.
"""

import unittest
from unittest.mock import patch
from pathlib import Path
import json
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.model.context import Context
from skylock_cli.model.token import Token
from skylock_cli.model.directory import Directory


class TestContextManager(unittest.TestCase):
    """Test the ContextManager class."""

    @patch("skylock_cli.core.context_manager.ContextManager.ensure_context_file_exists")
    @patch(
        "skylock_cli.core.context_manager.ContextManager.context_file_path",
        Path("/tmp/test_skylock_config/test_skylock_config.json"),
    )
    def test_get_context(self, mock_ensure_context_file_exists):
        """Test the get_context method."""
        # Create a temporary context file
        config_dir_path = Path("/tmp/test_skylock_config")
        config_dir_path.mkdir(parents=True, exist_ok=True)

        # Create test context object with a test token
        test_token = Token(access_token="test_token", token_type="bearer")
        dir = Directory()
        test_context = Context(token=test_token, cwd=dir)

        config_file_path = config_dir_path / "test_skylock_config.json"
        with config_file_path.open("w", encoding="utf-8") as f:
            json.dump({"context": test_context.model_dump()}, f, indent=4)

        # Initialize ContextManager and get context
        context_manager = ContextManager()
        context = context_manager.get_context()

        # Check the context object
        self.assertIsInstance(context, Context)
        self.assertIsInstance(context.token, Token)
        self.assertIsInstance(context.cwd, Directory)
        self.assertEqual(context.token.access_token, "test_token")
        self.assertEqual(context.token.token_type, "bearer")
        self.assertEqual(context.cwd.path, Path("/"))
        self.assertEqual(context.cwd.name, "/")

        mock_ensure_context_file_exists.assert_called_once()

        # Clean up: delete the created file and directory
        config_file_path.unlink()  # Delete the file
        config_dir_path.rmdir()  # Delete the directory

    @patch("skylock_cli.core.context_manager.ContextManager.ensure_context_file_exists")
    @patch(
        "skylock_cli.core.context_manager.ContextManager.context_file_path",
        Path("/tmp/test_skylock_config/test_skylock_config.json"),
    )
    def test_save_context(self, mock_ensure_context_file_exists):
        """Test the save_context method."""
        # Create a temporary context file
        config_dir_path = Path("/tmp/test_skylock_config")
        config_dir_path.mkdir(parents=True, exist_ok=True)

        # Create test context object with a test token
        test_token = Token(access_token="test_token", token_type="bearer")
        test_context = Context(token=test_token)

        # Initialize ContextManager and save context
        context_manager = ContextManager()
        context_manager.save_context(test_context)

        # Check the saved context file
        config_file_path = config_dir_path / "test_skylock_config.json"
        with config_file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            context_data = data.get("context")
            self.assertIsInstance(context_data, dict)
            self.assertEqual(context_data.get("token").get("access_token"), "test_token")
            self.assertEqual(context_data.get("token").get("token_type"), "bearer")

        mock_ensure_context_file_exists.assert_called_once()

        # Clean up: delete the created file and directory
        config_file_path.unlink()
        config_dir_path.rmdir()


if __name__ == "__main__":
    unittest.main()
