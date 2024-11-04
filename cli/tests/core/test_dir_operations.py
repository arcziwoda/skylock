"""
Test cases for the functions from core.dir_operations
"""

import unittest
from http import HTTPStatus
from unittest.mock import patch
from pathlib import Path
from io import StringIO
from click import exceptions
from skylock_cli.core.dir_operations import create_directory, remove_directory
from tests.helpers import mock_response_with_status, mock_test_context


class TestCreateDirectory(unittest.TestCase):
    """Test cases for the create_directory function from core.dir_operations"""

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_success(self, mock_post):
        """Test successful directory creation"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.CREATED)

        create_directory("test_dir", False)
        mock_post.assert_called_once()

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_success_parent(self, mock_post):
        """Test successful directory creation"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.CREATED)

        create_directory("test_dir", True)
        mock_post.assert_called_once()

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_already_exists(self, mock_post):
        """Test registration when the user already exists"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.UNAUTHORIZED)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir", False)
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
                create_directory("test_dir", False)
            self.assertIn("Directory `/test_dir` already exists!", mock_stderr.getvalue())

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_skylock_api_error(self, mock_post):
        """Test registration with a SkyLockAPIError"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.INTERNAL_SERVER_ERROR)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir", False)
            self.assertIn(
                "Failed to create directory (Internal Server Error)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_connection_error(self, mock_post):
        """Test registration when a ConnectionError occurs (backend is offline)"""
        mock_post.side_effect = ConnectionError("Failed to connect to the server. Please check your network connection.")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir", False)
            self.assertIn(
                "ConnectionError: Failed to connect to the server. Please check your network \nconnection.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_invalid_path(self, mock_post):
        """Test registration when the path is invalid (BAD_REQUEST)"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.BAD_REQUEST)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("/test_dir1/test_dir2", False)
            self.assertIn("Invalid path `/test_dir1/test_dir2`", mock_stderr.getvalue())

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_not_found(self, mock_post):
        """Test registration when the directory is not found (NOT_FOUND)"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)
        mock_post.return_value.json.return_value = {"missing": "test_dir2"}

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("/test_dir1/test_dir2", False)
            self.assertIn(
                "Directory `test_dir2` is missing! Use the --parent flag to create parent \ndirectories.\n",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_not_found_with_parent_flag(self, mock_post):
        """Test registration when the directory is not found (NOT_FOUND)"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)
        mock_post.return_value.json.return_value = {"missing": "test_dir2"}

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("/test_dir1/test_dir2", True)
            self.assertIn(
                "Failed to create directory (Internal Server Error)",
                mock_stderr.getvalue(),
            )


class TestRemoveDirectory(unittest.TestCase):
    """Test cases for the remove_directory function from core.dir_operations"""

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_success(self, mock_delete):
        """Test successful directory removal"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.NO_CONTENT)

        remove_directory("test_dir/", False)
        mock_delete.assert_called_once()

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_success_recursive(self, mock_delete):
        """Test successful directory removal"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.NO_CONTENT)

        remove_directory("test_dir/", True)
        mock_delete.assert_called_once()

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_not_found(self, mock_delete):
        """Test removal when the directory is not found"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("/test1/test2/", False)
            self.assertIn("Directory `/test1/test2` does not exist!\n", mock_stderr.getvalue())

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_skylock_api_error(self, mock_delete):
        """Test removal with a SkyLockAPIError"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.INTERNAL_SERVER_ERROR)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", False)
            self.assertIn(
                "Failed to delete directory (Internal Server Error)\n",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_connection_error(self, mock_delete):
        """Test removal when a ConnectionError occurs (backend is offline)"""
        mock_delete.side_effect = ConnectionError("Failed to connect to the server. Please check your network connection.")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", False)
            self.assertIn(
                "ConnectionError: Failed to connect to the server. Please check your network \nconnection.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_unauthorized(self, mock_delete):
        """Test removal when the user is unauthorized"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.UNAUTHORIZED)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", False)
            self.assertIn(
                "User is unauthorized. Please login to use this command.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_with_files(self, mock_delete):
        """Test removal when the directory is not empty"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.CONFLICT)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", False)
            self.assertIn(
                "Directory `/test_dir` is not empty! Use the --recursive flag to delete it \nrecursively.\n",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_with_files_but_recursive(self, mock_delete):
        """Test removal when the directory is not empty but recursive flag is set"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.CONFLICT)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", True)
            self.assertIn(
                "Failed to delete directory (Internal Server Error)\n",
                mock_stderr.getvalue(),
            )

    def test_remove_not_a_directory_error(self):
        """Test removal when the path is not a directory"""

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("/file", False)
            self.assertIn("/file is not a directory", mock_stderr.getvalue())

    def test_remove_root_directory_error(self):
        """Test removal when the path is the root directory"""

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("/", False)
            self.assertIn("Cannot delete the root directory", mock_stderr.getvalue())

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.context_manager.ContextManager.save_context", return_value=None)
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    @patch("skylock_cli.api.nav_requests.client.get")
    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_change_cwd(self, mock_delete, mock_change_dir, mock_context, _mock_save_context, _mock_is_valid, _mock_is_expired):
        """Test removal when the directory is the current working directory"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.NO_CONTENT)
        mock_change_dir.return_value = mock_response_with_status(HTTPStatus.OK)
        mock_context.return_value = mock_test_context(path=Path("/test/"))

        with patch("skylock_cli.core.dir_operations.change_directory") as mock_change_directory:
            remove_directory("/test/", True)
            mock_delete.assert_called_once()
            mock_change_directory.assert_called_once_with("/")


if __name__ == "__main__":
    unittest.main()
