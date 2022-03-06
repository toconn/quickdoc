from sys import exc_info
from traceback import extract_tb


def exception_message(exception: Exception) -> str:

    if issubclass(exception, BaseException):

        return exception.message

    elif len(exception.args) > 0:

        message = exception.args[0]
        if type(message) == str:
            return message
        else:
            return str(type(message))


def exception_module_name() -> str:
    """
    Returns the module where the exception was raised.
    """
    execution_info = exc_info()[-1]
    stack = extract_tb(execution_info)
    return stack[0][2]


def exception_name(exception: Exception) -> str:
    return type(exception).__name__


# Classes ##################################################


class BaseException (Exception):

    def __init__(self, exception: Exception = None, message: str = None, messages: list = None):

        self.exception = exception

        if messages:
            if message:
                messages.append(message)
            self.messages = messages
        elif message:
            self.messages = [message]
        else:
            self.messages = []

    @property
    def message(self):
        return ', '.join(self.messages)


class AccessDenied (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class AlreadyExists (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class ApplicationError (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class ExternalServerError (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class FailedValidation (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class InvalidConfiguration (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class InvalidRequest (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class InvalidState (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class NotAuthorized (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class NotFound (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class RequestTimedOut (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)


class UserRequestExit (BaseException):
    def __init__(self, *args, **kwargs):
        BaseException.__init__(self, *args, **kwargs)

