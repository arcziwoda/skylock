"""
Model for user directory.
"""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, field_serializer, Field


class UserDir(BaseModel):
    """Stores information abit user cwd."""

    path: Optional[Path] = Field(default=Path("/"))

    @field_serializer("path")
    def serialize_path(self, path: Path) -> str:
        """Serialize path."""
        return str(path)

    def __str__(self) -> str:
        return str(self.path)
