from typing import Any, List
from collections import OrderedDict


__all__ = (
    'FuseDictionary',
)


class FuseDictionary:
    """
    Контейнер для `Field`
    """

    __slots__ = (
        '__container',
    )

    def __init__(self):
        self.__container = OrderedDict({})

    def __setitem__(self, key, value):
        self.__container[key] = value

    def __getitem__(self, item):
        return self.__container[item]

    def __delitem__(self, key):
        del self.__container[key]

    def pop(self, key, default=None):
        self.__container.pop(key, default)

    def field(
        self,
        key: str,
        default: Any = None,
        attr: str = None
    ) -> List[Any]:
        result = self.__container.get(key, default)
        if result and attr:
            return getattr(result, attr or 'value', default)
        return result

    def set(self, key: str, value: Any) -> None:
        self.__container[key].value = value

    def get(self, key: str, default: Any = None) -> Any:
        res = self.__container.get(key)
        if res is not None:
            if res.value is None:
                return default
            else:
                return res.value
        raise KeyError(f'Key "{key}" not found')

    def get_values(self, *keys, attr: str = 'value', full_house: bool = False) -> List[Any]:
        """
        Method that returns values (value attr) by given keys
        Args:
            keys (tuple):
            attr (str): get needed attribute from `Field` based class
            full_house (bool): return all keys
        """
        keys = keys if not full_house else tuple(self.__container.keys())
        return [self.get(k) for k in keys]

    def get_items(
        self,
        *keys,
        attr: str = 'value',
        full_house: bool = True
    ) -> dict:
        """
        Method that returns dictionary by given keys
        Args:
            keys (tuple):
            attr (str): get needed attribute from `Field` based class
            full_house (bool): return all keys
        """
        if full_house and not keys:
            keys = self.__container.keys()

        return {
            getattr(self.field(k), 'name', None): getattr(self.field(k), attr or 'value', None)
            for k in keys
        }

    @property
    def container(self):
        return self.__container
