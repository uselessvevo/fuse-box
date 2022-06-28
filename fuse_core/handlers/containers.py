from typing import Any, Union, List
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
        """
        Метод для задания значения поля `value`
        """
        self.__container[key].value = value

    def get(self, key: str, default: Any = None) -> Any:
        res = self.__container.get(key)
        if res is not None:
            if res.value is None:
                return default
            else:
                return res.value
        raise KeyError(f'Key "{key}" not found')

    def get_values(self, *keys, full_house: bool = False) -> List[Any]:
        """
        Метод для получения значений (атрибут - values) по переданным полям
        Args:
            keys (tuple): наименования (ключи) полей
            full_house (bool): получить все ключи
        """

        keys = keys if not full_house else tuple(self.__container.keys())
        return [self.get(k) for k in keys]

    def get_fields(
        self,
        *keys, attr: str = None,
        raw: bool = False,
        full_house: bool = False
    ) -> Union[List[Any]]:
        """
        Метод для получения полей (экземпляров)
        Args:
            keys (tuple): наименования (ключи) полей
            attr (str): нужный атрибут поля
            raw (bool): вернуть объект
            full_house (bool): получить все ключи
        """

        keys = keys if not full_house else tuple(self.__container.keys())
        items = [getattr(self.field(k), attr or 'value', None) if not raw else self.field(k) for k in keys]
        return [i for i in items if i]

    def get_items(
        self,
        *fields,
        field_name: str = None,
        full_house: bool = True
    ) -> dict:
        """
        Метод для получения словаря.
        В качестве значений передаётся `slave_attr` (к примеру - `value`)
        Args:
            fields (tuple): наименования (ключи) полей
            field_name (str): нужный атрибут поля
            full_house (bool): получить все ключи
        """

        if full_house and not fields:
            fields = self.__container.keys()

        if not field_name:
            field_name = 'value'

        return {
            getattr(self.field(k), 'name', None): getattr(self.field(k), field_name or 'value', None)
            for k in fields
        }

    @property
    def container(self):
        return self.__container
