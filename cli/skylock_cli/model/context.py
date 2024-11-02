"""
Context model class.
"""

from typing import Optional
from pydantic import BaseModel, Field
from skylock_cli.model.token import Token
from skylock_cli.model.directory import Directory


class Context(BaseModel):
    """Stores context information."""

    token: Optional[Token] = Field(default=None)
    cwd: Optional[Directory] = Field(default=None)
