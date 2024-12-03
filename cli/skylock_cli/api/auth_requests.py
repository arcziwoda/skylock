"""
Module to handle HTTP requests to API
"""

from http import HTTPStatus
from httpx import Client
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.config import API_HEADERS, API_URL
from skylock_cli.model import user, token
from skylock_cli.exceptions import api_exceptions

client = Client(base_url=ContextManager.get_context().base_url + API_URL)


def send_register_request(_user: user.User) -> None:
    """
    Send a register request to the SkyLock backend API.

    Args:
        user (User): The user object containing registration details.

    Raises:
        UserAlreadyExistsError: If the user already exists.
        SkyLockAPIError: If there is an error during registration.
    """
    url = "/auth/register"

    response = client.post(url, json=_user.model_dump(), headers=API_HEADERS)
    if response.status_code == HTTPStatus.CONFLICT:
        raise api_exceptions.UserAlreadyExistsError(_user.username)
    if response.status_code != HTTPStatus.CREATED:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to register user (Error Code: {response.status_code})"
        )


def send_login_request(_user: user.User) -> token.Token:
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

    response = client.post(url, json=_user.model_dump(), headers=API_HEADERS)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.AuthenticationError()
    if response.status_code != HTTPStatus.OK:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to login user (Error Code: {response.status_code})"
        )

    token_data = response.json()
    if not token_data:
        raise api_exceptions.TokenNotFoundError()

    return token.Token(**token_data)
