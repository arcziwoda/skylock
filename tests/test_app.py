from typer.testing import CliRunner
from cli_client.app import app

runner = CliRunner()

def test_hello():
    result = runner.invoke(app, ["hello", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice!" in result.output

def test_goodbye():
    result = runner.invoke(app, ["goodbye", "Alice"])
    assert result.exit_code == 0
    assert "Goodbye Alice!" in result.output