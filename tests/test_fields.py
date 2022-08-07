import re
from typing import Union

from fuse_core import EmailValidator
from fuse_core.core.etc import INDEX_ALL
from fuse_core.core.handlers import Regex, Mapper

from fuse_core.core.fields import Field, DateField
from fuse_core.core.fields import FloatField
from fuse_core.core.fields import ArrayField
from fuse_core.core.fields import IntegerField


def clean_digits(value: str) -> Union[str, None]:
    value = re.search(r'^[\d+\,]+|^[\d+]', value)
    if value:
        value = value.group(0)
        value = value.replace(',', '.')
        return value


def test_fields():
    field_regex = Field(
        handlers=[Regex(r'([\w+\.]+)@([\w+\.]+)', index=INDEX_ALL())]
    )
    field_regex.set('username1@mail.com')
    print(f"input value: 'username1@mail.com', field_regex value: {field_regex.value}")

    field_mapping = Field(
        handlers=[Mapper({'Yes': True, 'No': False}, 'Not found', True)]
    )
    field_mapping.set('Yes')
    print(f"input value: 'Yes', field_mapping value: {field_mapping.value}")

    field_mapping.set('no')
    print(f"input value: 'no', field_mapping value: {field_mapping.value}")

    field_mapping.set('None value')
    print(f"input value: 'None value', field_mapping value: {field_mapping.value}")

    # Base data Fields

    integer_field = IntegerField(method=clean_digits)
    integer_field.set('123@@@')
    print(f"input value: '123@@@', integer_field value: {integer_field.value}")

    float_field = FloatField(method=clean_digits)
    float_field.set('222,00')
    print(f"input value: '222,00', float_field value: {float_field.value}")

    float_field = FloatField()
    float_field.set('4 3/2')
    print(f"input value: '4 3/2', float_field value: {float_field.value}")

    # Array Field

    array_field = ArrayField(
        name='my_array_field',
        verbose_name='Sizes',
        child_field=IntegerField(),
        size=2
    )
    array_field.set('222,222')
    print(f"input value: '222,222', array_field value: {array_field.value}")

    # Date Field

    date_field = DateField(as_string=True)
    date_field.set('2020.04.05')
    print(f"input value: '2020.04.05', date_field value: {date_field.value}")

    broken_field = Field(
        'invalidemail.com',
        name='broken_field',
        default='bettercallme@mail.com',
        raise_exception=False,
        validators=[EmailValidator]
    )
    broken_field.set()
    print(f'input value: invalidemail.com, broken_field value: {broken_field.value=}')
