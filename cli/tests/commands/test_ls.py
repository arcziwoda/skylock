"""
Tests for the ls command
"""

import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import assert_connection_error, mock_test_context

runner = CliRunner()


class TestLSCommand(unittest.TestCase):
    """Test cases for the ls command"""

    @patch("skylock_cli.core.nav.send_ls_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_ls_success(self, mock_get_context, mock_send):
        """Test the ls command"""
        mock_get_context.return_value = mock_test_context()

        mock_files = [
            {"name": "file1.txt", "path": "/file1.txt"},
            {"name": "file2.txt", "path": "/file2.txt"},
        ]
        mock_folders = [
            {"name": "folder1", "path": "/folder1"},
            {"name": "folder2", "path": "/folder2"},
        ]

        mock_send.return_value = {"files": mock_files, "folders": mock_folders}

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("file1.txt  file2.txt  folder1/  folder2/", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_ls_success_empty(self, mock_get_context, mock_send):
        """Test the ls command"""
        mock_get_context.return_value = mock_test_context()

        mock_send.return_value = {"files": [], "folders": []}

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No contents in directory", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_ls_success_only_files(self, mock_get_context, mock_send):
        """Test the ls command"""
        mock_get_context.return_value = mock_test_context()

        mock_files = [
            {"name": "file1.txt", "path": "/file1.txt"},
            {"name": "file2.txt", "path": "/file2.txt"},
        ]
        mock_folders = []

        mock_send.return_value = {"files": mock_files, "folders": mock_folders}

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("file1.txt  file2.txt", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_ls_success_only_folders(self, mock_get_context, mock_send):
        """Test the ls command"""
        mock_get_context.return_value = mock_test_context()

        mock_files = []
        mock_folders = [
            {"name": "folder1", "path": "/folder1"},
            {"name": "folder2", "path": "/folder2"},
        ]

        mock_send.return_value = {"files": mock_files, "folders": mock_folders}

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("folder1/  folder2/", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    def test_ls_user_unathorized(self, mock_send):
        """Test the ls command when the user is unauthorized"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("User is unauthorized. Please login to use this command.", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    def test_ls_skylock_api_error(self, mock_send):
        """Test the ls command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError("An unexpected API error occurred")

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("An unexpected API error occurred", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    def test_ls_connection_error(self, mock_send):
        """Test the ls command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError("Failed to connect to the server. Please check your network connection.")

        result = runner.invoke(app, ["ls"])
        assert_connection_error(result)

    @patch("skylock_cli.core.nav.send_ls_request")
    def test_ls_directory_not_found(self, mock_send):
        """Test the ls command when a DirectoryNotFoundError occurs"""
        mock_send.side_effect = api_exceptions.DirectoryNotFoundError("/test")

        result = runner.invoke(app, ["ls", "/test"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `/test` does not exist!", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    def test_ls_invalid_response_format(self, mock_send):
        """Test the ls command when an InvalidResponseFormatError occurs"""
        mock_send.side_effect = api_exceptions.InvalidResponseFormatError()

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid response format! (Internal Server Error)", result.output)


if __name__ == "__main__":
    unittest.main()
