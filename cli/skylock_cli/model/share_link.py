"""
Module with share link model class
"""

from typing import Annotated
from urllib.parse import urljoin
from pydantic import BaseModel, Field


class ShareLink(BaseModel):
    """Stores file metadata"""

    base_url: Annotated[str, Field(description="Base URL of the SkyLock server")]
    location: Annotated[str, Field(description="Location of the shared resource")]

    @property
    def url(self) -> str:
        """Get the URL of the shared resource"""
        return urljoin(self.base_url, self.location)
