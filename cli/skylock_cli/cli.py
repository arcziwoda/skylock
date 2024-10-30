"""
This module contains commands the user can run to interact with the SkyLock.
"""

import typer
from art import text2art
from skylock_cli.core.auth import register_user, login_user
from skylock_cli.core.dir_operations import create_directory

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
    context = login_user(username, password)

    typer.secho("User logged in successfully", fg=typer.colors.GREEN)
    typer.secho("Hello, " + username, fg=typer.colors.GREEN)
    typer.secho("Welcome to our file hosting service", fg=typer.colors.BLUE, bold=True)
    typer.secho(text2art("SkyLock"), fg=typer.colors.BLUE)
    typer.secho(
        f"Your current working directory is: {str(context.user_dir)}",
        fg=typer.colors.BLUE,
    )


@app.command()
def mkdir(directory_name: str) -> None:
    """
    Create a new directory in the SkyLock.

    Args:
        directory (str): The name of the new directory.

    Returns:
        None
    """
    dir_path = create_directory(directory_name)
    typer.secho(
        f"Directory {str(dir_path)} created successfully", fg=typer.colors.GREEN
    )


if __name__ == "__main__":
    app()
