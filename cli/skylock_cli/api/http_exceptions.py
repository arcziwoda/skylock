"""
Module for exceptions raised by the SkyLock API.
"""

from typing import Optional


class SkyLockAPIError(Exception):
    """Base exception for SkyLock API errors.

    Args:
        message (Optional[str]): The error message associated with the exception.
    """

    def __init__(self, message: Optional[str]) -> None:
        message = (
            message + " (Internal Server Error)" if message else "Internal Server Error"
        )
        super().__init__(message)
        self.message = message


class UserAlreadyExistsError(SkyLockAPIError):
    """Exception raised when attempting to register a user that already exists.

    Args:
        username (str): The username of the user that already exists.
    """

    def __init__(self, username: str) -> None:
        message = f"User with username `{username}` already exists!"
        super().__init__(message)


class AuthenticationError(SkyLockAPIError):
    """Exception raised for authentication errors."""

    def __init__(self) -> None:
        message = "Invalid username or password!"
        super().__init__(message)


class TokenNotFoundError(SkyLockAPIError):
    """Exception raised when the token is not found in the response."""

    def __init__(self) -> None:
        message = "Token not found in the response!"
        super().__init__(message)


class DirectoryAlreadyExistsError(SkyLockAPIError):
    """Exception raised when attempting to create a directory that already exists.

    Args:
        directory_name (str): The name of the directory that already exists.
    """

    def __init__(self, directory_name: str) -> None:
        message = f"Directory `{directory_name}` already exists!"
        super().__init__(message)


class UserUnauthorizedError(SkyLockAPIError):
    """Exception raised when the user is unauthorized to perform an operation."""

    def __init__(self) -> None:
        message = "User is unauthorized. Please login to use this command."
        super().__init__(message)
