"""
Module with Directory model class
"""

from pathlib import Path
from pydantic import BaseModel


class Directory(BaseModel):
    """Stores directory metadata"""

    name: str
    path: Path
