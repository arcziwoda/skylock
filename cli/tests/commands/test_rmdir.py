"""
Tests for the rmdir command
"""

import re
import unittest
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from httpx import ConnectError
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions
from tests.helpers import assert_connect_error, mock_test_context

runner = CliRunner()


class TestRMDIRCommand(unittest.TestCase):
    """Test cases for the rmdir command"""

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rmdir_success(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the rmdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["rmdir", "test_dir/"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), False
        )
        self.assertIn("Directory /test_dir removed successfully", result.output)
        self.assertIn("Current working directory: /", result.output)

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch(
        "skylock_cli.core.context_manager.ContextManager.save_context",
        return_value=None,
    )
    @patch("skylock_cli.core.nav.send_cd_request")
    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rmdir_success_chnage_dir(
        self,
        mock_get_context,
        mock_send_rmdir,
        mock_send_cd,
        _mock_save_context,
        _mock_is_valid,
        _mock_is_expired,
    ):
        """Test the rmdir command"""
        mock_get_context.return_value = mock_test_context(path=Path("/test_dir"))
        mock_send_cd.return_value = None

        result = runner.invoke(app, ["rmdir", "/test_dir/"])
        self.assertEqual(result.exit_code, 0)
        mock_send_rmdir.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), False
        )
        self.assertIn("Current working directory: /", result.output)
        self.assertIn("Directory /test_dir removed successfully", result.output)

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rmdir_success_recursive_long(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the rmdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["rmdir", "test_dir/", "--recursive"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )
        self.assertIn("Directory /test_dir removed successfully", result.output)
        self.assertIn("Current working directory: /", result.output)

    @patch("skylock_cli.model.token.Token.is_expired", return_value=False)
    @patch("skylock_cli.model.token.Token.is_valid", return_value=True)
    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rmdir_success_recursive_short(
        self, mock_get_context, mock_send, _mock_is_valid, _mock_is_expired
    ):
        """Test the rmdir command"""
        mock_get_context.return_value = mock_test_context()

        result = runner.invoke(app, ["rmdir", "test_dir/", "-r"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )
        self.assertIn("Directory /test_dir removed successfully", result.output)
        self.assertIn("Current working directory: /", result.output)

    def test_rmdir_not_a_directory_error(self):
        """Test the rmdir command when the path is not a directory"""
        result = runner.invoke(app, ["rmdir", "/test_file"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("/test_file is not a directory", result.output)

    def test_rmdir_root_dir(self):
        """Test the rmdir command when the path is the root directory"""
        result = runner.invoke(app, ["rmdir", "/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Cannot delete the root directory", result.output)

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    def test_rmdir_token_expired(self, mock_send):
        """Test the rmdir command when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = runner.invoke(app, ["rmdir", "test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    def test_rmdir_directory_not_found_error(self, mock_send):
        """Test the rmdir command when a DirectoryNotFoundError occurs"""
        mock_send.side_effect = api_exceptions.DirectoryNotFoundError("/test1/test2/")

        result = runner.invoke(app, ["rmdir", "/test1/test2/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `/test1/test2/` does not exist!", result.output)

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    def test_rmdir_directory_not_empty_error(self, mock_send):
        """Test the rmdir command when a DirectoryNotEmptyError occurs"""
        mock_send.side_effect = api_exceptions.DirectoryNotEmptyError("/test_dir")

        result = runner.invoke(app, ["rmdir", "/test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertRegex(
            result.output,
            re.compile(
                r"Directory `/test_dir` is not empty! Use the --recursive flag to delete it\s+recursively\.\n",
                re.MULTILINE,
            ),
        )

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    def test_rmdir_skylock_api_error(self, mock_send):
        """Test the rmdir command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to delete directory (Internal Server Error)"
        )

        result = runner.invoke(app, ["rmdir", "/test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to delete directory (Internal Server Error)", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    def test_rmdir_connection_error(self, mock_send):
        """Test the rmdir command when a ConnectError occurs (backend is offline)"""
        mock_send.side_effect = ConnectError("Failed to connect to the server")
        result = runner.invoke(app, ["rmdir", "/test_dir/"])
        assert_connect_error(result)


if __name__ == "__main__":
    unittest.main()
