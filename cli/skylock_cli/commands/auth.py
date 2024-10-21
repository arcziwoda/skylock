"""
Module that contains logic for the cli commands related to authentication
"""

from skylock_cli.model.token import Token
from skylock_cli.model.user import User
from skylock_cli.api.http_client import send_login_request, send_register_request
from skylock_cli.utils.http_exceptions import HTTPExceptionHandler


def register_user(login: str, password: str) -> None:
    """Register a new user"""
    user = User(username=login, password=password)
    with HTTPExceptionHandler():
        send_register_request(user)


def login_user(login: str, password: str) -> Token:
    """Login user"""
    user = User(username=login, password=password)
    with HTTPExceptionHandler():
        return send_login_request(user)
