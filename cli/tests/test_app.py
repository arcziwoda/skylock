"""
Tests for the main app.py module.
"""

from typer.testing import CliRunner
from skylock_cli.app import app

runner = CliRunner()


def test_login():
    result = runner.invoke(app, ["login"])
    assert result.exit_code == 0
    assert "Login to the SkyLock" in result.output


def test_logout():
    result = runner.invoke(app, ["logout"])
    assert result.exit_code == 0
    assert "Logout of the SkyLock" in result.output


def test_register():
    result = runner.invoke(app, ["register", "user", "pass"])
    assert result.exit_code == 0
    assert "Registering new user with login: user" in result.output
