"""
Module to send directory requests to the SkyLock backend API.
"""

from urllib.parse import quote
from pathlib import Path
from http import HTTPStatus
from httpx import Client
from skylock_cli.config import API_URL, API_HEADERS
from skylock_cli.model.token import Token
from skylock_cli.api import bearer_auth, api_exceptions

client = Client(base_url=API_URL)


def send_mkdir_request(token: Token, path: Path) -> None:
    """
    Send a mkdir request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        path (str): The path of the directory to be created.
    """
    url = "/folders" + quote(str(path))
    auth = bearer_auth.BearerAuth(token)

    response = client.post(
        url=url,
        auth=auth,
        headers=API_HEADERS,
    )

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.CONFLICT:
        raise api_exceptions.DirectoryAlreadyExistsError(path)

    if response.status_code != HTTPStatus.CREATED:
        raise api_exceptions.SkyLockAPIError(
            "Failed to create directory (Internal Server Error)"
        )


def send_rmdir_request(token: Token, path: Path) -> None:
    """
    Send a rmdir request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        path (str): The path of the directory to be deleted
    """
    url = "/folders" + quote(str(path))
    auth = bearer_auth.BearerAuth(token)

    response = client.delete(
        url=url,
        auth=auth,
        headers=API_HEADERS,
    )

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.DirectoryNotFoundError(path)

    if response.status_code != HTTPStatus.NO_CONTENT:
        raise api_exceptions.SkyLockAPIError(
            "Failed to delete directory (Internal Server Error)"
        )
