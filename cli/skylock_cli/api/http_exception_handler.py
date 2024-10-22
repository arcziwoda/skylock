"""
Module to handle HTTP exceptions and translate them to custom exceptions.
"""

from http import HTTPStatus
from httpx import HTTPStatusError
from skylock_cli.api.http_exceptions import (
    SkyLockAPIError,
    UserAlreadyExistsError,
    AuthenticationError,
)


class HTTPExceptionHandler:
    """A context manager to handle HTTP exceptions and translate them to custom exceptions"""

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, _):
        if isinstance(exc_value, HTTPStatusError):
            status_code = exc_value.response.status_code

            try:
                detail = exc_value.response.json().get("detail", "An error occurred")
            except ValueError:
                detail = exc_value.response.text or "An error occurred"

            if status_code == HTTPStatus.CONFLICT:
                raise UserAlreadyExistsError("User with username already exists", status_code, detail) from exc_value

            if status_code == HTTPStatus.UNAUTHORIZED:
                raise AuthenticationError("Failed to authenticate user", status_code, detail) from exc_value

            raise SkyLockAPIError(f"HTTP error occurred: {detail}", status_code, detail) from exc_value
