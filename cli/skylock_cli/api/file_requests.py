"""
Module to send file requests to the SkyLock backend API.
"""

from urllib.parse import quote
from http import HTTPStatus
from pathlib import Path
from httpx import Client
from skylock_cli.config import API_URL
from skylock_cli.model.token import Token
from skylock_cli.api import bearer_auth
from skylock_cli.exceptions import api_exceptions

client = Client(base_url=API_URL)


def send_upload_request(token: Token, virtual_path: Path, file_metadata: dict) -> None:
    """
    Send an upload request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path where the file should be uploaded.
        files (dict): The file to upload.
    """
    url = "/files/upload" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)

    response = client.post(url=url, auth=auth, files=file_metadata)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.CONFLICT:
        raise api_exceptions.FileAlreadyExistsError(virtual_path)

    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise api_exceptions.InvalidPathError(virtual_path)

    if response.status_code != HTTPStatus.CREATED:
        raise api_exceptions.SkyLockAPIError(
            "Failed to upload file (Internal Server Error)"
        )


def send_download_request(token: Token, virtual_path: Path) -> dict:
    """
    Send a download request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path of the file to download.
    """
    url = "/files/download" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)

    response = client.get(url=url, auth=auth)

    if response.status_code == HTTPStatus.UNAUTHORIZED:
        raise api_exceptions.UserUnauthorizedError()

    if response.status_code == HTTPStatus.BAD_REQUEST:
        raise api_exceptions.InvalidPathError(virtual_path)

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise api_exceptions.FileNotFoundError(virtual_path)

    if response.status_code != HTTPStatus.OK:
        raise api_exceptions.SkyLockAPIError(
            "Failed to download file (Internal Server Error)"
        )

    response_json = response.json()

    if "file_content" not in response_json or "file_name" not in response_json:
        raise api_exceptions.InvalidResponseFormatError()

    return response_json
