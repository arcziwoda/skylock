"""
Context model class.
"""

from typing import Optional, Annotated
from pydantic import BaseModel, Field
from skylock_cli.model.token import Token
from skylock_cli.model.directory import Directory


class Context(BaseModel):
    """Stores context information."""

    token: Annotated[Optional[Token], Field(description="Token object")] = None
    cwd: Annotated[
        Optional[Directory], Field(description="Current working directory")
    ] = None
