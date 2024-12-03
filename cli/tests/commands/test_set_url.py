"""
Tests for the set-url command
"""

import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from skylock_cli.cli import app
from tests.helpers import mock_test_context


class TestSetURLCommand(unittest.TestCase):
    """Test cases for the set-url command"""

    def setUp(self):
        self.runner = CliRunner()

    @patch(
        "skylock_cli.core.context_manager.ContextManager.save_context",
        return_value=True,
    )
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    def test_set_url_success(self, _mock_get_context, _mock_save_context):
        """Test the set-url command"""
        result = self.runner.invoke(app, ["set-url", "http://localhost:8000"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Base URL set to http://localhost:8000", result.output)

    @patch(
        "skylock_cli.core.context_manager.ContextManager.save_context",
        return_value=False,
    )
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    def test_set_url_default(self, _mock_get_context, _mock_save_context):
        """Test the set-url command with the default URL"""
        result = self.runner.invoke(app, ["set-url"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Base URL set to http://localhost:8000", result.output)

    def test_set_url_invalid_url(self):
        """Test the set-url command with an invalid URL"""
        result = self.runner.invoke(app, ["set-url", "example.com"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Invalid URL: `example.com`. Please provide a valid URL.", result.output
        )


if __name__ == "__main__":
    unittest.main()
