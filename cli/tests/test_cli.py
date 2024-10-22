"""
Tests for the main app.py module.
"""

from unittest.mock import patch
from typer.testing import CliRunner
from skylock_cli.cli import app
from skylock_cli.api.http_exceptions import UserAlreadyExistsError


runner = CliRunner()


def test_login():
    """Test the login command"""
    result = runner.invoke(app, ["login"])
    assert result.exit_code == 2


def test_logout():
    """Test the logout command"""
    result = runner.invoke(app, ["logout"])
    assert result.exit_code == 0
    assert "Logout of the SkyLock" in result.output


def test_register_success():
    """Test the register command"""
    with patch("skylock_cli.commands.auth.send_register_request") as mock_send:
        mock_send.return_value = None

        result = runner.invoke(app, ["register", "testuser1", "testpass1"])

        assert result.exit_code == 0
        assert "User registered successfully" in result.output


def test_register_user_already_exists():
    """Test the register command when the user already exists"""
    with patch("skylock_cli.commands.auth.send_register_request") as mock_send:
        mock_send.side_effect = UserAlreadyExistsError(
            "User with username already exists",
            status_code=409,
            detail="User with username testuser already exists",
        )

        result = runner.invoke(app, ["register", "testuser", "testpass"])
        assert result.exit_code == 1
        assert (
            "UserAlreadyExistsError occurred: User with username testuser already exists (409)"
            in result.output
        )
