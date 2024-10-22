"""
Module to handle HTTP requests to API
"""

from http import HTTPStatus
from httpx import Client
from skylock_cli.config import API_URL, API_HEADERS
from skylock_cli.model.user import User
from skylock_cli.model.token import Token
from skylock_cli.api.http_exceptions import (
    SkyLockAPIError,
    UserAlreadyExistsError,
    AuthenticationError,
    TokenNotFoundError,
)

client = Client(base_url=API_URL)


def send_register_request(user: User) -> None:
    """
    Send a register request to the SkyLock backend API.

    Args:
        user (User): The user object containing registration details.

    Raises:
        UserAlreadyExistsError: If the user already exists.
        SkyLockAPIError: If there is an error during registration.
    """
    url = "/auth/register"

    response = client.post(url, json=user.model_dump(), headers=API_HEADERS)
    if response.status_code == HTTPStatus.CONFLICT:
        raise UserAlreadyExistsError(user.username)
    if response.status_code != HTTPStatus.CREATED:
        raise SkyLockAPIError("Failed to register user (Internal Server Error)")


def send_login_request(user: User) -> Token:
    """
    Send a login request to the SkyLock backend API.

    Args:
        user (User): The user object containing login details.

    Raises:
        AuthenticationError: If the authentication fails.
        SkyLockAPIError: If there is an error during login.
        TokenNotFoundError: If the token is not found in the response.

    Returns:
        Token: The token object containing authentication token.
    """
    url = "/auth/login"

    response = client.post(url, json=user.model_dump(), headers=API_HEADERS)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise AuthenticationError()
    if response.status_code != HTTPStatus.OK:
        raise SkyLockAPIError("Failed to login user (Internal Server Error)")

    token_data = response.json()
    if not token_data:
        raise TokenNotFoundError()

    return Token(**token_data)
