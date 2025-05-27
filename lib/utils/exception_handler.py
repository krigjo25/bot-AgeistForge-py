#   Error handler

from typing import Optional


class ExceptionHandler(Exception):
    """ Base class for all exceptions """

    def __init__(self, code:int, message:Optional[str]):
        super().__init__(code, message)
        self.status_code = code
        self.message = message if message else "An error occurred"
        

        if not message:
            self.message = "An error occurred"


class OperationalError(ExceptionHandler):
    """ Raises when duplicated is not allowed """

    error = {
        000:"Dublicated data",
        200:"Table already exists with-in the database",
        404:"Table does not exist in the database",
        500:'Column has to be a type of list'}

    def __init__(self, code:int, message:Optional[str]):
        super().__init__(code, message)
        self.status_code = code
        self.message = message if message else self.error[code]


class NotFoundError(ExceptionHandler):
    """ Raises when the requested resource is not found """

    def __init__(self, code:int, message:Optional[str]):
        super().__init__(code, message)
        self.status_code = code
        self.message = message if message else "Resource not found"
        
