"""
Module for exceptions raised by the SkyLock API.
"""


class SkyLockAPIError(Exception):
    """Base exception for SkyLock API errors.

    Args:
        message (Optional[str]): The error message associated with the exception.
    """

    def __init__(self, message: str) -> None:
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
        directory_path (str): The path of the directory that already exists.
    """

    def __init__(self, directory_path: str) -> None:
        message = f"Directory `{directory_path}` already exists!"
        super().__init__(message)


class DirectoryNotFoundError(SkyLockAPIError):
    """Exception raised when attempting to delete a directory that does not exist.

    Args:
        directory_path (str): The path of the directory that does not exist.
    """

    def __init__(self, directory_path: str) -> None:
        message = f"Directory `{directory_path}` does not exist!"
        super().__init__(message)


class DirectoryMissingError(SkyLockAPIError):
    """Exception raised when a directory is missing.

    Args:
        missing (str): The path of the missing directory.
    """

    def __init__(self, missing: str) -> None:
        message = f"Directory `{missing}` is missing! Use the --parent flag to create parent directories."
        super().__init__(message)


class UserUnauthorizedError(SkyLockAPIError):
    """Exception raised when the user is unauthorized to perform an operation."""

    def __init__(self) -> None:
        message = "User is unauthorized. Please login to use this command."
        super().__init__(message)


class InvalidPathError(SkyLockAPIError):
    """Exception raised when the path is invalid.

    Args:
        path (str): The path that is invalid.
    """

    def __init__(self, path: str) -> None:
        message = f"Invalid path `{path}`!"
        super().__init__(message)
