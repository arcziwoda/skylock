"""
Test cases for the functions from core.file_operations
"""

import tempfile
import unittest
import os
from http import HTTPStatus
from io import StringIO
from unittest.mock import patch, mock_open, Mock
from pathlib import Path
from click import exceptions
from httpx import ConnectError
from skylock_cli.core.file_operations import (
    _generate_unique_file_path,
    upload_file,
    download_file,
    remove_file,
    make_file_public,
    make_file_private,
)
from tests.helpers import mock_test_context, mock_response_with_status


class TestGenerateUniqueFilePath(unittest.TestCase):
    """
    Test cases for the _generate_unique_file_path function
    """

    @patch("skylock_cli.core.file_operations.tempfile.NamedTemporaryFile")
    def test_generate_unique_file_path(self, mock_tempfile):
        """
        Test the _generate_unique_file_path function
        """
        mock_tempfile.return_value.__enter__.return_value.name = "/mocked/path/file.txt"
        directory = Path("/mocked/path")
        file_name = "file.txt"

        result = _generate_unique_file_path(directory, file_name)

        self.assertEqual(result, Path("/mocked/path/file.txt"))
        mock_tempfile.assert_called_once_with(
            dir=directory, prefix="file", suffix=".txt", delete=False
        )

    @patch("skylock_cli.core.file_operations.tempfile.NamedTemporaryFile")
    def test_generate_unique_file_path_with_different_extension(self, mock_tempfile):
        """
        Test the _generate_unique_file_path function with a different file extension
        """
        mock_tempfile.return_value.__enter__.return_value.name = "/mocked/path/file.pdf"
        directory = Path("/mocked/path")
        file_name = "file.pdf"

        result = _generate_unique_file_path(directory, file_name)

        self.assertEqual(result, Path("/mocked/path/file.pdf"))
        mock_tempfile.assert_called_once_with(
            dir=directory, prefix="file", suffix=".pdf", delete=False
        )

    @patch("skylock_cli.core.file_operations.tempfile.NamedTemporaryFile")
    def test_generate_unique_file_path_with_no_extension(self, mock_tempfile):
        """
        Test the _generate_unique_file_path function with no file extension
        """
        mock_tempfile.return_value.__enter__.return_value.name = "/mocked/path/file"
        directory = Path("/mocked/path")
        file_name = "file"

        result = _generate_unique_file_path(directory, file_name)

        self.assertEqual(result, Path("/mocked/path/file"))
        mock_tempfile.assert_called_once_with(
            dir=directory, prefix="file", suffix="", delete=False
        )


