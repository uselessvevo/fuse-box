import json
from typing import Any
from collections import OrderedDict

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

    def set(self, key: str, value: Any) -> None:
        """ Call Field's `set` method """
        self.__container[key].set(value)

    def get(self, key: str, default: Any = None) -> Any:
        """ Get value from `Field` instance """
        result = self.get_field(key, 'value', default)
        if result is None:
            raise KeyError(f'field "{key}" not found')
        return result

    def pop(self, key, default=None):
        self.__container.pop(key, default)

    def get_field(
        self,
        key: str,
        attr: str,
        default: Any = None,
    ) -> Any:
        """ Get any available attribute from `Field` class """
        result = self.__container.get(key, default)
        if result is not None:
            return getattr(result, attr, default)
        return result

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

    def to_dict(self, *keys, full_house: bool = True) -> dict:
        if full_house:
            keys = self.__container.keys()

        return {
            self.get_field(k, 'name'): self.get_field(k, 'value') for k in keys
        }

    def to_json(self, *keys, full_house: bool = True) -> str:
        """
        Convert dict to json

        Args:
            keys (tuple):
            full_house (bool): return all keys
        """
        return json.dumps(self.to_dict(*keys, full_house=full_house))

    def keys(self):
        return self.__container.keys()

    def values(self):
        return self.__container.values()

    def items(self):
        return self.__container.items()

    def __repr__(self):
        keys = ', '.join(tuple(self.__container.keys())[:3])
        return f'{self.__class__.__name__} <id: {id(self)}, keys: {keys}... (keys were truncated)>'
