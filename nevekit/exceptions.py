# This module keeps all the library specific exceptions used in the nevekit package.


class NeveKitException(Exception):
    """Base class for exceptions in this package."""

    def __init__(self, message=None):
        self.message = message


class SwaggerClientNotFoundException(NeveKitException):
    """Exception raised when the Swagger client is not found. In memory or on disk."""

    def __init__(self):
        self.message = "Swagger client not found in memory or on disk."


class SwaggerClientFailedToInitializeException(NeveKitException):
    """Exception raised when the Swagger client fails to initialize."""

    def __init__(self):
        self.message = "Swagger client failed to initialize."
