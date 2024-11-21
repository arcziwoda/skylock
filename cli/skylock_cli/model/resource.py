"""Resource model"""

from pydantic import BaseModel, PrivateAttr
from skylock_cli.model.resource_visibility import ResourceVisibility


class Resource(BaseModel):
    """Base class for resources"""

    _is_public: bool = PrivateAttr(False)
    _visibility: ResourceVisibility = PrivateAttr(ResourceVisibility.PRIVATE)

    def __init__(self, **data):
        """Custom initialization to handle is_public logic"""
        super().__init__(**data)
        if data.get("is_public", False):
            self.make_public()

    def make_public(self):
        """Make the resource public"""
        self._is_public = True
        self._visibility = ResourceVisibility.PUBLIC

    def make_private(self):
        """Make the resource private"""
        self._is_public = False
        self._visibility = ResourceVisibility.PRIVATE

    @property
    def is_public(self) -> bool:
        """Get whether the resource is public"""
        return self._is_public

    @property
    def visibility_label(self) -> str:
        """Get the visibility label"""
        return self._visibility.label

    @property
    def visibility_color(self) -> str:
        """Get the visibility color"""
        return self._visibility.color
