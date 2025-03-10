class UserAlreadyExists(Exception):
    """Exception raised when trying to register a user that already exists."""

    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    """Exception raised when trying to use invalid credentials"""

    def __init__(self, message="Invalid credentials provided"):
        self.message = message
        super().__init__(self.message)


class ResourceAlreadyExistsException(Exception):
    """Exception raised when trying to create a resource when there is already one with the same name"""

    def __init__(self, message="Resource already exists"):
        self.message = message
        super().__init__(self.message)


class ResourceNotFoundException(Exception):
    """Exception raised when trying to access a non existent resource"""

    def __init__(self, missing_resource_name: str, message="Resource not found"):
        self.missing_resource_name = missing_resource_name
        self.message = message
        super().__init__(self.message)


class InvalidPathException(Exception):
    """Exception raised when trying to use invalid path format"""

    def __init__(self, message="Invalid path format"):
        self.message = message
        super().__init__(self.message)


class FolderNotEmptyException(Exception):
    """Exception raised when trying to do forbidden operation on not empty folder"""

    def __init__(self, message="Folder not empty"):
        self.message = message
        super().__init__(self.message)


class ForbiddenActionException(Exception):
    """Exception raised when trying to do some forbidden action (for example deleting root folder)"""

    def __init__(self, message="Action forbidden"):
        self.message = message
        super().__init__(self.message)


class RootFolderAlreadyExistsException(Exception):
    """Exception raised when trying to create an already existing root folder"""

    def __init__(self, message="Root folder already exists"):
        self.message = message
        super().__init__(self.message)
