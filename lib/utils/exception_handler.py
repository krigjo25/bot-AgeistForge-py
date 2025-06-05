#   Error handler

from typing import Optional

class ExceptionHandler(Exception):
    """ Base class for all exceptions """

    def __init__(self, message:Optional[str] = None, code:int = 400):
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "An error occurred"

        if not message:
            self.message = "An error occurred"

class OperationalError(ExceptionHandler):
    """ Raises when a database operation is not allowed """

    error = {
        000:"Dublicated data",
        200:"Table already exists with-in the database",
        404:"Table was not found in the database",
        500:'Column has to be a type of list'}

    def __init__(self, message:Optional[str] = None, code:int = 000):
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else self.error[code]

class NotFoundError(ExceptionHandler):
    """ Raises when the requested resource is not found """

    def __init__(self, message:Optional[str] = None, code:int = 400):
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "Resource not found"
        
class SelfReferenceError(ExceptionHandler):
    """ Raises when the requested member is the Author of the request """

    def __init__(self, message:Optional[str] = None, code:int = 503):
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "Could not perform action on self, please try again with another member"

class InvalidDurationError(ExceptionHandler):
    """ Raises when the requested duration is not valid """

    def __init__(self, message:Optional[str] = None, code:int = 400):
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "Invalid duration specified"

class AuthorizationError(ExceptionHandler):
    """ Raises when the a user tries to authorize something forbidden """

    def __init__(self, message:Optional[str] = None, code:int = 403):
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "You are not authorized to perform this action on this member"

class DuplicationError(ExceptionHandler):
    """ Base class for all exceptions """

    def __init__(self, message:Optional[str] = None, code:int = 200):
        super().__init__(message, code)
        self.status_code = code
        self.message = message if message else "An error occurred"

        if not message:
            self.message = "An error occurred"
