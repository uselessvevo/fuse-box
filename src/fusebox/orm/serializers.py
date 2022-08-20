from typing import Union, Iterable

from fusebox.orm.exceptions import UndeclaredField
from fusebox.orm.fields import Field
from fusebox.core.containers import FieldContainer
from fusebox.orm import fields as fields_mod


__all__ = (
    'Serializer',
    'ModelSerializer',
)

from fusebox.orm.etc import SERIALIZER_FIELDS_MAPPING, SERIALIZER_META_MAIN_ATTRS


class BaseSerializer:

    def __init__(
        self, *,
        as_field_dict: bool = False,
        raise_exception: bool = True,
        only: tuple[str, ...] = None,
        exclude: tuple[str, ...] = None
    ):
        # Main preparations
        self._fields: dict = None
        self._prepare_fields(only, exclude)

        # Flags

        self._is_valid = None
        self._raise_exception = raise_exception
        self._as_field_dict = as_field_dict

    def _prepare_fields(
        self,
        only: Union[tuple[str], list[str]] = None,
        exclude: Union[tuple[str], list[str]] = None
    ):
        """
        Collect and prepare all fields in `Serializer`

        Args:
            only (list|tuple): list of values that will be displayed, unspecified will be ignored
            exclude (list|tuple):
        """
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
        >>> from fusebox.core.fields import *
        >>> from fusebox.core.validators import *
        >>> from fusebox.orm.serializers import *

        >>>    class UserModelSerializer(ModelSerializer):
        >>>        class Meta:
        >>>            model = User
        >>>            fields = ('id', 'username', 'firstname', 'lastname')
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

    @classmethod
    def __new__(cls, *args, **kwargs):
        cls._meta_info = cls._prepare_meta_info()
        return super().__new__(cls)

    @classmethod
    def _prepare_meta_info(cls) -> dict:
        meta_info = {}
        if hasattr(cls, 'Meta'):
            for key, val in cls.Meta.__dict__.items():
                meta_info.update({key: val})

        if not all(i in meta_info for i in SERIALIZER_META_MAIN_ATTRS):
            raise AttributeError('Not all required meta-fields are defined')

        return meta_info

    def __init__(
        self,
        model: Union[Iterable[object], object] = None,
        data: Union[Iterable[dict], dict] = None,
        many: bool = False,
        **kwargs,
    ):
        self._model = model or self._meta_info.get('model')
        self._model_dict = {}
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

        if model_attr_dict:
            return model_attr_dict

        raise ValueError('Model attrs dict is empty'
                         ' or doesnt contain needed attributes')

    def _prepare_fields(
        self,
        only: Union[tuple[str], list[str]] = None,
        exclude: Union[tuple[str], list[str]] = None
    ):
        """
        Collect and prepare all fields in `Serializer`

        Args:
            only (list|tuple): list of values that will be displayed, unspecified will be ignored
            exclude (list|tuple):
        """
        only = only or self._meta_info.get('only')
        exclude = exclude or self._meta_info.get('exclude')

        if only and exclude:
            raise AttributeError('Cant use `only` and `exclude` together')

        fields: list[Field] = []

        if self._meta_info.get('model'):
            self._model_dict = self._get_model_dict(self._model) or {}
            self._model_dict = {k: v for (k, v) in self._model_dict.items() if k in self._meta_info.get('fields')}

            if only:
                self._model_dict = {k: v for (k, v) in self._model_dict.items() if k in only}

            if exclude:
                self._model_dict = {k: v for (k, v) in self._model_dict.items() if k not in exclude}

            if self._model_dict:
                # We're not setting value here, only adding
                for name, value in self._model_dict.items():
                    # Guessing field class by its type
                    field = SERIALIZER_FIELDS_MAPPING.get(type(value))
                    field: Union[Field, None] = getattr(fields_mod, field, None)
                    if field:
                        field = field(name=name)
                        fields.append(field)

        field_names = tuple(i.name for i in fields)
        class_attrs_dict: dict = self.__class__.__dict__

        if exclude:
            class_attrs_dict = {k: v for (k, v) in class_attrs_dict.items() if k not in exclude}

        elif only:
            class_attrs_dict = {k: v for (k, v) in class_attrs_dict.items() if k in only}

        for name, field in class_attrs_dict.items():
            if name not in field_names and isinstance(field, Field):
                if name not in self._model_dict:
                    if not self._meta_info.get('ignore_undeclared_fields'):
                        raise UndeclaredField(name)

                if field.name is None:
                    field.name = name

                fields.append(field)

        self._fields = {f.name: f for f in fields}

    def _handle_model(self, as_dict: bool = False) -> Union[dict, FieldContainer]:
        """
        Main data handler

        Arguments:
            as_dict (bool): convert `FieldContainer (-s)` to dict
        """
        try:
            if self._as_field_dict:
                field_dict = FieldContainer()
            else:
                field_dict = {}

            # TODO: доделать
            model_dict = self._model_dict

            for field in self._fields.values():
                # TODO: it's kinda retarded way to set field's value
                field.set(model_dict.get(field.name))

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
