"""
Test cases for the functions from core.dir_operations
"""

import re
import unittest
from http import HTTPStatus
from unittest.mock import patch
from pathlib import Path
from io import StringIO
from click import exceptions
from httpx import ConnectError
from skylock_cli.core.dir_operations import (
    create_directory,
    remove_directory,
    make_directory_public,
    make_directory_private,
)
from tests.helpers import mock_response_with_status, mock_test_context


class TestCreateDirectory(unittest.TestCase):
    """Test cases for the create_directory function from core.dir_operations"""

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_success(self, mock_post):
        """Test successful directory creation"""
        return_json = {"name": "test_dir", "path": "", "is_public": False}
        mock_post.return_value = mock_response_with_status(
            HTTPStatus.CREATED, return_json
        )
        parent_flag = False
        public_flag = False

        new_dir = create_directory("test_dir", parent_flag, public_flag)
        mock_post.assert_called_once()
        self.assertEqual(new_dir.name, "test_dir/")
        self.assertEqual(new_dir.path, Path("."))
        self.assertFalse(new_dir.is_public)
        self.assertEqual(new_dir.color, "magenta")
        self.assertEqual(new_dir.type_label, "directory")
        self.assertEqual(new_dir.visibility_label, "private 🔐")
        self.assertEqual(new_dir.visibility_color, "red")

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_success_public(self, mock_post):
        """Test successful directory creation"""
        return_json = {"name": "test_dir", "path": "", "is_public": True}
        mock_post.return_value = mock_response_with_status(
            HTTPStatus.CREATED, return_json
        )
        parent_flag = False
        public_flag = True

        new_dir = create_directory("test_dir", parent_flag, public_flag)
        mock_post.assert_called_once()
        self.assertEqual(new_dir.name, "test_dir/")
        self.assertEqual(new_dir.path, Path("."))
        self.assertTrue(new_dir.is_public)
        self.assertEqual(new_dir.color, "magenta")
        self.assertEqual(new_dir.type_label, "directory")
        self.assertEqual(new_dir.visibility_label, "public 🔓")
        self.assertEqual(new_dir.visibility_color, "green")

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_already_exists(self, mock_post):
        """Test registration when the user already exists"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.UNAUTHORIZED)
        parent_flag = False
        public_flag = False

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir", parent_flag, public_flag)
            self.assertIn(
                "User is unauthorized. Please login to use this command.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_dir_already_exists(self, mock_post, mock_context):
        """Test registration when the directory already exists"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.CONFLICT)
        mock_context.return_value = mock_test_context()
        parent_flag = False
        public_flag = False

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir", parent_flag, public_flag)
            self.assertIn(
                "Directory `/test_dir` already exists!", mock_stderr.getvalue()
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_skylock_api_error(self, mock_post):
        """Test registration with a SkyLockAPIError"""
        mock_post.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )
        parent_flag = False
        public_flag = False

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir", parent_flag, public_flag)
            self.assertIn(
                "Failed to create directory (Error Code: 500)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_connection_error(self, mock_post):
        """Test registration when a ConnectError occurs (backend is offline)"""
        mock_post.side_effect = ConnectError("Failed to connect to the server")
        parent_flag = False
        public_flag = False

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("test_dir", parent_flag, public_flag)
            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_invalid_path(self, mock_post):
        """Test registration when the path is invalid (BAD_REQUEST)"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.BAD_REQUEST)
        parent_flag = False
        public_flag = False

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("/test_dir1/test_dir2", parent_flag, public_flag)
            self.assertIn("Invalid path `/test_dir1/test_dir2`", mock_stderr.getvalue())

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_not_found(self, mock_post):
        """Test registration when the directory is not found (NOT_FOUND)"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)
        mock_post.return_value.json.return_value = {"missing": "test_dir2"}
        parent_flag = False
        public_flag = False

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("/test_dir1/test_dir2", parent_flag, public_flag)
            self.assertRegex(
                mock_stderr.getvalue(),
                re.compile(
                    r"Directory `test_dir2` is missing! Use the --parent flag to create parent\s+directories\.\n",
                    re.MULTILINE,
                ),
            )

    @patch("skylock_cli.api.dir_requests.client.post")
    def test_create_directory_not_found_with_parent_flag(self, mock_post):
        """Test registration when the directory is not found (NOT_FOUND)"""
        mock_post.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)
        mock_post.return_value.json.return_value = {"missing": "test_dir2"}
        parent_flag = True
        public_flag = False

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                create_directory("/test_dir1/test_dir2", parent_flag, public_flag)
            self.assertIn(
                "Failed to create directory (Error Code: 404)",
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
            self.assertIn(
                "Directory `/test1/test2` does not exist!\n", mock_stderr.getvalue()
            )

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_skylock_api_error(self, mock_delete):
        """Test removal with a SkyLockAPIError"""
        mock_delete.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", False)
            self.assertIn(
                "Failed to delete directory (Error Code: 500)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_connection_error(self, mock_delete):
        """Test removal when a ConnectError occurs (backend is offline)"""
        mock_delete.side_effect = ConnectError("Failed to connect to the server")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", False)
            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
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

    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_with_files(self, mock_delete, mock_context):
        """Test removal when the directory is not empty"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.CONFLICT)
        mock_context.return_value = mock_test_context()

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", False)
            self.assertRegex(
                mock_stderr.getvalue(),
                re.compile(
                    r"Directory `/test_dir` is not empty! Use the --recursive flag to delete it\s+recursively\.\n",
                    re.MULTILINE,
                ),
            )

    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_with_files_but_recursive(self, mock_delete):
        """Test removal when the directory is not empty but recursive flag is set"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.CONFLICT)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_directory("test_dir/", True)
            self.assertIn(
                "Failed to delete directory (Error Code: 409)",
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
    @patch(
        "skylock_cli.core.context_manager.ContextManager.save_context",
        return_value=None,
    )
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    @patch("skylock_cli.api.nav_requests.client.get")
    @patch("skylock_cli.api.dir_requests.client.delete")
    def test_remove_directory_change_cwd(
        self,
        mock_delete,
        mock_change_dir,
        mock_context,
        _mock_save_context,
        _mock_is_valid,
        _mock_is_expired,
    ):
        """Test removal when the directory is the current working directory"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.NO_CONTENT)
        mock_change_dir.return_value = mock_response_with_status(HTTPStatus.OK)
        mock_context.return_value = mock_test_context(path=Path("/test/"))

        with patch(
            "skylock_cli.core.dir_operations.change_directory"
        ) as mock_change_directory:
            remove_directory("/test/", True)
            mock_delete.assert_called_once()
            mock_change_directory.assert_called_once_with("/")


class TestMakeDirectoryPublic(unittest.TestCase):
    """Test cases for the make_directory_public function from core.dir_operations"""

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_public_success(self, mock_patch):
        """Test successful directory public access"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.OK)

        make_directory_public("test_dir/")
        mock_patch.assert_called_once()

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_public_unauthorized(self, mock_patch):
        """Test public access when the user is unauthorized"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.UNAUTHORIZED)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_public("test_dir/")
            self.assertIn(
                "User is unauthorized. Please login to use this command.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_public_not_found(self, mock_patch):
        """Test public access when the directory is not found"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_public("/test1/test2/")
            self.assertIn(
                "Directory `/test1/test2` does not exist!\n", mock_stderr.getvalue()
            )

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_public_skylock_api_error(self, mock_patch):
        """Test public access with a SkyLockAPIError"""
        mock_patch.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_public("test_dir/")
            self.assertIn(
                "Failed to make directory public (Error Code: 500)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_public_connection_error(self, mock_patch):
        """Test public access when a ConnectError occurs (backend is offline)"""
        mock_patch.side_effect = ConnectError("Failed to connect to the server")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_public("test_dir/")
            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
                mock_stderr.getvalue(),
            )


class TestMakeDirectoryPrivate(unittest.TestCase):
    """Test cases for the make_directory_private function from core.dir_operations"""

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_private_success(self, mock_patch):
        """Test successful directory private access"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.OK)

        make_directory_private("test_dir/")
        mock_patch.assert_called_once()

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_private_unauthorized(self, mock_patch):
        """Test private access when the user is unauthorized"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.UNAUTHORIZED)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_private("test_dir/")
            self.assertIn(
                "User is unauthorized. Please login to use this command.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_private_not_found(self, mock_patch):
        """Test private access when the directory is not found"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_private("/test1/test2/")
            self.assertIn(
                "Directory `/test1/test2` does not exist!\n", mock_stderr.getvalue()
            )

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_private_skylock_api_error(self, mock_patch):
        """Test private access with a SkyLockAPIError"""
        mock_patch.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_private("test_dir/")
            self.assertIn(
                "Failed to make directory private (Error Code: 500)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.dir_requests.client.patch")
    def test_make_directory_private_connection_error(self, mock_patch):
        """Test private access when a ConnectError occurs (backend is offline)"""
        mock_patch.side_effect = ConnectError("Failed to connect to the server")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_directory_private("test_dir/")
            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
                mock_stderr.getvalue(),
            )


if __name__ == "__main__":
    unittest.main()
