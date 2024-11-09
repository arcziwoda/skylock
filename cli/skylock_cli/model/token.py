"""
Module that contains the token model.
"""

from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from jose import jwt
from jose.exceptions import JWTError


class Token(BaseModel):
    """
    Represents an authentication token returned from the API.

    Attributes:
        access_token (str): The token used for authenticated requests.
        token_type (str): The type of the token, typically 'Bearer'.
    """

    access_token: Optional[str] = Field(default="")
    token_type: Optional[str] = Field(default="")

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
            decoded_token = jwt.decode(self.access_token, key="", options={"verify_signature": False})
            exp = decoded_token.get("exp")
            return datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc) if exp else False
        except JWTError:
            return False
