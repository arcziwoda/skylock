"""
This module contains the functions to send requests to the SkyLock backend API for navigation purposes.
"""

from http import HTTPStatus
from urllib.parse import quote
from pathlib import Path
from httpx import Client
from skylock_cli.config import API_URL, API_HEADERS
from skylock_cli.core.context_manager import ContextManager
from skylock_cli.model.token import Token
from skylock_cli.api import bearer_auth
from skylock_cli.exceptions import api_exceptions

client = Client(base_url=ContextManager.get_context().base_url + API_URL)


def send_ls_request(token: Token, path: Path):
    """Send a ls request to the SkyLock backend API."""
    url = "/folders" + quote(str(path))
    auth = bearer_auth.BearerAuth(token)

    response = client.get(url=url, auth=auth, headers=API_HEADERS)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.DirectoryNotFoundError(path)

    if response.status_code != HTTPStatus.OK:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to list directory (Error Code: {response.status_code})"
        )

    if (
        not response.json()
        or "files" not in response.json()
        or "folders" not in response.json()
    ):
        raise api_exceptions.InvalidResponseFormatError()

    return response.json()


def send_cd_request(token: Token, path: Path) -> None:
    """Send a cd request to the SkyLock backend API."""
    url = "/folders" + quote(str(path))
    auth = bearer_auth.BearerAuth(token)

    response = client.get(url=url, auth=auth, headers=API_HEADERS)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.DirectoryNotFoundError(path)

    if response.status_code != HTTPStatus.OK:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to change directory (Error Code: {response.status_code})"
        )
