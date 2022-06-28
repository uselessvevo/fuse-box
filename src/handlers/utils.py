"""
Useful utils
"""


def get_separator(separators, string):
    """ Метод для получения разделителя строки """
    if isinstance(string, str):
        for separator in separators:
            if separator in string:
                return separator
