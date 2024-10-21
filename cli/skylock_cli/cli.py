"""
This module contains commands the user can run to interact with the SkyLock
"""

import typer
from skylock_cli.commands.auth import login_user, register_user

app = typer.Typer()


@app.command()
def register(username: str, password: str):
    """
    Register a new user
    """
    register_user(username, password)
    typer.secho("User registered successfully", fg=typer.colors.GREEN)


@app.command()
def login(username: str, password: str):
    """
    Login to the SkyLock
    """
    token = login_user(username, password)
    typer.secho(f"Token received: {token.access_token}", fg=typer.colors.GREEN)


@app.command()
def logout():
    """
    Logout of the SkyLock
    """
    typer.echo("Logout of the SkyLock")


if __name__ == "__main__":
    app()
