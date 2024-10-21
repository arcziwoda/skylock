"""
This module contains commands the user can run to interact with the SkyLock
"""

import typer
from skylock_cli.commands.auth.register import register_user

app = typer.Typer()


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


@app.command()
def register(user_login: str, user_password: str):
    """
    Register a new user
    """
    typer.echo(f"Registering new user with login: {user_login}")
    register_user(user_login, user_password)


if __name__ == "__main__":
    app()
