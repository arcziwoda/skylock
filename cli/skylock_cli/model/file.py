"""
Module with File model class
"""

from pathlib import Path
from pydantic import BaseModel


class File(BaseModel):
    """Stores file metadata"""

    name: str
    path: Path
