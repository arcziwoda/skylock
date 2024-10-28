"""
Module that contains the token model.
"""

from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Represents an authentication token returned from the API.

    Attributes:
        access_token (str): The token used for authenticated requests.
        token_type (str): The type of the token, typically 'Bearer'.
    """

    access_token: Optional[str] = Field(default="")
    token_type: Optional[str] = Field(default="")
