"""
Tests for the mkdir command
"""

import unittest
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import mock_test_context

runner = CliRunner()


class TestMKDIRCommand(unittest.TestCase):
    """Test cases for the mdkir command"""

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success_parent_flag_long(self, mock_get_context, mock_send):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["mkdir", "test_dir", "--parent"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(mock_get_context.return_value.token, Path("/test_dir"), True)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success_parent_flag_short(self, mock_get_context, mock_send):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["mkdir", "test_dir", "-p"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(mock_get_context.return_value.token, Path("/test_dir"), True)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mdkir_token_expired(self, mock_send):
        """Test the mkdir command when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("User is unauthorized. Please login to use this command.", result.output)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_directory_already_exists(self, mock_send):
        """Test the mkdir command when the directory already exists"""
        mock_send.side_effect = api_exceptions.DirectoryAlreadyExistsError("test_dir")

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `test_dir` already exists!", result.output)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_skylock_api_error(self, mock_send):
        """Test the mkdir command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError("Failed to create directory (Internal Server Error)")

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to create directory (Internal Server Error)", result.output)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_connection_error(self, mock_send):
        """Test the mkdir command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError("Failed to connect to the server. Please check your network connection.")

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_invalid_path_error(self, mock_send):
        """Test the mkdir command when an InvalidPathError occurs"""
        mock_send.side_effect = api_exceptions.InvalidPathError("Invalid path")

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid path `Invalid path`!", result.output)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_directory_missing_error(self, mock_send):
        """Test the mkdir command when a DirectoryMissingError occurs"""
        mock_send.side_effect = api_exceptions.DirectoryMissingError("/child_dir")

        result = runner.invoke(app, ["mkdir", "test_dir/child_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Directory `/child_dir` is missing! Use the --parent flag to create parent \ndirectories.\n",
            result.output,
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success(self, mock_get_context, mock_send):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(mock_get_context.return_value.token, Path("/test_dir"), False)


if __name__ == "__main__":
    unittest.main()
