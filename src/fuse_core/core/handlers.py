import re
from abc import ABC, abstractmethod
from typing import Any, List, Union

from core.etc import INDEX_ALL, DEFAULT_REGEX_INDEX
from core.exceptions import RegexGroupNotFoundError


__all__ = (
    'IHandler',
    'Mapper',
    'Regex',
)


class IHandler(ABC):

    @abstractmethod
    def handle(self, value, *args, **kwargs) -> Any:
        pass


class Mapper(IHandler):
    """
    Handful mapper (dict/hashmap)
    """

    def __init__(
        self,
        mapping: dict,
        default: Any = None,
        ignore_case: bool = False
    ) -> None:
        self._mapping = mapping
        self._default = default
        self._ignore_case = ignore_case

    def handle(self, value, *args, **kwargs) -> Any:
        if self._ignore_case:
            value = value.lower()
            self._mapping = {k.lower(): v for (k, v) in self._mapping.items()}

        return self._mapping.get(value, self._default)


class Regex(IHandler):

    def __init__(
        self,
        regex: str,
        default: Any = None,
        index: Union[int, INDEX_ALL] = DEFAULT_REGEX_INDEX
    ) -> None:
        self._regex = regex
        self._default = default
        self._index = index

    def handle(self, value, *args, **kwargs) -> Union[str, List[str]]:
        new_value = re.search(self._regex, value)

        if not new_value:
            raise RegexGroupNotFoundError

        if isinstance(self._index, int):
            return new_value.group(self._index)

        elif isinstance(self._index, INDEX_ALL):
            return list(new_value.groups())
