"""
Module to send directory requests to the SkyLock backend API.
"""

from urllib.parse import quote
from pathlib import Path
from http import HTTPStatus
from httpx import Client
from skylock_cli.config import API_URL, API_HEADERS
from skylock_cli.exceptions import api_exceptions
from skylock_cli.model.token import Token
from skylock_cli.api import bearer_auth

client = Client(base_url=API_URL)


def send_mkdir_request(token: Token, path: Path, parent: bool) -> None:
    """
    Send a mkdir request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        path (str): The path of the directory to be created.
        parent (bool): If True, create parent directories if they do not exist.
    """
    url = "/folders" + quote(str(path))
    auth = bearer_auth.BearerAuth(token)
    params = {"parent": parent}
    # TODO: Implement the request body for the mkdir request when the API is updated.
    print(params)

    response = client.post(
        url=url,
        auth=auth,
        headers=API_HEADERS,
        # params=params
    )

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.CONFLICT:
        raise api_exceptions.DirectoryAlreadyExistsError(str(path))

    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise api_exceptions.InvalidPathError(str(path))

    if response.status_code == HTTPStatus.NOT_FOUND:
        missing = response.json().get("missing", str(path))
        raise api_exceptions.DirectoryMissingError(missing)

    if response.status_code != HTTPStatus.CREATED:
        raise api_exceptions.SkyLockAPIError("Failed to create directory (Internal Server Error)")


def send_rmdir_request(token: Token, path: Path, recursive: bool) -> None:
    """
    Send a rm request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        path (str): The path of the directory to be deleted.
        force (bool): If True, delete the directory recursively.
    """
    url = "/folders" + quote(str(path))
    auth = bearer_auth.BearerAuth(token)
    params = {"recursive": recursive}
    # TODO: Implement the request body for the rmdir request when the API is updated.
    print(params)

    response = client.delete(
        url=url,
        auth=auth,
        headers=API_HEADERS,
        # params=params
    )

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.DirectoryNotFoundError(str(path))

    if response.status_code == HTTPStatus.CONFLICT:
        raise api_exceptions.DirectoryNotEmptyError(str(path))

    if response.status_code != HTTPStatus.NO_CONTENT:
        raise api_exceptions.SkyLockAPIError("Failed to delete directory (Internal Server Error)")
