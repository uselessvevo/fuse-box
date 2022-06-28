import re
from typing import Union

from handlers.config import INDEX_ALL
from handlers.handlers import Regex, Mapper

from handlers.fields import Field, DateField
from handlers.fields import FloatField
from handlers.fields import ArrayField
from handlers.fields import IntegerField


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
    field_regex_result = field_regex.set('username@mail.com')
    print(f'{field_regex_result=}')

    field_mapping = Field(
        handlers=[Mapper({'Yes': True, 'No': False}, 'Not found', True)]
    )
    field_mapping_result = field_mapping.set('Yes')
    print(f'{field_mapping_result=}')

    field_mapping_result = field_mapping.set('no')
    print(f'{field_mapping_result=}')

    field_mapping_result = field_mapping.set('None value')
    print(f'{field_mapping_result=}')

    # Base data Fields

    integer_field = IntegerField(method=clean_digits)
    integer_field_result = integer_field.set('123@@@')
    print(f'{integer_field_result=}')

    float_field = FloatField(method=clean_digits)
    float_field_result = float_field.set('222,00')
    print(f'{float_field_result=}')

    float_field = FloatField()
    float_field_fraction_result = float_field.set('4 3/2')
    print(f'{float_field_fraction_result=}')

    # Array Field

    array_field = ArrayField(
        name='my_array_field',
        verbose_name='Размерность',
        child_field=IntegerField(),
        size=2
    )
    array_field_result = array_field.set('222,222')
    print(f'{array_field_result=}')

    # Date Field

    date_field = DateField(as_string=True)
    date_field_result = date_field.set('2020.04.05')
    print(f'{date_field_result=}')


if __name__ == '__main__':
    main()
