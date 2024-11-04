"""
Tests for the pwd command
"""

import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from skylock_cli.cli import app
from tests.helpers import mock_test_context

runner = CliRunner()


class TestPWDCommand(unittest.TestCase):
    """Test cases for the pwd command"""

    @patch("skylock_cli.model.token.Token.is_expired", return_value=True)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=False)
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_pwd_token_invalid(
        self, mock_get_context, _mock_is_valid, _mock_is_expired
    ):
        """Test the pwd command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["pwd"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("User token is invalid. Login again to continue.", result.output)

    @patch("skylock_cli.model.token.Token.is_expired", return_value=True)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_pwd_token_expired(
        self, mock_get_context, _mock_is_valid, _mock_is_expired
    ):
        """Test the pwd command with an expired token"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["pwd"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("User token has expired. Login again to continue.", result.output)

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_pwd_success(self, mock_get_context, _mock_is_valid, _mock_is_expired):
        """Test the pwd command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["pwd"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.output)


if __name__ == "__main__":
    unittest.main()
