import dateutil.parser
from datetime import datetime
from fractions import Fraction

from typing import Any
from typing import List
from typing import Tuple
from typing import Union
from typing import Callable

from fuse_core.core.etc import EMPTY_VALUE
from fuse_core.core.etc import LIMITLESS_ARRAY
from fuse_core.core.etc import DEFAULT_FROM_INPUT
from fuse_core.core.etc import EUROPEAN_DATE_FORMAT
from fuse_core.core.etc import DEFAULT_FLOAT_SEPARATORS
from fuse_core.core.etc import DEFAULT_ARRAY_SEPARATORS
from fuse_core.core.exceptions import HandlerError

from fuse_core.core.handlers import IHandler
from fuse_core.core.utils import get_separator
from fuse_core.core.exceptions import ArraySizeLimitError
from fuse_core.core.exceptions import ValidationError
from fuse_core.core.validators import IValidator


__all__ = ('Field', 'StringField', 'IntegerField',
           'FloatField', 'DateField', 'ArrayField',)


class Field:
    """
    Base field class
    """

    __slots__ = (
        '_value', '_name', '_verbose_name',
        '_null', '_default', '_skip_values',
        '_method', '_handlers', '_validators',
        '_raise_exception'
    )

    exceptions = (
        KeyError,
        ValueError,
        IndexError,
        RuntimeError,
        OverflowError,
        MemoryError,
    )

    def __init__(
        self,
        value: Any = EMPTY_VALUE(),
        *,
        name: str = None,
        verbose_name: str = None,
        null: bool = False,
        skip_values: List[Any] = None,
        default: Union[Any, DEFAULT_FROM_INPUT] = None,
        method: Callable = None,
        handlers: List[IHandler] = None,
        validators: List[IValidator] = None,
        raise_exception: bool = True
    ) -> None:
        self._value = value

        # Field code name
        self._name = name

        # Verbose name (f.e. we use it in `fuse.sheets`)
        self._verbose_name = verbose_name

        # Is value nullable
        self._null = null

        # Default value. Can be any type or `DEFAULT_FROM_INPUT()`
        self._default = default

        # List of values to skip
        self._skip_values = skip_values

        # Method must have only one parameter - `value`
        self._method = method

        # List of core with initial parameters
        self._handlers = handlers

        if self._method and self._handlers:
            raise AttributeError('using `method` and `handlers` together is not allowed')

        self._validators = validators

        # Raise exception or not
        self._raise_exception = raise_exception

    def validate(self, value: Any) -> Any:
        """
        Method that allows you to validate
        via list of `IValidator` based classes
        """
        for validator in self._validators:
            if not validator.validate(value):
                raise ValidationError

        return value

    def handle(self, value: str) -> Any:
        return value

    def set(self, value: Any = EMPTY_VALUE()) -> Any:
        """
        Method `set` validates data by validators, handlers and methods
        and then parse it via `Field` base objects by calling `handle` method in it

        Args:
            value (Any): Any value to handle. By default, it's `EMPTY_VALUE`
            that allows you to set value from `__init__` method
        """
        original_value = value
        if isinstance(value, EMPTY_VALUE):
            value = self._value

        try:
            if self._skip_values:
                if value in self._skip_values:
                    raise ValueError(f'Value "{value}" in skip list')

            if self._handlers:
                for handler in self._handlers:
                    value = handler.handle(value)

            if self._method:
                value = self._method(value)

            if self._validators:
                self.validate(value)

            try:
                value = self.handle(value)
            except self.exceptions as e:
                raise HandlerError(str(e))

            setattr(self, '_value', value)
            return value

        except self.exceptions as e:
            # To return value as it was passed
            # then you need to pass `default=DEFAULT_FROM_INPUT()`.
            # But remember, that result will be unpredictable in some way
            if not self._raise_exception:
                if isinstance(self.default, DEFAULT_FROM_INPUT):
                    setattr(self, '_value', original_value)
                    return original_value

                setattr(self, '_value', self._default)
                return self._default

            raise e

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def verbose_name(self):
        """ Verbose name (f.e. we use it in `fuse_sheets`) """
        return self._verbose_name

    @property
    def null(self):
        """ Is value can be nullable """
        return self._null

    @property
    def default(self):
        return self._default

    def __repr__(self):
        return f'({self.__class__.__name__}) ' \
               f'<id: {id(self)}, name: {self.name}, ' \
               f'verbose_name: {self.verbose_name}>'


