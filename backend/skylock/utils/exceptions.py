class UserAlreadyExists(Exception):
    """Exception raised when trying to register a user that already exists."""

    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class AccessDeniedException(Exception):
    """Exception raised when trying to perform an operation with no required permissions"""

    def __init__(self, message="Access denied"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    """Exception raised when trying to use invalid credentials"""

    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """Exception raised when trying to retrive non existent user"""

    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)
