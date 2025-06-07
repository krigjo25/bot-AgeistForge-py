#   Error handler

from typing import Optional

class ExceptionHandler(Exception):
    """ Base class for all exceptions """

    def __init__(self, message:Optional[str] = None, code:Optional[int] = 000) -> None:
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "An error occurred"

class OperationalError(ExceptionHandler):
    """ Raises when a database operation is not allowed """

    error = {
        000:"Dublicated data",
        200:"Table already exists with-in the database",
        404:"Table was not found in the database",
        500:'Column has to be a type of list'}

    def __init__(self, message:Optional[str] = None, code:int = 000) -> None:
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else self.error[code]

class ResourceNotFoundError(ExceptionHandler):
    """ Raises when the requested resource is not found """

    def __init__(self, message:Optional[str] = None, code:int = 400) -> None:
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "Resource not found"
        
class SelfReferenceError(ExceptionHandler):
    """ Raises when the requested member is the Author of the request """

    def __init__(self, message:Optional[str] = None, code:int = 503) -> None:
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "Could not perform action on self, please try again with another member"

class InvalidDurationError(ExceptionHandler):
    """ Raises when the requested duration is not valid """

    def __init__(self, message:Optional[str] = None, code:int = 400) -> None:
        super().__init__(message, code)
        self.status_code = code
        self.message = f"{code} : " + message if message else f"{code} : Invalid duration specified"

class AuthorizationError(ExceptionHandler):
    """ Raises when the a user tries to authorize something forbidden """

    def __init__(self, message:Optional[str] = None, code:int = 403) -> None:
        super().__init__(message, code)
        self.message = f"{code} : " + message if message else f"{code} : You are not authorized to perform this action on this member"

class DuplicationError(ExceptionHandler):
    """ Duplication error raises when a resource already exists """

    def __init__(self, message:Optional[str] = None, code:int = 200) -> None:
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "Resource already exists"

class NotImplementedError(ExceptionHandler):
    """ Raises when a feature is not implemented yet """

    def __init__(self, message:Optional[str] = None, code:int = 501) -> None:
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "This feature is not implemented yet"