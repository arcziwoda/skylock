"""
Module with Directory model class
"""

from pathlib import Path
from pydantic import BaseModel, field_validator
from typer.colors import MAGENTA


class Directory(BaseModel):
    """Stores directory metadata"""

    name: str
    path: Path
    color: str = MAGENTA

    @field_validator("name")
    def ensure_trailing_slash(cls, _name: str) -> str:
        """Ensure that the directory name ends with a slash"""
        if not _name.endswith("/"):
            return _name + "/"
        return _name
