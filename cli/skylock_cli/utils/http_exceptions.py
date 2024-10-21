"""
Module to handle HTTP exceptions
"""

import httpx
import typer


class HTTPExceptionHandler:
    """A context manager to handle HTTP exceptions"""

    def __enter__(self): ...

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is httpx.HTTPStatusError:
            response = exc_value.response
            try:
                error_detail = response.json().get("detail", "An error occurred")
            except ValueError:
                error_detail = response.text or "An error occurred"

            typer.secho(f"HTTP error code {response.status_code} occurred: {error_detail}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        if exc_type is not None:
            typer.secho(f"An unexpected error occurred: {exc_value}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        return False
