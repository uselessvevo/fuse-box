import abc
import re
from typing import Any, Iterable
from fusebox.core.exceptions import ValidationError


__all__ = (
    'EmailValidator',
    'MinLengthValidator',
    'MaxLengthValidator',
    'RangeValidator',
)


class IValidator:

    @abc.abstractmethod
    def validate(self, value: Any):
        pass


class MinLengthValidator(IValidator):

    def __init__(self, min_length: int) -> None:
        self._min_length = min_length

    def validate(self, value: Iterable):
        if not hasattr(value, '__iter__'):
            raise ValidationError('Value is not iterable', 'type_error')

        if not self._min_length > len(value):
            raise ValidationError('Value is less than min length')


class MaxLengthValidator(IValidator):

    def __init__(self, max_length: int) -> None:
        self._max_length = max_length

    def validate(self, value: Iterable):
        if not hasattr(value, '__iter__'):
            raise ValidationError('Value is not iterable', 'type_error')

        if not self._max_length < len(value):
            raise ValidationError('Value is bigger than max length')


class RangeValidator(IValidator):

    def __init__(self, min_val: int, max_val: int) -> None:
        self._min_val = min_val
        self._max_val = max_val

    def validate(self, value: Any):
        if value not in range(self._min_val, self._max_val):
            raise ValidationError('Value is out of range')


class RegexValidator(IValidator):

    def __init__(self, regex: str) -> None:
        self._regex = regex

    def validate(self, value: Any):
        try:
            if not re.match(self._regex, value):
                raise ValidationError(f'Cant parse given regular expression with value {value}', 'regex_error')

        except re.error:
            raise ValidationError('Cant parse given regular expression', 'regex_error')


EmailValidator = RegexValidator(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
