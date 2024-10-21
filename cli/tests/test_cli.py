"""
Tests for the main app.py module.
"""

from unittest.mock import patch, Mock
import httpx
from typer.testing import CliRunner
from skylock_cli.cli import app


runner = CliRunner()


def test_login():
    """Test the login command"""
    result = runner.invoke(app, ["login"])
    assert result.exit_code == 0
    assert "Login to the SkyLock" in result.output


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
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Conflict",
            request=None,
            response=Mock(status_code=409, json=lambda: {"detail": "HTTP error code 409 occurred: User with username testuser already exists"}),
        )
        mock_send.side_effect = mock_response.raise_for_status

        result = runner.invoke(app, ["register", "testuser", "testpass"])
        assert result.exit_code == 1
        assert "HTTP error code 409 occurred: User with username testuser already exists" in result.output
