"""
Module to handle API exceptions and display them to the user using the typer library.
"""

import typer
from rich.console import Console
from rich.traceback import Traceback
from skylock_cli.api.http_client import SkyLockAPIError

err_console = Console(stderr=True)


class APIExceptionHandler:
    """A context manager to handle exceptions and display them to the user using typer"""

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Exit the runtime context related to this object.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception instance.
            exc_traceback (traceback): The traceback object.

        Returns:
            bool: False if an exception was handled, otherwise None.
        """
        if isinstance(exc_value, SkyLockAPIError):
            err_console.print(f"[red]{exc_value}[/red]")
            raise typer.Exit(code=1)
        if exc_type is not None:
            tb = Traceback.from_exception(
                exc_type, exc_value, exc_traceback, max_frames=5
            )
            err_console.print(tb)
            raise typer.Exit(code=1)

        return False
