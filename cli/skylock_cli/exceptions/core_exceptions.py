"""
Module for exceptions raised by the SkyLock Core.
"""


class SkyLockCoreError(Exception):
    """Base exception for SkyLock Core errors.

    Args:
        message (Optional[str]): The error message associated with the exception.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotADirectoryError(SkyLockCoreError):
    """Exception raised when a directory is expected but a file is provided.

    Args:
        path (str): The path of the file.
    """

    def __init__(self, path: str) -> None:
        message = f"{path} is not a directory"
        super().__init__(message)
