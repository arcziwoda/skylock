"""
Module to handle HTTP requests to API
"""

from httpx import Client
from skylock_cli.config import API_URL, API_HEADERS
from skylock_cli.model.user import User
from skylock_cli.model.token import Token
from skylock_cli.api.http_exception_handler import HTTPExceptionHandler
from skylock_cli.api.http_exceptions import TokenNotFoundError

client = Client(base_url=API_URL)


def send_register_request(user: User) -> None:
    """
    Send a register request to the SkyLock backend API
    """
    url = "/auth/register"

    with HTTPExceptionHandler():
        client.post(url, json=user.model_dump(), headers=API_HEADERS).raise_for_status()


def send_login_request(user: User) -> Token:
    """
    Send a login request to the SkyLock backend API
    """
    url = "/auth/login"

    with HTTPExceptionHandler():
        response = client.post(
            url, json=user.model_dump(), headers=API_HEADERS
        ).raise_for_status()

    token_data = response.json()
    if not token_data:
        raise TokenNotFoundError("Token not found in the response")

    return Token(**token_data)
