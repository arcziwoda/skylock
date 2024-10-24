"""
Context model class.
"""

from pydantic import BaseModel
from skylock_cli.model.token import Token
from skylock_cli.model.user_dir import UserDir


class Context(BaseModel):
    """Stores context information."""

    token: Token = None
    user_dir: UserDir = None
