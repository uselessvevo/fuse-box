from typing import Union, Any, Iterable

from fuse_core.core.fields import Field
from fuse_core.core.containers import FieldContainer


__all__ = (
    'Serializer',
    'ModelSerializer',
)


class BaseSerializer:

    def __init__(
        self, *,
        as_field_dict: bool = False,
        raise_exception: bool = True,
        only: tuple[str, ...] = None,
        exclude: tuple[str, ...] = None
    ):
        # Main preparations
        self._prepare_fields(only, exclude)

        # Flags

        self._is_valid = None
        self._raise_exception = raise_exception
        self._as_field_dict = as_field_dict

    def _prepare_fields(
        self,
        only: tuple[str] = None,
        exclude: tuple[str] = None
    ):
        if only and exclude:
            raise AttributeError('cant use `only` and `exclude` together')

        class_attrs_dict: dict = self.__class__.__dict__

        if exclude:
            class_attrs_dict = {k: v for (k, v) in class_attrs_dict.items() if k not in exclude}

        elif only:
            class_attrs_dict = {k: v for (k, v) in class_attrs_dict.items() if k in only}

        fields: list[Field] = []
        for name, field in class_attrs_dict.items():
            if isinstance(field, Field):
                if field.name is None:
                    field.name = name

                fields.append(field)

        self._fields = {f.name: f for f in fields}

    def __repr__(self):
        return f'({self.__class__.__name__}) <id: {id(self)}>'


class ModelSerializer(BaseSerializer):
    """
    Simple SQLAlchemy query serializer.
    Inspired by DRF's serializers

    Example:
        >>> from fuse_core.core.fields import *
        >>> from fuse_core.core.validators import *
        >>> from fuse_core.orm.serializers import *

        >>>    class UserModelSerializer(ModelSerializer):
        >>>        class Meta:
        >>>                model = User
        >>>                fields = ('id', 'username', 'firstname', 'lastname')
        >>>
        >>>

        >>> user_info = UserModelSerializer(session.query(User).first(), as_field_dict=True)
        >>> result = user_info.handle(as_dict=True)
        >>> {
        >>>     "id": "e935114c-e810-4c83-bee2-2519d48f87e8",
        >>>     "username": "cyrill.ivanov.1337",
        >>>     "firstname": "Cyrill",
        >>>     "lastname": "Ivanov"
        >>> }
    """

    def __init__(
        self,
        model: Union[Iterable[object], object] = None,
        data: Union[Iterable[dict], dict] = None,
        many: bool = False,
        **kwargs,
    ):
        self._model = model
        self._many = many
        self._data = data

        super().__init__(**kwargs)

    # Pre-serialization methods

    def _get_model_dict(self, model) -> dict:
        """
        Get dict from model

        Args:
            model (object):
        """
        model_attr_dict = {}
        if hasattr(model, '__values__'):
            model_attr_dict = model.__values__

        elif hasattr(model, '_sa_instance_state'):
            model_attr_dict = model._sa_instance_state.dict

        model_attr_dict = {k: v for (k, v) in model_attr_dict.items() if k in self._fields.keys()}

        if model_attr_dict:
            return model_attr_dict

        raise ValueError('Model attrs dict is empty'
                         ' or doesnt contain needed attributes')

    def _handle_model(self, model, as_dict: bool = False) -> Union[dict, FieldContainer]:
        """
        Main entrypoint

        Arguments:
            as_dict (bool): convert `FieldContainer (-s)` to dict
        """
        try:
            if self._as_field_dict:
                field_dict = FieldContainer()
            else:
                field_dict = {}

            model_attr_dict = self._get_model_dict(model)

            for key, value in model_attr_dict.items():
                field: Field = self._fields.get(key)
                field.set(value)

                if self._as_field_dict:
                    field_dict[field.name] = field
                else:
                    field_dict[field.name] = field.value

            if as_dict and isinstance(field_dict, FieldContainer):
                return field_dict.as_dict(full_house=True)

            return field_dict

        except Exception as e:
            self._is_valid = False
            if self._raise_exception:
                raise e

    def handle(self, **kwargs):
        if self._many:
            return [self._handle_model(i, **kwargs) for i in self._model]
        return self._handle_model(self._model, **kwargs)

    def create(self):
        raise NotImplementedError('Method `create` must be implemented')

    def update(self):
        raise NotImplementedError('Method `update` must be implemented')


class Serializer(BaseSerializer):

    def __init__(
        self, *,
        data: Union[dict, Iterable[dict]] = None,
        **kwargs
    ):
        self._data = data
        super().__init__(**kwargs)

    def _handle_data(
        self,
        data: Union[Iterable[dict], dict],
        as_dict: bool = False
    ) -> Union[dict, FieldContainer]:
        """
        Main entrypoint

        Arguments:
            as_dict (bool): convert `FieldContainer (-s)` to dict
        """
        try:
            if self._as_field_dict:
                field_dict = FieldContainer()
            else:
                field_dict = {}

            for field_name, field_inst in self._fields.items():
                if field_inst.required and not data.get(field_name):
                    raise KeyError(f'Input data doesnt contain field {field_name}'
                                   f' ({field_inst.__class__.__name__})')

            for key, value in data.items():
                field: Field = self._fields.get(key)
                if field.required is True and key not in self._fields:
                    raise KeyError

                field.set(value)

                if self._as_field_dict:
                    field_dict[field.name] = field
                else:
                    field_dict[field.name] = field.value

            if as_dict and isinstance(field_dict, FieldContainer):
                return field_dict.as_dict(full_house=True)

            return field_dict

        except Exception as e:
            self._is_valid = False
            if self._raise_exception:
                raise e

    def handle(self, **kwargs):
        if isinstance(self._data, (tuple, list)):
            return [self._handle_data(i, **kwargs) for i in self._data]
        return self._handle_data(self._data, **kwargs)
