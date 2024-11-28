"""
Tests for the make-private command
"""

import unittest
from unittest.mock import patch
from httpx import ConnectError
from typer.testing import CliRunner
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import mock_test_context, assert_connect_error


class TestMakeprivateCommand(unittest.TestCase):
    """Test cases for the make-private command"""

    def setUp(self):
        self.runner = CliRunner()

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.dir_operations.send_make_private_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_make_private_directory_success(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()
        mock_send.return_value = {"name": "test_dir", "path": "", "is_public": False}

        result = self.runner.invoke(app, ["make-private", "test_dir/"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.output)
        self.assertIn("Directory test_dir/ is now private 🔐", result.output)

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.file_operations.send_make_private_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_make_private_file_success(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the mkdir command"""
        mock_get_context.return_value = mock_test_context()
        mock_send.return_value = {
            "name": "test_file.txt",
            "path": "",
            "is_public": False,
        }

        result = self.runner.invoke(app, ["make-private", "test_file.txt"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.output)
        self.assertIn("File test_file.txt is now private 🔐", result.output)

    @patch("skylock_cli.core.dir_operations.send_make_private_request")
    def test_make_private_directory_token_expired(self, mock_send):
        """Test the make-private command of directory when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = self.runner.invoke(app, ["make-private", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_make_private_request")
    def test_make_private_directory_not_found_error(self, mock_send):
        """Test the make-private command of directory when a DirectoryNotFoundError occurs"""
        mock_send.side_effect = api_exceptions.DirectoryNotFoundError("/test_dir")

        result = self.runner.invoke(app, ["make-private", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `/test_dir` does not exist!", result.output)

    @patch("skylock_cli.core.dir_operations.send_make_private_request")
    def test_make_private_directory_skylock_api_error(self, mock_send):
        """Test the make-private command of directory when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to delete file (Internal Server Error)"
        )

        result = self.runner.invoke(app, ["make-private", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to delete file (Internal Server Error)", result.output)

    @patch("skylock_cli.core.dir_operations.send_make_private_request")
    def test_make_private_directory_connection_error(self, mock_send):
        """Test the make-private command of directory when a ConnectError occurs (backend is offline)"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        result = self.runner.invoke(app, ["make-private", "test_dir/"])
        assert_connect_error(result)

    @patch("skylock_cli.core.file_operations.send_make_private_request")
    def test_make_private_file_token_expired(self, mock_send):
        """Test the make-private command for a file when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = self.runner.invoke(app, ["make-private", "test_file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.file_operations.send_make_private_request")
    def test_make_private_file_not_found_error(self, mock_send):
        """Test the make-private command for a file when a FileNotFoundError occurs"""
        mock_send.side_effect = api_exceptions.FileNotFoundError("/test_file.txt")

        result = self.runner.invoke(app, ["make-private", "test_file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("File `/test_file.txt` does not exist!", result.output)

    @patch("skylock_cli.core.file_operations.send_make_private_request")
    def test_make_private_file_skylock_api_error(self, mock_send):
        """Test the make-private command for a file when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to make file private (Internal Server Error)"
        )

        result = self.runner.invoke(app, ["make-private", "test_file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to make file private (Internal Server Error)", result.output
        )

    @patch("skylock_cli.core.file_operations.send_make_private_request")
    def test_make_private_file_connection_error(self, mock_send):
        """Test the make-private command for a file when a ConnectError occurs (backend is offline)"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        result = self.runner.invoke(app, ["make-private", "test_file.txt"])
        assert_connect_error(result)


if __name__ == "__main__":
    unittest.main()
