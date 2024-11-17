"""
Module with File model class
"""

from pathlib import Path
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from typer.colors import YELLOW


class File(BaseModel):
    """Stores file metadata"""

    name: Annotated[str, Field(description="File name")]
    path: Annotated[Path, Field(description="File path")]
    color: Annotated[
        Optional[str], Field(description="File color used to pretty print in CLI")
    ] = YELLOW
