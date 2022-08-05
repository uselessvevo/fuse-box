import re
from typing import Union

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


def main():
    field_regex = Field(
        handlers=[Regex(r'([\w+\.]+)@([\w+\.]+)', index=INDEX_ALL())]
    )
    print(f"{field_regex.set('username@mail.com')=}")

    field_mapping = Field(
        handlers=[Mapper({'Yes': True, 'No': False}, 'Not found', True)]
    )
    print(f"{field_mapping.set('Yes')=}")

    print(f"{field_mapping.set('no')=}")

    print(f"{field_mapping.set('None value')=}")

    # Base data Fields

    integer_field = IntegerField(method=clean_digits)
    print(f"{integer_field.set('123@@@')=}")

    float_field = FloatField(method=clean_digits)
    print(f"{float_field.set('222,00')=}")

    float_field = FloatField()
    print(f"{float_field.set('4 3/2')=}")

    # Array Field

    array_field = ArrayField(
        name='my_array_field',
        verbose_name='Sizes',
        child_field=IntegerField(),
        size=2
    )
    print(f"{array_field.set('222,222')=}")

    # Date Field

    date_field = DateField(as_string=True)
    print(f"{date_field.set('2020.04.05')=}")


if __name__ == '__main__':
    main()
