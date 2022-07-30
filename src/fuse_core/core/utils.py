"""
Useful utils
"""


__all__ = (
    'get_separator',
)


def get_separator(separators, string):
    """ Method that returns needed separator from string"""
    if isinstance(string, str):
        for separator in separators:
            if separator in string:
                return separator
