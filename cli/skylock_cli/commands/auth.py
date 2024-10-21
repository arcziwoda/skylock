"""
Module that contains logic for the cli commands related to authentication
"""

from skylock_cli.model.user import User
from skylock_cli.api.http_client import send_register_request
from skylock_cli.utils.http_exceptions import HTTPExceptionHandler


def register_user(login: str, password: str) -> None:
    """Register a new user"""
    user = User(login, password)
    with HTTPExceptionHandler():
        send_register_request(user)
