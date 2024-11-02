"""
Module that contains logic for the cli commands related to authentication
"""

from pathlib import Path
from skylock_cli.api.auth_requests import send_login_request, send_register_request
from skylock_cli.utils.cli_exception_handler import CLIExceptionHandler
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.model import user, context, directory


def register_user(login: str, password: str) -> None:
    """
    Register a new user.

    Args:
        login (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        None
    """
    _user = user.User(username=login, password=password)
    with CLIExceptionHandler():
        send_register_request(_user)


def login_user(login: str, password: str) -> context.Context:
    """
    Login an existing user.

    Args:
        login (str): The username of the user.
        password (str): The password of the user.

    Returns:
        Token: The token object containing the authentication token.
    """
    _user = user.User(username=login, password=password)
    with CLIExceptionHandler():
        token = send_login_request(_user)

    new_context = context.Context(
        token=token,
        cwd=directory.Directory(path=Path("/")),
    )
    ContextManager.save_context(new_context)
    return new_context
