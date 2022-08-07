from fuse_core.core.fields import *
from fuse_core.core.validators import *


def test_validators():
    age = IntegerField(10, name='age', validators=[RangeValidator(10, 20)])
    print(f'{age.value=}')

    email_field = Field('username2@mail.ru', validators=[EmailValidator])
    print(f"{email_field.value=}")


if __name__ == '__main__':
    test_validators()
