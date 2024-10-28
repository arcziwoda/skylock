"""
Test the ContextManager class.
"""

import unittest
from unittest.mock import patch
from pathlib import Path
import json
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.model.context import Context, Token, UserDir


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
        cwd = UserDir(path=Path("/"))
        test_context = Context(token=test_token, user_dir=cwd)

        config_file_path = config_dir_path / "test_skylock_config.json"
        with config_file_path.open("w", encoding="utf-8") as f:
            json.dump({"context": test_context.model_dump()}, f, indent=4)

        # Initialize ContextManager and get context
        context_manager = ContextManager()
        context = context_manager.get_context()

        # Check the context object
        self.assertIsInstance(context, Context)
        self.assertIsInstance(context.token, Token)
        self.assertIsInstance(context.user_dir, UserDir)
        self.assertEqual(context.token.access_token, "test_token")
        self.assertEqual(context.token.token_type, "bearer")
        self.assertEqual(context.user_dir.path, Path("/"))

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

    @patch("skylock_cli.core.context_manager.ContextManager.ensure_context_file_exists")
    @patch(
        "skylock_cli.core.context_manager.ContextManager.context_file_path",
        Path("/tmp/test_skylock_config/test_skylock_config.json"),
    )
    def test_update_context(self, _mock_ensure_context_file_exists):
        """Test the update_context method."""
        # Create a temporary context file
        config_dir_path = Path("/tmp/test_skylock_config")
        config_dir_path.mkdir(parents=True, exist_ok=True)

        # Create test context object with an old token
        old_token = Token(access_token="old_token", token_type="bearer")
        old_dir = UserDir(path=Path("/old"))
        old_context = Context(token=old_token, user_dir=old_dir)

        # Initialize ContextManager and save old_context
        context_manager = ContextManager()
        context_manager.save_context(old_context)

        # Create test context object with a new token
        new_token = Token(access_token="new_token", token_type="bearer")
        new_context = Context(token=new_token)

        # Update the context
        context_manager.update_context(new_context)

        # Check the updated context file
        final_context = context_manager.get_context()

        self.assertIsInstance(final_context, Context)
        self.assertIsInstance(final_context.token, Token)
        self.assertIsInstance(final_context.user_dir, UserDir)
        self.assertEqual(final_context.token.access_token, "new_token")
        self.assertEqual(final_context.token.token_type, "bearer")
        self.assertEqual(final_context.user_dir.path, Path("/old"))

        # Clean up: delete the created file and directory
        config_file_path = config_dir_path / "test_skylock_config.json"
        config_file_path.unlink()
        config_dir_path.rmdir()


if __name__ == "__main__":
    unittest.main()
