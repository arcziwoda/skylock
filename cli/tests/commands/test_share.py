"""
Tests for the share command
"""

import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from httpx import ConnectError
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import mock_test_context, assert_connect_error


class TestShareCommand(unittest.TestCase):
    """Test cases for the share command"""

    def setUp(self):
        self.runner = CliRunner()

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch("skylock_cli.core.dir_operations.dir_requests.send_share_request")
    def test_share_directory_success(
        self,
        mock_send_share_request,
        _mock_get_context,
        _mock_is_valid,
        _mock_is_expired,
    ):
        """Test the share command on directory"""
        mock_send_share_request.return_value = {"location": "/folders/349248263498632"}
        result = self.runner.invoke(app, ["share", "test_dir/"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.stdout)
        self.assertIn(
            "URL to shared resource: http://localhost:8000/folders/349248263498632",
            result.stdout,
        )

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(),
    )
    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_success(
        self,
        mock_send_share_request,
        _mock_get_context,
        _mock_is_valid,
        _mock_is_expired,
    ):
        """Test the share command on file"""
        mock_send_share_request.return_value = {"location": "/files/349248263498632"}
        result = self.runner.invoke(app, ["share", "file.txt"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.stdout)
        self.assertIn(
            "URL to shared resource: http://localhost:8000/files/349248263498632",
            result.stdout,
        )

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch(
        "skylock_cli.core.context_manager.ContextManager.get_context",
        return_value=mock_test_context(base_url="https://skylock.com"),
    )
    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_success_other_base_url(
        self,
        mock_send_share_request,
        _mock_get_context,
        _mock_is_valid,
        _mock_is_expired,
    ):
        """Test the share command on file with a different base URL"""
        mock_send_share_request.return_value = {"location": "/files/349248263498632"}
        result = self.runner.invoke(app, ["share", "file.txt"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current working directory: /", result.stdout)
        self.assertIn(
            "URL to shared resource: https://skylock.com/files/349248263498632",
            result.stdout,
        )

    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_unathorized(
        self,
        mock_send_share_request,
    ):
        """Test the share command on file with an unauthorized user"""
        mock_send_share_request.side_effect = api_exceptions.UserUnauthorizedError()

        result = self.runner.invoke(app, ["share", "file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.dir_operations.dir_requests.send_share_request")
    def test_share_directory_unathorized(
        self,
        mock_send_share_request,
    ):
        """Test the share command on directory with an unauthorized user"""
        mock_send_share_request.side_effect = api_exceptions.UserUnauthorizedError()

        result = self.runner.invoke(app, ["share", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_not_found_error(
        self,
        mock_send_share_request,
    ):
        """Test the share command on file with a FileNotFoundError"""
        mock_send_share_request.side_effect = api_exceptions.FileNotFoundError(
            "file.txt"
        )

        result = self.runner.invoke(app, ["share", "file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("File `file.txt` does not exist!", result.output)

    @patch("skylock_cli.core.dir_operations.dir_requests.send_share_request")
    def test_share_directory_not_found_error(
        self,
        mock_send_share_request,
    ):
        """Test the share command on directory with a DirectoryNotFoundError"""
        mock_send_share_request.side_effect = api_exceptions.DirectoryNotFoundError(
            "test_dir/"
        )

        result = self.runner.invoke(app, ["share", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `test_dir/` does not exist!", result.output)

    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_not_public(
        self,
        mock_send_share_request,
    ):
        """Test the share command on file that is not public"""
        mock_send_share_request.side_effect = api_exceptions.FileNotPublicError(
            "file.txt"
        )

        result = self.runner.invoke(app, ["share", "file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("File `file.txt` is not public!", result.output)

    @patch("skylock_cli.core.dir_operations.dir_requests.send_share_request")
    def test_share_directory_not_public(
        self,
        mock_send_share_request,
    ):
        """Test the share command on directory that is not public"""
        mock_send_share_request.side_effect = api_exceptions.DirectoryNotPublicError(
            "test_dir/"
        )

        result = self.runner.invoke(app, ["share", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `test_dir/` is not public!", result.output)

    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_wrong_reponse_format(
        self,
        mock_send_share_request,
    ):
        """Test the share command on file with a wrong response format"""
        mock_send_share_request.side_effect = (
            api_exceptions.InvalidResponseFormatError()
        )

        result = self.runner.invoke(app, ["share", "file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid response format!", result.output)

    @patch("skylock_cli.core.dir_operations.dir_requests.send_share_request")
    def test_share_directory_wrong_reponse_format(
        self,
        mock_send_share_request,
    ):
        """Test the share command on directory with a wrong response format"""
        mock_send_share_request.side_effect = (
            api_exceptions.InvalidResponseFormatError()
        )

        result = self.runner.invoke(app, ["share", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid response format!", result.output)

    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_internal_server_error(
        self,
        mock_send_share_request,
    ):
        """Test the share command on file with an InternalServerError"""
        mock_send_share_request.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to share file (Internal Server Error)"
        )

        result = self.runner.invoke(app, ["share", "file.txt"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Failed to share file (Internal Server Error)", result.output)

    @patch("skylock_cli.core.dir_operations.dir_requests.send_share_request")
    def test_share_directory_internal_server_error(
        self,
        mock_send_share_request,
    ):
        """Test the share command on directory with an InternalServerError"""
        mock_send_share_request.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to share directory (Internal Server Error)"
        )

        result = self.runner.invoke(app, ["share", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to share directory (Internal Server Error)", result.output
        )

    @patch("skylock_cli.core.file_operations.file_requests.send_share_request")
    def test_share_file_connection_error(
        self,
        mock_send_share_request,
    ):
        """Test the share command on file with a ConnectionError"""
        mock_send_share_request.side_effect = ConnectError(
            "Failed to connect to the server"
        )
        result = self.runner.invoke(app, ["share", "file.txt"])
        assert_connect_error(result)

    @patch("skylock_cli.core.dir_operations.dir_requests.send_share_request")
    def test_share_directory_connection_error(
        self,
        mock_send_share_request,
    ):
        """Test the share command on directory with a ConnectionError"""
        mock_send_share_request.side_effect = ConnectError(
            "Failed to connect to the server"
        )
        result = self.runner.invoke(app, ["share", "test_dir/"])
        assert_connect_error(result)


if __name__ == "__main__":
    unittest.main()
