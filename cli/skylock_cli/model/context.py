"""
Context model class.
"""

from typing import Optional
from pydantic import BaseModel, Field
from skylock_cli.model.token import Token
from skylock_cli.model.user_dir import UserDir


class Context(BaseModel):
    """Stores context information."""

    token: Optional[Token] = Field(default=None)
    user_dir: Optional[UserDir] = Field(default=None)
