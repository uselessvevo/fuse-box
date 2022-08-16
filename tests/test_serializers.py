from fusebox.core.fields import *
from fusebox.core.validators import *
from fusebox.orm.serializers import *


def test_model_serializer():
    class UserModelSerializer(ModelSerializer):
        class Meta:
            model = None
            fields = ('id', 'username')

    user_serializer = UserModelSerializer(...)
    user_serializer.handle()


def test_serializer():
    class UserSerializer(Serializer):
        email = StringField(validators=[EmailValidator], required=True)
        username = StringField(validators=[MinLengthValidator(75)], required=True)
        age = IntegerField(validators=[RangeValidator(16, 75)], required=True)

    user_serializer = UserSerializer(data={'email': 'email@email.com', 'username': 'username1337', 'age': '16'})
    user_info = user_serializer.handle()
    assert user_info == {'email': 'email@email.com', 'username': 'username1337', 'age': 16}, ValueError
