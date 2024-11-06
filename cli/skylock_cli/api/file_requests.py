"""
Module to send file requests to the SkyLock backend API.
"""

from urllib.parse import quote
from pathlib import Path
from httpx import Client
from skylock_cli.config import API_URL
from skylock_cli.model.token import Token
from skylock_cli.api import bearer_auth

client = Client(base_url=API_URL)


def send_upload_request(token: Token, virtual_path: Path, real_file_path: Path) -> None:
    """
    Send an upload request to the SkyLock backend API.

    Args:
        token (Token): The token object containing authentication token.
        virtual_path (Path): The path where the file should be uploaded.
        real_file_path (Path): The path of the real file to be uploaded.
    """
    url = "/files/upload" + quote(str(virtual_path))
    auth = bearer_auth.BearerAuth(token)

    with open(real_file_path, "rb") as file:
        files = {"upload-file": file}

    print(url, auth, files)

    # response = client.post(url=url, auth=auth, files=files)
