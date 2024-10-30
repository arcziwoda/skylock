"""
Test cases for the functions from core.dir_operations
"""

import unittest
from http import HTTPStatus
from unittest.mock import patch
from io import StringIO
from click import exceptions
from skylock_cli.core.dir_operations import create_directory
from tests.helpers import mock_response_with_status


class TestCreateDirectory(unittest.TestCase):
    """Test cases for the create_directory function from core.dir_operations"""

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_success(self, mock_post):
        """Test successful directory creation"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.CREATED)

        create_directory("test_dir")
        mock_post.assert_called_once()

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_already_exists(self, mock_post):
        """Test registration when the user already exists"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.UNAUTHORIZED)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir")
            self.assertIn(
                "User is unauthorized. Please login to use this command.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_dir_already_exists(self, mock_post):
        """Test registration when the directory already exists"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.CONFLICT)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir")
            self.assertIn(
                "Directory `/test_dir` already exists!", mock_stderr.getvalue()
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_skylock_api_error(self, mock_post):
        """Test registration with a SkyLockAPIError"""
        mock_post.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir")
            self.assertIn(
                "Failed to create directory (Internal Server Error)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_connection_error(self, mock_post):
        """Test registration when a ConnectionError occurs (backend is offline)"""
        mock_post.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir")
            self.assertIn(
                "ConnectionError: Failed to connect to the server. Please check your network \nconnection.",
                mock_stderr.getvalue(),
            )


if __name__ == "__main__":
    unittest.main()
