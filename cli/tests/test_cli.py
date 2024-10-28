"""
Tests for the CLI commands.
"""

import unittest
from pathlib import Path
from unittest.mock import patch, Mock
from typer.testing import CliRunner
from art import text2art
from skylock_cli.model.token import Token
from skylock_cli.cli import app
from skylock_cli.api.http_exceptions import (
    UserAlreadyExistsError,
    SkyLockAPIError,
    AuthenticationError,
    UserUnauthorizedError,
    DirectoryAlreadyExistsError,
)

runner = CliRunner()


class TestCLICommands(unittest.TestCase):
    """Test cases for the CLI commands"""

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_success(self, mock_send):
        """Test the register command"""
        mock_send.return_value = None

        result = runner.invoke(
            app, ["register", "testuser1"], input="testpass1\ntestpass1"
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("User registered successfully", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_user_already_exists(self, mock_send):
        """Test the register command when the user already exists"""
        mock_send.side_effect = UserAlreadyExistsError("testuser")

        result = runner.invoke(
            app, ["register", "testuser"], input="testpass\ntestpass"
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("User with username `testuser` already exists!", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_skylock_api_error(self, mock_send):
        """Test the register command when a SkyLockAPIError occurs"""
        mock_send.side_effect = SkyLockAPIError("An unexpected API error occurred")

        result = runner.invoke(
            app, ["register", "testuser2"], input="testpass2\ntestpass2"
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("An unexpected API error occurred", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_connection_error(self, mock_send):
        """Test the register command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(
            app, ["register", "testuser3"], input="testpass3\ntestpass3"
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )

    @patch("skylock_cli.core.auth.send_login_request")
    @patch("skylock_cli.core.auth.ContextManager.save_context")
    def test_login_success(self, mock_save_context, mock_send):
        """Test the login command"""
        mock_send.return_value = Mock(
            Token(access_token="test_token", token_type="bearer")
        )

        result = runner.invoke(app, ["login", "testuser"], input="testpass")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("User logged in successfully", result.output)
        self.assertIn("Hello, testuser", result.output)
        self.assertIn("Welcome to our file hosting service", result.output)
        self.assertIn(text2art("SkyLock"), result.output)
        self.assertIn("Your current working directory is: /", result.output)
        mock_save_context.assert_called_once()

    @patch("skylock_cli.core.auth.send_login_request")
    def test_login_authentication_error(self, mock_send):
        """Test the login command when an AuthenticationError occurs"""
        mock_send.side_effect = AuthenticationError()

        result = runner.invoke(app, ["login", "testuser"], input="wrongpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid username or password", result.output)

    @patch("skylock_cli.core.auth.send_login_request")
    def test_login_skylock_api_error(self, mock_send):
        """Test the login command when a SkyLockAPIError occurs"""
        mock_send.side_effect = SkyLockAPIError("An unexpected API error occurred")

        result = runner.invoke(app, ["login", "testuser"], input="testpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("An unexpected API error occurred", result.output)

    @patch("skylock_cli.core.auth.send_login_request")
    def test_login_connection_error(self, mock_send):
        """Test the login command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(app, ["login", "testuser"], input="testpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success(self, mock_get_context, mock_send):
        """Test the mkdir command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir")
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mdkir_token_expired(self, mock_send):
        """Test the mkdir command when the token has expired"""
        mock_send.side_effect = UserUnauthorizedError()

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_directory_already_exists(self, mock_send):
        """Test the mkdir command when the directory already exists"""
        mock_send.side_effect = DirectoryAlreadyExistsError("test_dir")

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `test_dir` already exists!", result.output)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_skylock_api_error(self, mock_send):
        """Test the mkdir command when a SkyLockAPIError occurs"""
        mock_send.side_effect = SkyLockAPIError(
            "Failed to create directory (Internal Server Error)"
        )

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to create directory (Internal Server Error)", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_connection_error(self, mock_send):
        """Test the mkdir command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )


if __name__ == "__main__":
    unittest.main()
