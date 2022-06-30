import re
from typing import Union

from fuse_core.handlers.config import INDEX_ALL
from fuse_core.handlers.handlers import Regex, Mapper

from fuse_core.handlers.fields import Field, DateField
from fuse_core.handlers.fields import FloatField
from fuse_core.handlers.fields import ArrayField
from fuse_core.handlers.fields import IntegerField


def clean_digits(value: str) -> Union[str, None]:
    value = re.search(r'^[\d+\,]+|^[\d+]', value)
    if value:
        value = value.group(0)
        value = value.replace(',', '.')
        return value


def main():
    field_regex = Field(
        handlers=[Regex(r'([\w+\.]+)@([\w+\.]+)', index=INDEX_ALL())]
    )
    field_regex.set('username@mail.com')
    print(f'{field_regex.value=}')

    field_mapping = Field(
        handlers=[Mapper({'Yes': True, 'No': False}, 'Not found', True)]
    )
    field_mapping.set('Yes')
    print(f'{field_mapping.value=}')

    field_mapping.set('no')
    print(f'{field_mapping.value=}')

    field_mapping.set('None value')
    print(f'{field_mapping.value=}')

    # Base data Fields

    integer_field = IntegerField(method=clean_digits)
    integer_field.set('123@@@')
    print(f'{integer_field.value=}')

    float_field = FloatField(method=clean_digits)
    float_field.set('222,00')
    print(f'{float_field.value=}')

    float_field = FloatField()
    float_field.set('4 3/2')
    print(f'{float_field.value=}')

    # Array Field

    array_field = ArrayField(
        name='my_array_field',
        verbose_name='Размерность',
        child_field=IntegerField(),
        size=2
    )
    array_field.set('222,222')
    print(f'{array_field.value=}')

    # Date Field

    date_field = DateField(as_string=True)
    date_field.set('2020.04.05')
    print(f'{date_field.value=}')


if __name__ == '__main__':
    main()
