import json
from typing import Any
from collections import OrderedDict

from fuse_core.core.etc import RAW_FIELDS
from fuse_core.core.fields import Field


__all__ = (
    'FieldContainer',
)


class FieldContainer:

    __slots__ = (
        '__container',
    )

    def __init__(self):
        self.__container = OrderedDict({})

    def __setitem__(self, key, field: Field):
        if not isinstance(field, Field):
            raise TypeError('argument field must be `Field` based class')
        self.__container[key] = field

    def __getitem__(self, item):
        return self.__container[item]

    def __delitem__(self, key):
        self.__container.pop(key)

    def get_field(
        self,
        key: str,
        attr: str,
        default: Any = None,
    ) -> Any:
        """ Get instance or attribute from `Field` """
        field = self.__container.get(key, default)
        if field is not None:
            # Return `Field` instance
            if isinstance(attr, RAW_FIELDS):
                return field

            # Return attribute from `Field` instance.
            # Default is `value`
            return getattr(field, attr, default)

        raise AttributeError(f'Field `{key}` not found')

    def set(self, key: str, value: Any) -> None:
        """ Set value by calling field's `set` method """
        self.__container[key].set(value)

    def get(
        self,
        key: str,
        attr: str = 'value',
        default: Any = None
    ) -> Any:
        """ Get value from `Field` instance """
        result = self.get_field(key, attr, default)
        if result is None:
            raise KeyError(f'field "{key}" not found')
        return result

    def pop(self, key, default=None):
        """ Delete key/field from container """
        self.__container.pop(key, default)

    def get_items(
        self,
        *keys,
        attr: str = 'value',
        full_house: bool = True
    ) -> dict:
        """
        Return dictionary by given keys
        Args:
            keys (tuple):
            attr (str): get needed attribute from `Field` based class
            full_house (bool): return all keys
        """
        if full_house:
            keys = self.__container.keys()

        return {
            self.get_field(k, 'name'): self.get_field(k, attr) for k in keys
        }

    def as_dict(self, *keys, full_house: bool = True) -> dict:
        if full_house:
            keys = self.__container.keys()

        return {
            self.get_field(k, 'name'): self.get_field(k, 'value') for k in keys
        }

    def as_json(self, *keys, full_house: bool = True) -> str:
        """
        Convert dict to json
        Args:
            keys (tuple):
            full_house (bool): return all keys
        """
        return json.dumps(self.as_dict(*keys, full_house=full_house))

    def keys(self):
        return self.__container.keys()

    def values(self):
        return self.__container.values()

    def items(self):
        return self.__container.items()

    def __repr__(self):
        keys = ', '.join(tuple(self.__container.keys())[:3])
        return f'{self.__class__.__name__} <id: {id(self)}, keys: {keys}... (truncated)>'
