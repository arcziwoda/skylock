"""
Module to handle HTTP requests to API
"""

from httpx import Client
from skylock_cli.config import API_URL
from skylock_cli.model.user import User
from skylock_cli.model.token import Token

client = Client(base_url=API_URL)


def send_register_request(user: User) -> None:
    """
    Send a register request to the SkyLock backend API
    """
    url = "/auth/register"
    headers = {"Content-Type": "application/json"}

    client.post(url, json=user.model_dump(), headers=headers).raise_for_status()


def send_login_request(user: User) -> Token:
    """
    Send a login request to the SkyLock backend API
    """
    url = "/auth/login"
    headers = {"Content-Type": "application/json"}

    response = client.post(url, json=user.model_dump(), headers=headers)

    response.raise_for_status()

    token_data = response.json()
    if not token_data:
        raise ValueError("Token not found in the response")

    return Token(**token_data)
