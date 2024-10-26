"""
Module that contains logic for the cli commands related to authentication
"""

from pathlib import Path
from skylock_cli.model.user import User
from skylock_cli.model.user_dir import UserDir
from skylock_cli.api.http_client import send_login_request, send_register_request
from skylock_cli.utils.api_exception_handler import APIExceptionHandler
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.model.context import Context


def register_user(login: str, password: str) -> None:
    """
    Register a new user.

    Args:
        login (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        None
    """
    user = User(username=login, password=password)
    with APIExceptionHandler():
        send_register_request(user)


def login_user(login: str, password: str) -> UserDir:
    """
    Login an existing user.

    Args:
        login (str): The username of the user.
        password (str): The password of the user.

    Returns:
        Token: The token object containing the authentication token.
    """
    user = User(username=login, password=password)
    with APIExceptionHandler():
        token = send_login_request(user)

    # TODO This should be handled by the context manager (and tested)
    previous_context = ContextManager.get_context()
    cwd = (
        previous_context.user_dir
        if previous_context.user_dir.path
        else UserDir(path=Path("/"))
    )
    new_context = Context(token=token, user_dir=cwd)
    ContextManager.save_context(new_context)
    return cwd
