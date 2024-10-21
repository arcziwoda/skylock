"""
Tests for the main app.py module.
"""

from unittest import mock
from typer.testing import CliRunner
from skylock_cli.app import app

runner = CliRunner()


def test_hello():
    """Test the hello command with a mocked name."""
    with mock.patch("skylock_cli.app.get_name", return_value="MockName"):
        result = runner.invoke(app, ["hello"])
        assert result.exit_code == 0
        assert "Hello MockName!" in result.output


def test_hello_uppercase():
    """Test the hello command with the uppercase option."""
    result = runner.invoke(app, ["hello", "Alice", "--uppercase"])
    assert result.exit_code == 0
    assert "Hello ALICE!" in result.output


def test_hello_with_name():
    """Test the hello command with a provided name."""
    result = runner.invoke(app, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice!" in result.output


def test_hello_root():
    """Test the hello command with 'root' as the name."""
    result = runner.invoke(app, ["hello", "root"])
    assert result.exit_code == 1
    assert "Cannot use 'root' as name!" in result.output


def test_goodbye():
    """Test the goodbye command."""
    result = runner.invoke(app, ["goodbye", "Alice"])
    assert result.exit_code == 0
    assert "Goodbye Alice!" in result.output
