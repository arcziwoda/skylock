"""
Model for user directory.
"""

from pathlib import Path
from pydantic import BaseModel, field_serializer


class UserDir(BaseModel):
    """Stores information abit user cwd."""

    path: Path

    @field_serializer("path")
    def serialize_path(self, path: Path) -> str:
        """Serialize path."""
        return str(path)
