"""
Module to handle API exceptions and display them to the user using the typer library.
"""

import typer


class CliExceptionHandler:
    """A context manager to handle exceptions and display them to the user using typer"""

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, _):
        if hasattr(exc_value, "status_code") and exc_value.status_code:
            typer.secho(
                f"{exc_type.__name__} occurred: {exc_value.detail} ({exc_value.status_code})",
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)

        if exc_type is not None:
            typer.secho(f"{exc_type} occurred: {exc_value}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        return False
