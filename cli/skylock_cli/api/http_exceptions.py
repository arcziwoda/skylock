"""
Module for exceptions raised by the SkyLock API
"""


class SkyLockAPIError(Exception):
    """Base exception for SkyLock API errors"""

    def __init__(self, message, status_code=None, detail=None):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail


class UserAlreadyExistsError(SkyLockAPIError):
    """Exception raised when trying to register a user that already exists"""


class AuthenticationError(SkyLockAPIError):
    """Exception raised for authentication errors"""


class TokenNotFoundError(SkyLockAPIError):
    """Exception raised when the token is not found in the response"""
