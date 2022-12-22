import re
import datetime
from typing import Union

from fusebox import EmailValidator
from fusebox.core.etc import INDEX_ALL
from fusebox.core.handlers import Regex, Mapper

from fusebox.core.fields import (
    Field, StringField, IntegerField,
    FloatField, ArrayField, DateField
)


def clean_digits(value: str) -> Union[str, None]:
    value = re.search(r'^[\d+\,]+|^[\d+]', value)
    if value:
        value = value.group(0)
        value = value.replace(',', '.')
        return value


class Object:
    
    def __init__() -> None:
        self._var = 123
        
    def __str__() -> str:
        return str(self._var)


def test_fields():
    string_field = StringField(name='base_string_field')
    string_field.set(Object())
    assert isinstance(string_field, str), TypeError('Value type must be string')
    
    integer_field = IntegerField(name='base_integer_field')
    integer_field.set("123")
    assert isinstance(integer_field, int), TypeError('Value type must be integer')
    
    float_field = FloatField(name='base_float_field')
    float_field.set('4 3/2')
    assert isinstance(float_field.value, float), TypeError('Value type must be float')
    
    array_field = ArrayField(
        name='my_array_field',
        child_field=IntegerField(),
        size=2
    )
    array_field.set('222,222')
    assert len(array_field) == 2, ValueError('Value length must be equal 2')
    assert isinstance(array_field.value, (tuple, list)), TypeError('Value type must be list or tuple')
    
    date_field = DateField(as_string=False)
    date_field.set('2020.04.05')
    assert isinstance(date_field, datetime.datetime), TypeError('Value type must be datetime')
    

def test_handlers():
    field_regex = Field(
        handlers=[Regex(r'([\w+\.]+)@([\w+\.]+)', index=INDEX_ALL())]
    )
    field_regex.set('username1@mail.com')
    assert ['username1', 'mail.com'] == field_regex.value, IndexError('Value list must be equal ['username1', 'mail.com']')
    
    field_mapping = Field(
        handlers=[Mapper({'Yes': True, 'No': False}, default=None, ignore_case=True)]
    )
    field_mapping.set('Yes')
    assert field_mapping.value is True, TypeError('Value type must be False')

    field_mapping.set('no')
    assert field_mapping.value is False, TypeError('Value type must be False')

    field_mapping.set('None value')
    assert field_mapping.value is None, TypeError('Value type must be `NoneType`')


def test_functional_handlers():
    integer_field = IntegerField(method=clean_digits)
    integer_field.set('123@@@')
    assert isinstance(integer_field.value, int), TypeError('Value type must be integer')
    
    float_field = FloatField(method=clean_digits)
    float_field.set('222,00')
    assert isinstance(float_field.value, float), TypeError('Value type must be float')
