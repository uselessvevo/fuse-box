"""
Main exceptions
"""


__all__ = (
    'ArraySizeLimitError',
    'ValueValidationError',
    'RegexGroupNotFoundError',
)


class ValueValidationError(ValueError):
    pass


class RegexGroupNotFoundError(ValueError):
    pass


class ArraySizeLimitError(ValueError):
    pass