class StringField(Field):
    """
    A very simple string field
    """

    def handle(self, value: str) -> Any:
        return str(value)


class IntegerField(Field):
    """
    A very simple integer field
    """

    def handle(self, value, *args, **kwargs):
        return int(value)


class FloatField(Field):
    """
    Float field.
    Supports separators, fractials
    """

    __slots__ = (
        'separators',
    )

    def __init__(
        self, *,
        separators: str = None,
        **kwargs
    ) -> None:
        self.separators = separators or DEFAULT_FLOAT_SEPARATORS
        super().__init__(**kwargs)

    def handle(self, value: str) -> Any:
        new_value = value
        separator = get_separator(self.separators, value)

        # Check for separator
        if separator:
            new_value = new_value.replace(separator, '.')

        # Check for fraction
        if '/' in new_value:
            new_value = float(sum(Fraction(s) for s in new_value.split()))

        return float(new_value)


class DateField(Field):

    def __init__(
        self, *,
        as_string: bool = False,
        out_date_format: str = EUROPEAN_DATE_FORMAT,
        date_attribute: str = None,
        **kwargs
    ) -> None:
        # Return `datetime` object as string
        self.as_string = as_string

        # Output date format
        self.out_date_format = out_date_format

        # Attribute from `datetime` object
        self.date_attribute = date_attribute

        super().__init__(**kwargs)

    def handle(self, value: str) -> datetime:
        try:
            if isinstance(value, str):
                new_value = dateutil.parser.parse(value, fuzzy=True)
            elif isinstance(value, (int, float)):
                new_value = datetime.fromtimestamp(value)
            elif isinstance(value, datetime):
                new_value = value

        except dateutil.parser.ParserError as e:
            raise e

        if self.date_attribute:
            new_value = getattr(new_value, self.date_attribute)()

        if self.as_string and self.out_date_format:
            try:
                return new_value.strftime(self.out_date_format)
            except (ValueError, OverflowError) as e:
                raise e

        if isinstance(self.date_attribute, str):
            if not hasattr(new_value, self.date_attribute):
                raise AttributeError(f'value doesn\'t have `{self.date_attribute}` attribute')

        return new_value


class ArrayField(Field):

    __slots__ = (
        'child_field', 'separators', 'size'
    )

    def __init__(
        self, *,
        child_field: Field,
        separators: Tuple[str] = None,
        size: Union[int, LIMITLESS_ARRAY] = LIMITLESS_ARRAY(),
        **kwargs
    ) -> None:

        # Instance of `Field` class
        self.child_field = child_field

        # List of separators
        self.separators = separators or DEFAULT_ARRAY_SEPARATORS

        # Array size limit
        self.size = size

        super().__init__(**kwargs)

    def _split_string(self, value) -> List[Any]:
        """ Split string by separator """
        separator = get_separator(self.separators, value)
        return value.split(separator)

    def _check_array_size(self, value) -> bool:
        """ Check array size, I guess """
        if isinstance(self.size, LIMITLESS_ARRAY):
            return True

        return len(value) >= self.size

    def _convert_values(self, values: List[Any]) -> List[Field]:
        """ Convert child field values """
        collect = []
        for value in values:
            self.child_field.set(value)
            collect.append(self.child_field.value)

        return collect

    def handle(self, value: str) -> Any:
        new_value = self._split_string(value)

        if not self._check_array_size(new_value):
            raise ArraySizeLimitError(f'array size ({self.size}) exceeded')

        new_value = self._convert_values(new_value)
        return new_value