class TestUploadFile(unittest.TestCase):
    """
    Test cases for the upload_file function
    """

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch("skylock_cli.core.file_operations.send_upload_request", return_value=None)
    def test_upload_file_success(self, _mock_send, _mock_get_context):
        """Test the upload_file function with a successful upload"""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file_name = temp_file_path.name
            result = upload_file(temp_file_path, Path("."))

            self.assertEqual(result, Path(f"/{temp_file_name}"))

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(Path("/test")),
    )
    @patch("skylock_cli.core.file_operations.send_upload_request", return_value=None)
    def test_upload_file_with_different_cwd(self, _mock_send, _mock_get_context):
        """Test the upload_file function with a different current working directory"""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file_name = temp_file_path.name
            result = upload_file(temp_file_path, Path("."))

            self.assertEqual(result, Path(f"/test/{temp_file_name}"))

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch("skylock_cli.core.file_operations.send_upload_request", side_effect=None)
    def test_upload_file_with_other_than_cwd_destination_path(
        self, _mock_send, _mock_get_context
    ):
        """Test the upload_file function with a destination path other than the current working directory"""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file_name = temp_file_path.name
            result = upload_file(temp_file_path, Path("/test"))

            self.assertEqual(result, Path(f"/test/{temp_file_name}"))

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.api.file_requests.client.post",
        return_value=mock_response_with_status(HTTPStatus.UNAUTHORIZED),
    )
    def test_upload_file_with_unauthorized_error(self, _mock_send, _mock_get_context):
        """Test the upload_file function with an unauthorized error"""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with self.assertRaises(exceptions.Exit):
                    upload_file(temp_file_path, Path("."))

                self.assertIn(
                    "User is unauthorized. Please login to use this command.",
                    mock_stderr.getvalue(),
                )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.api.file_requests.client.post",
        return_value=mock_response_with_status(HTTPStatus.CONFLICT),
    )
    def test_upload_file_already_exists(self, _mock_send, _mock_get_context):
        """Test the upload_file function with an unauthorized error"""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file_name = os.path.basename(temp_file_path)
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with self.assertRaises(exceptions.Exit):
                    upload_file(temp_file_path, Path("."))

                self.assertIn(
                    f"File `/{temp_file_name}` already exists!", mock_stderr.getvalue()
                )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.api.file_requests.client.post",
        return_value=mock_response_with_status(HTTPStatus.BAD_REQUEST),
    )
    def test_upload_file_dest_path_does_not_exists(self, _mock_send, _mock_get_context):
        """Test the upload_file function with an unauthorized error"""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file_name = os.path.basename(temp_file_path)
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with self.assertRaises(exceptions.Exit):
                    upload_file(temp_file_path, Path("."))

                self.assertIn(
                    f"Invalid path `/{temp_file_name}`!", mock_stderr.getvalue()
                )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.api.file_requests.client.post",
        return_value=mock_response_with_status(HTTPStatus.INTERNAL_SERVER_ERROR),
    )
    def test_upload_file_with_internal_server_error(
        self, _mock_send, _mock_get_context
    ):
        """Test the upload_file function with an unauthorized error"""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with self.assertRaises(exceptions.Exit):
                    upload_file(temp_file_path, Path("."))

                self.assertIn(
                    "Failed to upload file (Error Code: 500)", mock_stderr.getvalue()
                )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch("skylock_cli.api.file_requests.client.post")
    def test_upload_file_with_connection_error(self, mock_send, _mock_get_context):
        """Test the upload_file function with a connection error"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with self.assertRaises(exceptions.Exit):
                    upload_file(temp_file_path, Path("."))

                self.assertIn(
                    "The server is not reachable at the moment. Please try again later.",
                    mock_stderr.getvalue(),
                )


class TestDownloadFile(unittest.TestCase):
    """
    Test cases for the download_file function
    """

    @patch("skylock_cli.core.file_operations.create_downloads_dir", return_value=None)
    @patch(
        "skylock_cli.core.file_operations._generate_unique_file_path",
        return_value=Path("/mocked/Downloads/file.txt"),
    )
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.core.file_operations.send_download_request",
        return_value=b"123\nabc",
    )
    @patch("skylock_cli.core.file_operations.Path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_download_file_target_path_exists(
        self,
        _mock_open,
        _mock_exists,
        _mock_send,
        _mock_get_context,
        _mock_generate_unique,
        _mock_create_downloads_dir,
    ):
        """Test the download_file function with a successful download"""
        result = download_file(Path("file.txt"))
        self.assertEqual(result, Path("/mocked/Downloads/file.txt"))
        _mock_open.assert_called_once_with(Path("/mocked/Downloads/file.txt"), "wb")
        _mock_open().write.assert_called_once_with(b"123\nabc")

    @patch(
        "skylock_cli.core.file_operations.DOWNLOADS_DIR", new=Path("/mocked/Downloads/")
    )
    @patch("skylock_cli.core.file_operations.create_downloads_dir", return_value=None)
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.core.file_operations.send_download_request",
        return_value=b"123\nabc",
    )
    @patch("skylock_cli.core.file_operations.Path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    def test_download_file_target_path_does_not_exist(
        self,
        _mock_open,
        _mock_exists,
        _mock_send,
        _mock_get_context,
        _mock_create_downloads_dir,
    ):
        """Test the download_file function when target_file_path does not exists"""
        result = download_file(Path("file.txt"))
        self.assertEqual(result, Path("/mocked/Downloads/file.txt"))
        self.assertEqual(result.parent, Path("/mocked/Downloads"))
        _mock_open.assert_called_once_with(Path("/mocked/Downloads/file.txt"), "wb")
        _mock_open().write.assert_called_once_with(b"123\nabc")

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.api.file_requests.client.get",
        return_value=mock_response_with_status(HTTPStatus.UNAUTHORIZED),
    )
    def test_download_file_with_unauthorized_error(self, _mock_send, _mock_get_context):
        """Test the download_file function with an unauthorized error"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                download_file(Path("file.txt"))

            self.assertIn(
                "User is unauthorized. Please login to use this command.",
                mock_stderr.getvalue(),
            )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch(
        "skylock_cli.api.file_requests.client.get",
        return_value=mock_response_with_status(HTTPStatus.BAD_REQUEST),
    )
    def test_download_file_with_invalid_path_error(self, _mock_send, _mock_get_context):
        """Test the download_file function with an invalid path error"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                download_file(Path("/$/file.txt"))

            self.assertIn(
                "Invalid path `/$/file.txt`!",
                mock_stderr.getvalue(),
            )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(Path("/test")),
    )
    @patch(
        "skylock_cli.api.file_requests.client.get",
        return_value=mock_response_with_status(HTTPStatus.NOT_FOUND),
    )
    def test_download_file_with_not_found_error(self, _mock_send, _mock_get_context):
        """Test the download_file function with a not found error"""
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                download_file(Path("non_existent_file.txt"))

            self.assertIn(
                "File `/test/non_existent_file.txt` does not exist!",
                mock_stderr.getvalue(),
            )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch("skylock_cli.api.file_requests.client.get")
    def test_download_file_with_invalid_response_format_error(
        self, mock_send, _mock_get_context
    ):
        """Test the download_file function with an invalid response format error"""
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.content = None
        mock_send.return_value = mock_response

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                download_file(Path("file.txt"))

            self.assertIn(
                "Invalid response format!",
                mock_stderr.getvalue(),
            )

    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch("skylock_cli.api.file_requests.client.get")
    def test_download_file_with_connection_error(self, mock_send, _mock_get_context):
        """Test the download function with a connection error"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                download_file(Path("file.txt"))

            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
                mock_stderr.getvalue(),
            )


