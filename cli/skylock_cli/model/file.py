"""
Module with File model class
"""

from pathlib import Path
from pydantic import BaseModel
from typer.colors import YELLOW


class File(BaseModel):
    """Stores file metadata"""

    name: str
    path: Path
    color: str = YELLOW
