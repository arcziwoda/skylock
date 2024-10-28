"""
This module contains the BearerAuth class for bearer token authentication.
"""

from typing import Generator
from httpx import Request, Response, Auth
from skylock_cli.model.token import Token


class BearerAuth(Auth):
    """Custom HTTPX authentication class for bearer token authentication."""

    def __init__(self, token: Token) -> None:
        self.token = token

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token.access_token}"
        yield request
