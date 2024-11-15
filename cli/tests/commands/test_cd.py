"""
Tests for the cd command
"""

import unittest
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from httpx import ConnectError
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import assert_connect_error, mock_test_context

runner = CliRunner()


class TestCDCommand(unittest.TestCase):
    """Test cases for the cd command"""

    @patch("skylock_cli.core.nav.send_cd_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    @patch("skylock_cli.core.context_manager.ContextManager.save_context")
    def test_cd_success(self, mock_save_context, mock_get_context, mock_send):
        """Test the cd command"""
        mock_get_context.return_value = mock_test_context()

        mock_save_context.return_value = None

        mock_send.return_value = None

        result = runner.invoke(app, ["cd", "test_dir"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir")
        )

    @patch("skylock_cli.core.nav.send_cd_request")
    def test_cd_token_expired(self, mock_send):
        """Test the cd command when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = runner.invoke(app, ["cd", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.nav.send_cd_request")
    def test_cd_directory_not_found_error(self, mock_send):
        """Test the cd command when a DirectoryNotFoundError occurs"""
        mock_send.side_effect = api_exceptions.DirectoryNotFoundError("/test_dir")

        result = runner.invoke(app, ["cd", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `/test_dir` does not exist!", result.output)

    @patch("skylock_cli.core.nav.send_cd_request")
    def test_cd_skylock_api_error(self, mock_send):
        """Test the cd command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to change directory (Internal Server Error)"
        )

        result = runner.invoke(app, ["cd", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to change directory (Internal Server Error)", result.output
        )

    @patch("skylock_cli.core.nav.send_cd_request")
    def test_cd_connection_error(self, mock_send):
        """Test the cd command when a Connect Eroor occurs (server is down)"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        result = runner.invoke(app, ["cd", "test_dir/"])
        assert_connect_error(result)


if __name__ == "__main__":
    unittest.main()
