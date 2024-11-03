"""
Module with Directory model class
"""

from pathlib import Path
from pydantic import (
    BaseModel,
    field_validator,
    model_validator,
    Field,
    field_serializer,
)
from typer.colors import MAGENTA
from skylock_cli.config import ROOT_PATH


class Directory(BaseModel):
    """Stores directory metadata"""

    path: Path = Field(default=ROOT_PATH)
    name: str = Field(default=None)
    color: str = MAGENTA

    @field_serializer("path")
    def serialize_path(self, path: Path) -> str:
        """Serialize path."""
        return str(path)

    @field_validator("name")
    def ensure_trailing_slash(cls, _name: str) -> str:
        """Ensure that the directory name ends with a slash"""
        if not _name.endswith("/"):
            return _name + "/"
        return _name

    @model_validator(mode="before")
    def set_name_from_path(cls, values):
        """Set the name from the path if name is not provided"""
        if "name" not in values or values["name"] is None:
            path = values.get("path", ROOT_PATH)
            values["name"] = path.name
        return values
