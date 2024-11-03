"""
Tests for the register command
"""

import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import assert_connection_error

runner = CliRunner()


class TestRegisterCommand(unittest.TestCase):
    """Test cases for the register command"""

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_success(self, mock_send):
        """Test the register command"""
        mock_send.return_value = None

        result = runner.invoke(app, ["register", "testuser1"], input="testpass1\ntestpass1")

        self.assertEqual(result.exit_code, 0)
        self.assertIn("User registered successfully", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_user_already_exists(self, mock_send):
        """Test the register command when the user already exists"""
        mock_send.side_effect = api_exceptions.UserAlreadyExistsError("testuser")

        result = runner.invoke(app, ["register", "testuser"], input="testpass\ntestpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("User with username `testuser` already exists!", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_skylock_api_error(self, mock_send):
        """Test the register command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError("An unexpected API error occurred")

        result = runner.invoke(app, ["register", "testuser2"], input="testpass2\ntestpass2")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("An unexpected API error occurred", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_connection_error(self, mock_send):
        """Test the register command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError("Failed to connect to the server. Please check your network connection.")

        result = runner.invoke(app, ["register", "testuser3"], input="testpass3\ntestpass3")
        assert_connection_error(result)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_password_mismatch(self, _mock_send):
        """Test the register command when the passwords do not match"""
        result = runner.invoke(app, ["register", "testuser4"], input="testpass4\ntestpass5")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Passwords do not match. Please try again.", result.output)


if __name__ == "__main__":
    unittest.main()
