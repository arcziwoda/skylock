"""
Module to send file requests to the SkyLock backend API.
"""

from urllib.parse import quote
from http import HTTPStatus
from pathlib import Path
from httpx import Client
from skylock_cli.config import API_URL, API_HEADERS
from skylock_cli.model.token import Token
from skylock_cli.api import bearer_auth
from skylock_cli.exceptions import api_exceptions

client = Client(base_url=API_URL)


def send_upload_request(
    token: Token, virtual_path: Path, files: dict, force: bool, public: bool
) -> None:
    """
    Send an upload request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path where the file should be uploaded.
        files (dict): The file to upload.
    """
    url = "/files/upload" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)
    params = {"force": force, "public": public}

    response = client.post(url=url, auth=auth, files=files, params=params)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.CONFLICT:
        if not force:
            raise api_exceptions.FileAlreadyExistsError(virtual_path)

    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise api_exceptions.InvalidPathError(virtual_path)

    if response.status_code != HTTPStatus.CREATED:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to upload file (Error Code: {response.status_code})"
        )


def send_download_request(token: Token, virtual_path: Path) -> bytes:
    """
    Send a download request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path of the file to download.

    Returns:
        bytes: The binary content of the downloaded file.
    """
    url = "/files/download" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)

    response = client.get(url=url, auth=auth, headers=API_HEADERS)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise api_exceptions.InvalidPathError(virtual_path)

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.FileNotFoundError(virtual_path)

    if response.status_code != HTTPStatus.OK:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to download file (Error Code: {response.status_code})"
        )

    if not response.content:
        raise api_exceptions.InvalidResponseFormatError()

    return response.content


def send_rm_request(token: Token, virtual_path: Path) -> None:
    """
    Send a remove request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path of the file to remove.
    """
    url = "/files" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)

    response = client.delete(url=url, auth=auth, headers=API_HEADERS)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise api_exceptions.InvalidPathError(virtual_path)

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.FileNotFoundError(virtual_path)

    if response.status_code != HTTPStatus.NO_CONTENT:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to remove file (Error Code: {response.status_code})"
        )


def send_make_public_request(token: Token, virtual_path: Path) -> None:
    """
    Send a make public request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path of the file to be made public.
    """
    url = "/files" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)
    body = {"is_public": True}

    response = client.patch(url=url, auth=auth, headers=API_HEADERS, json=body)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.FileNotFoundError(virtual_path)

    if response.status_code != HTTPStatus.OK:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to make file public (Error Code: {response.status_code})"
        )


def send_make_private_request(token: Token, virtual_path: Path) -> None:
    """
    Send a make private request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path of the file to be made private.
    """
    url = "/files" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)
    body = {"is_public": False}

    response = client.patch(url=url, auth=auth, headers=API_HEADERS, json=body)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.FileNotFoundError(virtual_path)

    if response.status_code != HTTPStatus.OK:
        raise api_exceptions.SkyLockAPIError(
            f"Failed to make file private (Error Code: {response.status_code})"
        )
