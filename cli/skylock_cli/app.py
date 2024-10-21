"""
This module contains commands the user can run to interact with the SkyLock 
"""

from typing import Optional
import random
import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer()
console = Console()


def get_name() -> str:
    """
    Get a random name.

    Returns:
        str: A randomly chosen name from a predefined list.
    """
    return random.choice(["Deadpool", "Rick", "Morty", "Hiro"])


@app.command()
def hello(
    name: Optional[str] = typer.Argument(None, help="Name of the person to greet"),
    uppercase: bool = typer.Option(False, help="Convert the name to uppercase"),
) -> None:
    """
    Say hello to NAME.

    If NAME is not provided, a random name will be used. If the name is 'root', an error will be raised.

    Args:
        name (Optional[str]): Name of the person to greet. Defaults to None.
        uppercase (bool): Convert the name to uppercase. Defaults to False.

    Raises:
        typer.Abort: If the name is 'root'.
    """
    if not name:
        name = get_name()
    if name == "root":
        typer.secho("Cannot use 'root' as name!", fg=typer.colors.RED)
        raise typer.Abort()
    if uppercase:
        name = name.upper()
    print(f"Hello {name}!")


@app.command()
def goodbye(name: str) -> None:
    """
    Say goodbye to NAME.

    Args:
        name (str): Name of the person to say goodbye to.
    """
    print(f"Goodbye {name}!")


@app.command()
def show_table() -> None:
    """
    Show a sample table using Rich.

    This command demonstrates how to create a simple table using Rich.
    """
    table = Table(title="Sample Table")

    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Age", style="magenta")
    table.add_column("City", style="green")

    table.add_row("John Doe", "30", "New York")
    table.add_row("Jane Smith", "25", "Los Angeles")
    table.add_row("Sam Brown", "22", "Chicago")

    console.print(table)


if __name__ == "__main__":
    app()
