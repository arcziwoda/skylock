"""
Model for user directory.
"""

from pathlib import Path
from pydantic import BaseModel


class UserDir(BaseModel):
    """Stores information abit user cwd."""

    path: Path
