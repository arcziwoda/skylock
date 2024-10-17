"""
This module contains a simple CLI application using Typer.
"""

import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    """Say hello to NAME."""
    print(f"Hello {name}!")


@app.command()
def goodbye(name: str):
    """Say goodbye to NAME."""
    print(f"Goodbye {name}!")


if __name__ == "__main__":
    app()
