"""
Main exceptions
"""

__all__ = (
    'ArraySizeLimitError',
    'RegexError',
    'HandlerError',
)


class FieldNotReadyError(Exception):
    """ Raise an error if the method has not been called"""


class HandlerError(Exception):

    def __init__(self, message: str = None):
        self._message = message

    def __str__(self):
        return self._message


class RegexError(ValueError):
    pass


class ArraySizeLimitError(ValueError):
    pass


class NullValueError(ValueError):

    def __str__(self):
        return 'Value cant be nullable'


class SkipValueError(ValueError):

    def __str__(self):
        return 'Value in skip list'


class ValidationError(ValueError):

    def __init__(
        self,
        message: str = 'Validation error',
        code_name: str = 'validation_error',
        detailed_exception: bool = False
    ) -> None:
        self._message = message
        self._code_name = code_name
        self._detailed_exception = detailed_exception

    def __str__(self):
        return self._message

    @property
    def error(self):
        if self._detailed_exception:
            return {'message': self._message, 'code_name': self._code_name}
        return self._message
