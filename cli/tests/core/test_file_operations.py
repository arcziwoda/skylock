"""
Test cases for the functions from core.file_operations
"""

import tempfile
import unittest
import os
from http import HTTPStatus
from io import StringIO
from unittest.mock import patch
from pathlib import Path
from click import exceptions
from skylock_cli.core.file_operations import _generate_unique_file_path, upload_file
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
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file_path = Path(temp_file.name)
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with self.assertRaises(exceptions.Exit):
                    upload_file(temp_file_path, Path("."))

                self.assertIn(
                    "ConnectionError: Failed to connect to the server. Please check your network \nconnection.",
                    mock_stderr.getvalue(),
                )


if __name__ == "__main__":
    unittest.main()
