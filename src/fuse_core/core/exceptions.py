"""
Main exceptions
"""


__all__ = (
    'ArraySizeLimitError',
    'ValidationError',
    'RegexError',
    'HandlerError',
)


class HandlerError(Exception):

    def __init__(self, message: str = None):
        self._message = message

    def __str__(self):
        return self._message


class ValidationError(ValueError):
    pass


class RegexError(ValueError):
    pass


class ArraySizeLimitError(ValueError):
    pass
