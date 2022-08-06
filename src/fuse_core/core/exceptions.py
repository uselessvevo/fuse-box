"""
Main exceptions
"""


__all__ = (
    'ArraySizeLimitError',
    'ValueValidationError',
    'RegexError',
)


class ValueValidationError(ValueError):
    pass


class RegexError(ValueError):
    pass


class ArraySizeLimitError(ValueError):
    pass
