"""
This module contains commands the user can run to interact with the SkyLock.
"""

import typer
from art import text2art
from skylock_cli.core.auth import register_user, login_user

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def register(username: str) -> None:
    """
    Register a new user in the SkyLock.

    Args:
        username (str): The username of the new user.

    Returns:
        None
    """
    password = typer.prompt("Password", hide_input=True)
    confirm_password = typer.prompt("Confirm password", hide_input=True)
    if password != confirm_password:
        typer.secho("Passwords do not match. Please try again.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    register_user(username, password)
    typer.secho("User registered successfully", fg=typer.colors.GREEN)


@app.command()
def login(username: str) -> None:
    """
    Login to the SkyLock.

    Args:
        username (str): The username of the user.

    Returns:
        None
    """
    password = typer.prompt("Password", hide_input=True)
    login_user(username, password)
    typer.secho("User logged in successfully", fg=typer.colors.GREEN)
    typer.secho("Hello, " + username, fg=typer.colors.GREEN)
    typer.secho("Welcome to our file hosting service", fg=typer.colors.BLUE, bold=True)
    ascii_art = text2art("SkyLock")
    typer.secho(ascii_art, fg=typer.colors.BLUE)


if __name__ == "__main__":
    app()
