"""
Module that contains the token model.
"""

from typing import Optional, Annotated
from pydantic import BaseModel, Field
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError


class Token(BaseModel):
    """
    Represents an authentication token returned from the API.
    """

    access_token: Annotated[Optional[str], Field(description="Access token")] = ""
    token_type: Annotated[Optional[str], Field(description="Token type")] = "Bearer"

    def is_valid(self) -> bool:
        """
        Checks if the token is valid.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        if not self.access_token:
            return False
        try:
            jwt.decode(self.access_token, key="", options={"verify_signature": False})
            return True
        except JWTError:
            return False

    def is_expired(self) -> bool:
        """
        Checks if the token is expired.

        Returns:
            bool: True if the token is expired, False otherwise.
        """
        if not self.access_token:
            return False
        try:
            jwt.decode(self.access_token, key="", options={"verify_signature": False})
            return False
        except ExpiredSignatureError:
            return True
