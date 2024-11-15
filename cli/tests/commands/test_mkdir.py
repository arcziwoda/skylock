"""
Tests for the mkdir command
"""

import re
import unittest
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from httpx import ConnectError
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import mock_test_context, assert_connect_error

runner = CliRunner()


class TestMKDIRCommand(unittest.TestCase):
    """Test cases for the mdkir command"""

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success_parent_flag_long(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["mkdir", "test_dir", "--parent"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.output)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success_parent_flag_short(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["mkdir", "test_dir", "-p"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.output)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mdkir_token_expired(self, mock_send):
        """Test the mkdir command when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

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
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to create directory (Internal Server Error)"
        )

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to create directory (Internal Server Error)", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_connection_error(self, mock_send):
        """Test the mkdir command when a ConnectError occurs (backend is offline)"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        result = runner.invoke(app, ["mkdir", "test_dir"])
        assert_connect_error(result)

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
        self.assertRegex(
            result.output,
            re.compile(
                r"Directory `/child_dir` is missing! Use the --parent flag to create parent\s+directories\.\n",
                re.MULTILINE,
            ),
        )

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.output)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), False
        )


if __name__ == "__main__":
    unittest.main()
