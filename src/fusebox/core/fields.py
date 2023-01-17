import dateutil.parser
from datetime import datetime
from fractions import Fraction

from typing import Any
from typing import List
from typing import Tuple
from typing import Union
from typing import Callable

from fusebox.core.etc import EMPTY_VALUE
from fusebox.core.etc import LIMITLESS_ARRAY
from fusebox.core.etc import DEFAULT_FROM_INPUT
from fusebox.core.etc import EUROPEAN_DATE_FORMAT
from fusebox.core.etc import DEFAULT_FLOAT_SEPARATORS
from fusebox.core.etc import DEFAULT_ARRAY_SEPARATORS
from fusebox.core.exceptions import HandlerError, FieldNotReadyError, NullValueError, SkipValueError

from fusebox.core.handlers import IHandler
from fusebox.core.utils import get_separator
from fusebox.core.exceptions import ArraySizeLimitError
from fusebox.core.validators import IValidator


__all__ = ('Field', 'StringField', 'IntegerField',
           'FloatField', 'DateField', 'ArrayField',)


class Field:
    """
    Base field class
    """

    __add_slots__: list[str] = None

    __slots__: list[str] = [
        '_value', '_name', '_verbose_name',
        '_null', '_default', '_skip_values',
        '_method', '_handlers', '_validators',
        '_raise_exception', '_check_type', '_ready',
    ]

    allowed_types: tuple[Any] = None

    exceptions: tuple[Exception] = (
        KeyError,
        ValueError,
        IndexError,
        RuntimeError,
        OverflowError,
        MemoryError,
    )

    @classmethod
    def __new__(cls, *args, **kwargs):
        if isinstance(cls.__add_slots__, (list, tuple)):
            cls.__slots__.extend(cls.__add_slots__)

        return super().__new__(cls)

    def __init__(
        self,
        value: Union[Any, EMPTY_VALUE] = EMPTY_VALUE(),
        *,
        name: str = None,
        verbose_name: str = None,
        skip_values: List[Any] = None,
        default: Union[Any, DEFAULT_FROM_INPUT] = None,
        method: Callable = None,
        handlers: List[IHandler] = None,
        validators: List[IValidator] = None,
        null: bool = False,
        check_type: bool = False,
        raise_exception: bool = True,
    ) -> None:

        # Main attributes #

        # Field's value
        self._value = value

        # Field code name
        self._name = name

        # Verbose name (f.e. we use it in `fuse.sheets`)
        self._verbose_name = verbose_name

        # Default value. Can be any type or `DEFAULT_FROM_INPUT()`
        self._default = default

        # List of skippable values
        self._skip_values = skip_values

        # Flags #

        # Check if method `set` has not been called
        self._ready: bool = False

        # Is value nullable
        self._null = null

        # Check input value/data type by `allowed_types`
        self._check_type = check_type

        # Raise exception or not
        self._raise_exception = raise_exception

        # Handlers, methods and validators #

        # Method (see tests/test_fields.py)
        self._method = method

        # List of handlers (see core/handlers.py)
        self._handlers = handlers

        if self._method and self._handlers:
            raise AttributeError('using `method` and `handlers` together is not allowed')

        # List of validators (see core/validators.py)
        self._validators = validators

    def validate(self, value: Any) -> Any:
        """
        Calls all validators

        Returns:
              is_valid (bool): is value passed all validators
        """
        for validator in self._validators:
            try:
                validator.validate(value)
            except Exception as e:
                raise e

    def handle(self, value: Any) -> Any:
        for handler in self._handlers:
            value = handler.handle(value)

        return value

    def process(self, value: Any) -> Any:
        return value

    def set(self, value: Any = EMPTY_VALUE()) -> Any:
        """
        Method `set` does everything:
        * Does basic checks
        * Calls validators, handlers and method `handle`
        * Sets final, validated and handled value as field's attribute

        Args:
            value (Any): Any value to handle. By default, it's `EMPTY_VALUE`
            that allows you to set value from `__init__` method
        """
        original_value = value

        if isinstance(value, EMPTY_VALUE):
            value = self._value

        try:
            # First, check if value can be nullable
            if not self._null and value is None:
                raise NullValueError

            # Then check if value in skippables
            if self._skip_values:
                if value in self._skip_values:
                    raise SkipValueError

            # Handle by handlers objects
            if self._handlers:
                value = self.handle(value)

            # Handle by method
            if self._method:
                value = self._method(value)

            # And now we need to call method `process`
            try:
                value = self.process(value)
            except self.exceptions as e:
                raise HandlerError(str(e))

            # Then we need to validate finalized data

            if self._validators:
                self.validate(value)

            if self._check_type and hasattr(self, 'allowed_types'):
                if value in self.allowed_types:
                    raise TypeError(f'Type `{type(value)}` is not allowed in {self.__class__.__name__}')

            # Final preparations

            self._ready = True
            self._value = value
            return value

        except self.exceptions as e:
            # To return value as it was passed
            # then you need to pass `default=DEFAULT_FROM_INPUT()`.
            # But remember, that result will be unpredictable in some way
            if not self._raise_exception:
                self._ready = True
                if isinstance(self._default, DEFAULT_FROM_INPUT):
                    self._value = original_value
                    return original_value

                self._value = self._default
                return self._default

            raise e

    @property
    def value(self):
        if self._ready is True:
            return self._value
        raise FieldNotReadyError()

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
    def default(self):
        return self._default

    def __repr__(self):
        return f'{self.__class__.__name__} <id: {id(self)}, name: {self._name}, value: {self._value}>'


class StringField(Field):
    """
    A very simple string field
    """
    __add_slots__ = ['_min_length', '_max_length']

    def __init__(
        self, *,
        min_length: int = None,
        max_length: int = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._min_length = min_length
        self._max_length = max_length

    def process(self, value: str) -> Union[str, None]:
        if self._min_length:
            if len(value) < self._min_length:
                raise ValueError('String length is less then min value')

        if self._max_length:
            if len(value) > self._max_length:
                raise ValueError('String length is bigger then max value')

        if value is None:
            return

        return str(value)


class IntegerField(Field):
    """
    A very simple integer field
    """

    def process(self, value, *args, **kwargs) -> Union[int, None]:
        if value is None:
            return

        return int(value)


class FloatField(Field):
    """
    Float field.
    Supports separators, fractials
    """

    __add_slots__ = (
        'separators',
    )

    def __init__(
        self, *,
        separators: str = None,
        **kwargs
    ) -> None:
        self.separators = separators or DEFAULT_FLOAT_SEPARATORS
        super().__init__(**kwargs)

    def process(self, value: str) -> Union[float, None]:
        if value is None:
            return

        new_value = value
        separator = get_separator(self.separators, new_value)

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

    def process(self, value: str) -> Union[datetime, None]:
        if value is None:
            return

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

    __add_slots__ = (
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

    def process(self, value: str) -> Any:
        if value is None:
            return

        new_value = self._split_string(value)

        if not self._check_array_size(new_value):
            raise ArraySizeLimitError(f'array size ({self.size}) exceeded')

        new_value = self._convert_values(new_value)
        return new_value
