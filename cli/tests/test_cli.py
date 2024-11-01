"""
Tests for the CLI commands.
"""

import unittest
import json
from pathlib import Path
from unittest.mock import patch, Mock
from typer.testing import CliRunner
from art import text2art
from skylock_cli.model.token import Token
from skylock_cli.model.context import Context
from skylock_cli.model.user_dir import UserDir
from skylock_cli.cli import app
from skylock_cli.exceptions import api_exceptions

runner = CliRunner()


class TestRegisterCommand(unittest.TestCase):
    """Test cases for the register command"""

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_success(self, mock_send):
        """Test the register command"""
        mock_send.return_value = None

        result = runner.invoke(
            app, ["register", "testuser1"], input="testpass1\ntestpass1"
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("User registered successfully", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_user_already_exists(self, mock_send):
        """Test the register command when the user already exists"""
        mock_send.side_effect = api_exceptions.UserAlreadyExistsError("testuser")

        result = runner.invoke(
            app, ["register", "testuser"], input="testpass\ntestpass"
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("User with username `testuser` already exists!", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_skylock_api_error(self, mock_send):
        """Test the register command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "An unexpected API error occurred"
        )

        result = runner.invoke(
            app, ["register", "testuser2"], input="testpass2\ntestpass2"
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("An unexpected API error occurred", result.output)

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_connection_error(self, mock_send):
        """Test the register command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(
            app, ["register", "testuser3"], input="testpass3\ntestpass3"
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )

    @patch("skylock_cli.core.auth.send_register_request")
    def test_register_password_mismatch(self, _mock_send):
        """Test the register command when the passwords do not match"""
        result = runner.invoke(
            app, ["register", "testuser4"], input="testpass4\ntestpass5"
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Passwords do not match. Please try again.", result.output)


class TestLoginCommand(unittest.TestCase):
    """Test cases for the login command"""

    @patch("skylock_cli.core.auth.send_login_request")
    @patch("skylock_cli.core.context_manager.ContextManager.ensure_context_file_exists")
    @patch(
        "skylock_cli.core.context_manager.ContextManager.context_file_path",
        Path("/tmp/test_skylock_config/test_skylock_config.json"),
    )
    def test_login_success(self, _mock_ensure_context_file_exists, mock_send):
        """Test the login command"""
        # Create a context file with old token and cwd
        config_dir_path = Path("/tmp/test_skylock_config")
        config_dir_path.mkdir(parents=True, exist_ok=True)
        config_file_path = config_dir_path / "test_skylock_config.json"

        old_token = Token(access_token="old_token", token_type="bearer")
        old_cwd = UserDir(path=Path("/old_cwd"))
        old_context = Context(token=old_token, user_dir=old_cwd)
        with open(config_file_path, "w", encoding="utf-8") as file:
            json.dump({"context": old_context.model_dump()}, file, indent=4)

        new_token = Token(access_token="new_token", token_type="bearer")
        mock_send.return_value = new_token

        result = runner.invoke(app, ["login", "testuser"], input="testpass")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("User logged in successfully", result.output)
        self.assertIn("Hello, testuser", result.output)
        self.assertIn("Welcome to our file hosting service", result.output)
        self.assertIn(text2art("SkyLock"), result.output)
        self.assertIn("Your current working directory is: /old_cwd", result.output)

        with open(config_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            new_context = Context(**data.get("context", {}))
            self.assertEqual(new_context.user_dir.path, Path("/old_cwd"))
            self.assertEqual(new_context.token.access_token, "new_token")

        # Clean up: delete the created file and directory
        config_file_path.unlink()
        config_dir_path.rmdir()

    @patch("skylock_cli.core.auth.send_login_request")
    def test_login_authentication_error(self, mock_send):
        """Test the login command when an AuthenticationError occurs"""
        mock_send.side_effect = api_exceptions.AuthenticationError()

        result = runner.invoke(app, ["login", "testuser"], input="wrongpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid username or password", result.output)

    @patch("skylock_cli.core.auth.send_login_request")
    def test_login_skylock_api_error(self, mock_send):
        """Test the login command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "An unexpected API error occurred"
        )

        result = runner.invoke(app, ["login", "testuser"], input="testpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("An unexpected API error occurred", result.output)

    @patch("skylock_cli.core.auth.send_login_request")
    def test_login_token_not_found_error(self, mock_send):
        """Test the login command when a TokenNotFoundError occurs"""
        mock_send.side_effect = api_exceptions.TokenNotFoundError()

        result = runner.invoke(app, ["login", "testuser"], input="testpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Token not found in the response", result.output)

    @patch("skylock_cli.core.auth.send_login_request")
    def test_login_connection_error(self, mock_send):
        """Test the login command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(app, ["login", "testuser"], input="testpass")
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )


class TestMKDIRCommand(unittest.TestCase):
    """Test cases for the mdkir command"""

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success(self, mock_get_context, mock_send):
        """Test the mkdir command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), False
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success_parent_flag_long(self, mock_get_context, mock_send):
        """Test the mkdir command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        result = runner.invoke(app, ["mkdir", "test_dir", "--parent"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_mkdir_success_parent_flag_short(self, mock_get_context, mock_send):
        """Test the mkdir command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        result = runner.invoke(app, ["mkdir", "test_dir", "-p"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mdkir_token_expired(self, mock_send):
        """Test the mkdir command when the token has expired"""
        mock_send.side_effect = api_exceptions.UserUnauthorizedError()

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_directory_already_exists(self, mock_send):
        """Test the mkdir command when the directory already exists"""
        mock_send.side_effect = api_exceptions.DirectoryAlreadyExistsError("test_dir")

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Directory `test_dir` already exists!", result.output)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_skylock_api_error(self, mock_send):
        """Test the mkdir command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "Failed to create directory (Internal Server Error)"
        )

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to create directory (Internal Server Error)", result.output
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_connection_error(self, mock_send):
        """Test the mkdir command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_invalid_path_error(self, mock_send):
        """Test the mkdir command when an InvalidPathError occurs"""
        mock_send.side_effect = api_exceptions.InvalidPathError("Invalid path")

        result = runner.invoke(app, ["mkdir", "test_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid path `Invalid path`!", result.output)

    @patch("skylock_cli.core.dir_operations.send_mkdir_request")
    def test_mkdir_directory_missing_error(self, mock_send):
        """Test the mkdir command when a DirectoryMissingError occurs"""
        mock_send.side_effect = api_exceptions.DirectoryMissingError("/child_dir")

        result = runner.invoke(app, ["mkdir", "test_dir/child_dir"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Directory `/child_dir` is missing! Use the --parent flag to create parent \ndirectories.\n",
            result.output,
        )


class TestRMDIRCommand(unittest.TestCase):
    """Test cases for the rmdir command"""

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rmdir_success(self, mock_get_context, mock_send):
        """Test the rmdir command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        result = runner.invoke(app, ["rmdir", "test_dir/"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), False
        )

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rmdir_success_recursive_long(self, mock_get_context, mock_send):
        """Test the rmdir command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        result = runner.invoke(app, ["rmdir", "test_dir/", "--recursive"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )

    @patch("skylock_cli.core.dir_operations.send_rmdir_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_rmdir_success_recursive_short(self, mock_get_context, mock_send):
        """Test the rmdir command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        result = runner.invoke(app, ["rmdir", "test_dir/", "-r"])
        self.assertEqual(result.exit_code, 0)
        mock_send.assert_called_once_with(
            mock_get_context.return_value.token, Path("/test_dir"), True
        )

    def test_rmdir_not_a_directory_error(self):
        """Test the rmdir command when the path is not a directory"""
        result = runner.invoke(app, ["rmdir", "/test_file"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("/test_file is not a directory", result.output)

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
        self.assertIn(
            "Directory `/test_dir` is not empty! Use the --recursive flag to delete it \nrecursively.\n",
            result.output,
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
        """Test the rmdir command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(app, ["rmdir", "/test_dir/"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )


class TestLSCommand(unittest.TestCase):
    """Test cases for the ls command"""

    @patch("skylock_cli.core.nav.send_ls_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_ls_success(self, mock_get_context, mock_send):
        """Test the ls command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

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
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

        mock_send.return_value = {"files": [], "folders": []}

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("No contents in directory", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    @patch("skylock_cli.core.context_manager.ContextManager.get_context")
    def test_ls_success_only_files(self, mock_get_context, mock_send):
        """Test the ls command"""
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

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
        mock_get_context.return_value = Mock(
            token=Token(access_token="test_token", token_type="bearer"),
            user_dir=Mock(path=Path("/")),
        )

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
        self.assertIn(
            "User is unauthorized. Please login to use this command.", result.output
        )

    @patch("skylock_cli.core.nav.send_ls_request")
    def test_ls_skylock_api_error(self, mock_send):
        """Test the ls command when a SkyLockAPIError occurs"""
        mock_send.side_effect = api_exceptions.SkyLockAPIError(
            "An unexpected API error occurred"
        )

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("An unexpected API error occurred", result.output)

    @patch("skylock_cli.core.nav.send_ls_request")
    def test_ls_connection_error(self, mock_send):
        """Test the ls command when a ConnectionError occurs (backend is offline)"""
        mock_send.side_effect = ConnectionError(
            "Failed to connect to the server. Please check your network connection."
        )

        result = runner.invoke(app, ["ls"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn(
            "Failed to connect to the server. Please check your network \nconnection.",
            result.output,
        )

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
