import abc
import re
from typing import Any, Iterable

__all__ = (
    'MinLengthValidator',
    'MaxLengthValidator'
)


class IValidator:

    @abc.abstractmethod
    def validate(self, value: Any) -> bool:
        pass


class MinLengthValidator(IValidator):

    def __init__(self, min_length: int) -> None:
        self._min_length = min_length

    def validate(self, value: Iterable) -> bool:
        if isinstance(value, Iterable):
            return self._min_length > len(value)
        raise TypeError('value is not iterable')


class MaxLengthValidator(IValidator):

    def __init__(self, max_length: int) -> None:
        self._max_length = max_length

    def validate(self, value: Iterable) -> bool:
        if isinstance(value, Iterable):
            return self._max_length < len(value)
        raise TypeError('value is not iterable')


class EmailValidator(IValidator):

    def validate(self, value: Any) -> bool:
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        try:
            if re.match(regex, value):
                return True
            return False

        except Exception:
            raise ValueError('can\'t parse email address')
