"""
Context model class.
"""

from pydantic import BaseModel
from skylock_cli.model.token import Token


class Context(BaseModel):
    """Stores context information."""

    token: Token = None