class TestRemoveFile(unittest.TestCase):
    """Test cases for the remove_file function from core.file_operations"""

    @patch("skylock_cli.api.file_requests.client.delete")
    def test_remove_file_success(self, mock_delete):
        """Test successful file removal"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.NO_CONTENT)

        remove_file("test.txt")
        mock_delete.assert_called_once()

    @patch("skylock_cli.api.file_requests.client.delete")
    def test_remove_file_not_found(self, mock_delete):
        """Test removal when the file is not found"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_file("test.txt")
            self.assertIn("File `/test.txt` does not exist!", mock_stderr.getvalue())

    @patch("skylock_cli.api.file_requests.client.delete")
    def test_remove_file_skylock_api_error(self, mock_delete):
        """Test removal with a SkyLockAPIError"""
        mock_delete.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_file("test.txt")
            self.assertIn(
                "Failed to remove file (Error Code: 500)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.file_requests.client.delete")
    def test_remove_file_connection_error(self, mock_delete):
        """Test removal when a ConnectError occurs (backend is offline)"""
        mock_delete.side_effect = ConnectError("Failed to connect to the server")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_file("test.txt")
            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
                mock_stderr.getvalue(),
            )

    def test_remove_not_a_file_error(self):
        """Test removal when the path is not a file"""

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_file("test_dir/")
            self.assertIn("test_dir/ is not a file", mock_stderr.getvalue())

    @patch("skylock_cli.api.file_requests.client.delete")
    def test_remove_file_unauthorized(self, mock_delete):
        """Test removal when the user is unauthorized"""
        mock_delete.return_value = mock_response_with_status(HTTPStatus.UNAUTHORIZED)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                remove_file("test.txt")
            self.assertIn(
                "User is unauthorized. Please login to use this command.",
                mock_stderr.getvalue(),
            )


class TestMakeFilePublic(unittest.TestCase):
    """Test cases for the make_file_public function from core.file_operations"""

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_public_success(self, mock_patch):
        """Test successful file public access"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.OK)

        make_file_public("test.txt")
        mock_patch.assert_called_once()

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_public_not_found(self, mock_patch):
        """Test making a file public when the file is not found"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_file_public("test.txt")
            self.assertIn("File `/test.txt` does not exist!", mock_stderr.getvalue())

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_public_skylock_api_error(self, mock_patch):
        """Test making a file public with a SkyLockAPIError"""
        mock_patch.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_file_public("test.txt")
            self.assertIn(
                "Failed to make file public (Error Code: 500)",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_public_connection_error(self, mock_patch):
        """Test making a file public when a ConnectError occurs (backend is offline)"""
        mock_patch.side_effect = ConnectError("Failed to connect to the server")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_file_public("test.txt")
            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
                mock_stderr.getvalue(),
            )


class TestMakeFilePrivate(unittest.TestCase):
    """Test cases for the make_file_private function from core.file_operations"""

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_private_success(self, mock_patch):
        """Test successful file private access"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.OK)

        make_file_private("test.txt")
        mock_patch.assert_called_once()

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_private_not_found(self, mock_patch):
        """Test making a file private when the file is not found"""
        mock_patch.return_value = mock_response_with_status(HTTPStatus.NOT_FOUND)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_file_private("test.txt")
            self.assertIn("File `/test.txt` does not exist!", mock_stderr.getvalue())

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_private_connection_error(self, mock_patch):
        """Test making a file private when a ConnectError occurs (backend is offline)"""
        mock_patch.side_effect = ConnectError("Failed to connect to the server")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_file_private("test.txt")
            self.assertIn(
                "The server is not reachable at the moment. Please try again later.",
                mock_stderr.getvalue(),
            )

    @patch("skylock_cli.api.file_requests.client.patch")
    def test_make_file_private_skylock_api_error(self, mock_patch):
        """Test making a file private with a SkyLockAPIError"""
        mock_patch.return_value = mock_response_with_status(
            HTTPStatus.INTERNAL_SERVER_ERROR
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            with self.assertRaises(exceptions.Exit):
                make_file_private("test.txt")
            self.assertIn(
                "Failed to make file private (Error Code: 500)",
                mock_stderr.getvalue(),
            )


if __name__ == "__main__":
    unittest.main()
