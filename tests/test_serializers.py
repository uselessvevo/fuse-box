import datetime
import random

from fusebox.orm.fields import *
from fusebox.core.validators import *
from fusebox.orm.serializers import *


def test_model_serializer():
    _sa_instance_dict = {
        'dict': {
            'id': random.randrange(1, 20),
            'age': str(random.randrange(18, 25)),
            'birth_day': datetime.datetime.now(),
            'username': f'username{random.randrange(100, 200)}',
            'email': f'username{random.randrange(100, 200)}@email.com'
        }
    }

    class User:
        """ Pseudo-model """
        _sa_instance_state = type('_sa_instance_state', (), _sa_instance_dict)

    class UserModelSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username', 'email', 'username')
            # ignore_undeclared_fields = True

        email = StringField(validators=[EmailValidator])
        username = StringField()

    user_serializer = UserModelSerializer()
    try:
        user_serializer.handle()
    except RuntimeError:
        raise RuntimeError


def test_serializer():
    class UserSerializer(Serializer):
        email = StringField(validators=[EmailValidator], required=True)
        username = StringField(validators=[MinLengthValidator(75)], required=True)
        age = IntegerField(validators=[RangeValidator(16, 75)], required=True)

    user_serializer = UserSerializer(data={'email': 'email@email.com', 'username': 'username1337', 'age': '16'})
    user_info = user_serializer.handle()
    assert user_info == {'email': 'email@email.com', 'username': 'username1337', 'age': 16}, ValueError
