from fuse_core.core.fields import Field


__all__ = (
    'Serializer',
)


class Serializer:
    """
    Simple SQLAlchemy query serializer.
    Inspired by DRF's serializers

    Example:
        class UserSerializer(Serializer):
            id = IntegerField()
            email = StringField()
            first_name = StringField()
            second_name = StringField()
            middle_name = StringField()


        class UserCreateSerializer(Serializer):
            email = StringField(validators=[EmailValidator()])
            first_name = StringField(validators=[MinLengthValidator(1)])
            second_name = StringField(validators=[MaxLengthValidator(125)])
            middle_name = StringField(validators=[MinLengthValidator(1)])
            email = StringField(validators=[EmailValidator()])


        async def test_orm_sql(request: web.Request) -> web.Response:
            # Let's get info from `User` model
            users = await User.query.order_by(User.id.desc()).gino.all()
            results = await UserSerializer(users, many=True).result
            return web.json_response({'results': results})
    """

    @classmethod
    def __new__(cls, *args, **kwargs):
        fields = []
        for name, field in cls.__dict__.items():
            if isinstance(field, Field):
                if field.name is None:
                    field.name = name
                fields.append(field)

        cls._fields = fields
        cls._fields_mapping = {f.name: f for f in fields}
        return super().__new__(cls)

    def __init__(
        self,
        models,
        many: bool = False
    ):
        self._models = models
        self._many = many
        self._is_valid = None

    async def handle(self, raise_exception: bool = True):
        collect = []
        try:
            for model in self._models:
                values = getattr(model, '__values__')
                if not isinstance(values, dict):
                    raise ValueError('non-hashmap `__values__` were found')

                for key, value in values.items():
                    if key in self._fields_mapping.keys():
                        field = self._fields_mapping.get(key)
                        values[key] = field.validate(value)

                collect.append(values)

        except Exception as e:
            self._is_valid = False
            if raise_exception:
                raise e

        return collect

    @property
    async def result(self):
        return await self.handle()

    def __repr__(self):
        return f'({self.__class__.__name__}) <id: {id(self)}>'
