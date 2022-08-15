from fuse_core.core.fields import *
from fuse_core.core.validators import *


def test_validators():
    age = IntegerField(10, name='age', validators=[RangeValidator(10, 20)])
    age.set()
    assert age.value in (10, 20), ValueError
    print(f'{age.value=}')

    email_field = Field('username2@mail.ru', validators=[EmailValidator])
    email_field.set()
    assert isinstance(email_field.value, str), ValueError
    print(f"{email_field.value=}")
