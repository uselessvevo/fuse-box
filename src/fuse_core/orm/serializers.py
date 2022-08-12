from typing import Union

from fuse_core.core.fields import Field
from fuse_core.core.containers import FieldDictionary


__all__ = (
    'Serializer',
)


class Serializer:
    """
    Simple SQLAlchemy query serializer.
    Inspired by DRF's serializers

    Example:
    >>> from fuse_core.core.fields import *
    >>> from fuse_core.core.validators import *
    >>> from fuse_core.orm.serializers import *

    >>>    class UserSerializer(Serializer):
    >>>        id = IntegerField()
    >>>        email = StringField()
    >>>        first_name = StringField()
    >>>        second_name = StringField()
    >>>        middle_name = StringField()
    >>>
    >>>
    >>>    class UserCreateSerializer(Serializer):
    >>>        email = StringField(validators=[EmailValidator()])
    >>>        first_name = StringField(validators=[MinLengthValidator(1)])
    >>>        second_name = StringField(validators=[MaxLengthValidator(125)])
    >>>        middle_name = StringField(validators=[MinLengthValidator(1)])
    >>>        email = StringField(validators=[EmailValidator()])

    >>> user_info = UserSerializer(query, as_field_dict=True)
    >>> result = user_info.result(to_dict=True)
    >>> {
    >>>     "id": "e935114c-e810-4c83-bee2-2519d48f87e8",
    >>>     "email": "",
    >>>     "firstname": "Cyrill",
    >>>     "patronymic": None,
    >>>     "username": "cyrill.ivanov.1488",
    >>>     "lastname": "Ivanov"
    >>> }
    """

    @classmethod
    def __new__(cls, *args, **kwargs):
        cls.prepare_fields()
        return super().__new__(cls)

    def __init__(
        self,
        entity,
        many: bool = False,
        as_field_dict: bool = False,
        raise_exception: bool = True
    ):
        # Main attributes
        self._entity = entity
        self._many = many

        # Flags

        self._is_valid = None
        self._raise_exception = raise_exception
        self._as_field_dict = as_field_dict

    @classmethod
    def prepare_fields(cls):
        fields: list[Field] = []
        for name, field in cls.__dict__.items():
            if isinstance(field, Field):
                if field.name is None:
                    field.name = name
                fields.append(field)

        cls._fields = {f.name: f for f in fields}

    # Pre-serialization methods

    def get_entity_dict(self, entity) -> dict:
        """
        Get dict from entity

        Args:
            entity (object):
        """
        entity_dict = {}
        if hasattr(entity, '__values__'):
            entity_dict = entity.__values__

        elif hasattr(entity, '_sa_instance_state'):
            entity_dict = entity._sa_instance_state.dict

        entity_dict = {k: v for (k, v) in entity_dict.items() if k in self._fields.keys()}

        if entity_dict:
            return entity_dict

        raise ValueError('Entity dict is empty or doesnt contain needed attributes')

    def handle(self, entity, to_dict: bool = False) -> Union[dict, FieldDictionary]:
        """
        Main entrypoint

        Arguments:
            to_dict (bool): convert `FieldDictionary (-s)` to dict
        """
        try:
            if self._as_field_dict:
                field_dict = FieldDictionary()
            else:
                field_dict = {}

            entity_dict = self.get_entity_dict(entity)

            for key, value in entity_dict.items():
                field: Field = self._fields.get(key)
                field.set(value)

                if self._as_field_dict:
                    field_dict[field.name] = field
                else:
                    field_dict[field.name] = field.value

            if to_dict:
                return field_dict.to_dict(full_house=True)

        except Exception as e:
            self._is_valid = False
            if self._raise_exception:
                raise e

    def result(self, **kwargs):
        if self._many:
            return [self.handle(i, **kwargs) for i in self._entity]
        return self.handle(self._entity, **kwargs)

    def __repr__(self):
        return f'({self.__class__.__name__}) <id: {id(self)}>'
