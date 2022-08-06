"""
Main exceptions
"""


__all__ = (
    'ArraySizeLimitError',
    'ValidationError',
    'RegexError',
)


class ValidationError(ValueError):
    pass


class RegexError(ValueError):
    pass


class ArraySizeLimitError(ValueError):
    pass
