import abc
import re
from typing import Any
from collections import Iterable

from fuse_core.core.exceptions import RegexError


__all__ = (
    'EmailValidator',
    'MinLengthValidator',
    'MaxLengthValidator',
    'RangeValidator',
)


class IValidator:

    @abc.abstractmethod
    def validate(self, value: Any) -> bool:
        pass


class MinLengthValidator(IValidator):

    def __init__(self, min_length: int) -> None:
        self._min_length = min_length

    def validate(self, value: Iterable) -> bool:
        if hasattr(value, '__iter__'):
            return self._min_length > len(value)
        raise TypeError('value is not iterable')


class MaxLengthValidator(IValidator):

    def __init__(self, max_length: int) -> None:
        self._max_length = max_length

    def validate(self, value: Iterable) -> bool:
        if hasattr(value, '__iter__'):
            return self._max_length < len(value)
        raise TypeError('value is not iterable')


class RangeValidator(IValidator):

    def __init__(self, min_val: int, max_val: int) -> None:
        self._min_val = min_val
        self._max_val = max_val

    def validate(self, value: Any) -> bool:
        return self._min_val >= value <= self._max_val


class RegexValidator(IValidator):

    def __init__(self, regex: str) -> None:
        self._regex = regex

    def validate(self, value: Any) -> bool:
        try:
            if re.match(self._regex, value):
                return True
            return False

        except RegexError:
            raise ValueError('can\'t parse given regex')


EmailValidator = RegexValidator(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
