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
