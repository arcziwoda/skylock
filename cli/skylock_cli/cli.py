"""
This module contains commands the user can run to interact with the SkyLock
"""

import typer
from skylock_cli.commands.auth import register_user

app = typer.Typer()


@app.command()
def register(username: str, password: str):
    """
    Register a new user
    """
    register_user(username, password)
    typer.secho("User registered successfully", fg=typer.colors.GREEN)


@app.command()
def login():
    """
    Login to the SkyLock
    """
    typer.echo("Login to the SkyLock")


@app.command()
def logout():
    """
    Logout of the SkyLock
    """
    typer.echo("Logout of the SkyLock")


if __name__ == "__main__":
    app()
