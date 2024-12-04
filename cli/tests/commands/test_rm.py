"""
Tests for the rm command
"""

import unittest
from pathlib import Path
from unittest.mock import patch
from httpx import ConnectError
from typer.testing import CliRunner
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import mock_test_context, assert_connect_error


class TestRMCommand(unittest.TestCase):
    """Test cases for the rm command"""

    def setUp(self):
        """Create a runner to invoke the commands"""
        self.runner = CliRunner()

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.file_operations.file_requests.send_rm_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rm_success(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the rm command"""
        mock_get_context.return_value = mock_test_context()

        result = self.runner.invoke(app, ["rm", "test.txt"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test.txt")
        )
        self.assertIn("File /test.txt removed successfully", result.output)
        self.assertIn("Current working directory: /", result.output)

    def test_rm_not_a_file_error(self):
        """Test the rm command with a directory path"""
        result = self.runner.invoke(app, ["rm", "test/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("test/ is not a file", result.output)

    @patch("skylock_cli.core.file_operations.file_requests.send_rm_request")
    def test_rm_token_expired(self, mock_send):
        """Test the rm command when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = self.runner.invoke(app, ["rm", "test.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.file_operations.file_requests.send_rm_request")
    def test_rm_file_not_found_error(self, mock_send):
        """Test the rm command when a FileNotFoundError occurs"""
        mock_send.side_effect = api_exceptions.FileNotFoundError("test.txt")

        result = self.runner.invoke(app, ["rm", "test.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("File `test.txt` does not exist!", result.output)

    @patch("skylock_cli.core.file_operations.file_requests.send_rm_request")
    def test_rm_skylock_api_error(self, mock_send):
        """Test the rm command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to delete file (Internal Server Error)"
        )

        result = self.runner.invoke(app, ["rm", "test.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to delete file (Internal Server Error)", result.output)

    @patch("skylock_cli.core.file_operations.file_requests.send_rm_request")
    def test_rm_connection_error(self, mock_send):
        """Test the rm command when a ConnectError occurs (backend is offline)"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        result = self.runner.invoke(app, ["rm", "test.txt"])
        assert_connect_error(result)


if __name__ == "__main__":
    unittest.main()
