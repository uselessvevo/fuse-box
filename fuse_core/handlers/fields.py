import dateutil.parser
from datetime import datetime
from fractions import Fraction

from typing import Any
from typing import List
from typing import Tuple
from typing import Union
from typing import Callable

from fuse_core.handlers.config import DEFAULT_AS_INPUT
from fuse_core.handlers.config import ARRAY_NO_SIZE_LIMITS
from fuse_core.handlers.config import DATETIME_ATTRIBUTE
from fuse_core.handlers.config import EUROPEAN_DATE_FORMAT
from fuse_core.handlers.config import DEFAULT_FLOAT_SEPARATORS
from fuse_core.handlers.config import DEFAULT_ARRAY_SEPARATORS

from fuse_core.handlers.handlers import IHandler
from fuse_core.handlers.utils import get_separator
from fuse_core.handlers.exceptions import ArraySizeLimitError
from fuse_core.handlers.exceptions import ValueValidationError
from fuse_core.orm.validators import IValidator


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
        OverflowError
    )

    def __init__(
        self, *,
        name: str = None,
        verbose_name: str = None,
        null: bool = False,
        skip_values: List[Any] = None,
        default: Union[Any, DEFAULT_AS_INPUT] = None,
        method: Callable = None,
        handlers: List[IHandler] = None,
        validators: List[IValidator] = None,
        raise_exception: bool = True
    ) -> None:
        self._raise_exception = raise_exception
        self._value: Any = None

        # Field code name
        self._name = name

        # Verbose name (f.e. we use it in `fuse.sheets`)
        self._verbose_name = verbose_name

        # Is value nullable
        self._null = null

        self._default = default
        self._skip_values = skip_values or tuple()

        # method with only one parameter `value`
        self._method = method

        # List of handlers with initial parameters
        self._handlers = handlers or tuple()

        if self.method and self.handlers:
            raise AttributeError('using `method` and `handlers` together is not allowed')

        self._validators = validators or tuple()

    def validate(self, value: Any) -> Any:
        """
        Method that allows you to validate
        via list of `IValidator` based classes
        """
        for validator in self._validators:
            if not validator.validate(value):
                raise ValueValidationError

        return value

    def handle(self, value: str) -> Any:
        return value

    def set(self, value, *args, **kwargs):
        try:
            if value in self.skip_values:
                raise ValueError(f'Value "{value}" in skip list')

            for handler in self.handlers:
                value = handler.handle(value)

            if self.method:
                value = self.method(value)

            try:
                value = self.handle(value)
            except Exception as e:
                if self._raise_exception:
                    raise e

            return value

        except self.exceptions as e:
            if isinstance(self.default, DEFAULT_AS_INPUT):
                self._value = value
            raise e

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Verbose name (f.e. we use it in `fuse.sheets`)
    @property
    def verbose_name(self):
        return self._verbose_name

    @verbose_name.setter
    def verbose_name(self, value):
        self._verbose_name = value

    # Is value nullable
    @property
    def null(self):
        return self._null

    @null.setter
    def null(self, value):
        self._null = value

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    @property
    def skip_values(self):
        return self._skip_values

    @skip_values.setter
    def skip_values(self, value):
        self._skip_values = value

    # method with only one parameter `value`
    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    # List of handlers with initial parameters
    @property
    def handlers(self):
        return self._handlers

    @handlers.setter
    def handlers(self, value):
        self._handlers = value

    def __repr__(self):
        return f'({self.__class__.__name__}) ' \
               f'<id: {id(self)}, name: {self.name}, ' \
               f'verbose_name: {self.verbose_name}, value: {self._value}>'


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

        # Check if we've got a separator
        if separator:
            new_value = new_value.replace(separator, '.')

        # Check if value is fraction
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
        self.date_attribute = date_attribute or DATETIME_ATTRIBUTE

        super().__init__(**kwargs)

    def handle(self, value: str) -> datetime:
        try:
            new_value = dateutil.parser.parse(value, fuzzy=True)
        except dateutil.parser.ParserError as e:
            raise e

        new_value = getattr(new_value, self.date_attribute)()
        if self.as_string:
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
        size: Union[int, ARRAY_NO_SIZE_LIMITS] = ARRAY_NO_SIZE_LIMITS(),
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
        if isinstance(self.size, ARRAY_NO_SIZE_LIMITS):
            return True

        return len(value) >= self.size

    def _convert_values(self, value: List[Any]) -> List[Field]:
        """ Convert child field values """
        return [self.child_field.set(v) for v in value]

    def handle(self, value: str) -> Any:
        new_value = self._split_string(value)

        if not self._check_array_size(new_value):
            raise ArraySizeLimitError(f'array size ({self.size}) exceeded')

        new_value = self._convert_values(new_value)
        return new_value
