from fuse_core import EmailValidator
from fuse_core.core.fields import Field
from fuse_core.core.containers import FieldDictionary


def test_container():
    field_cont = FieldDictionary()

    name_field = Field(name='name')
    name_field.set('Name')

    email_field = Field(name='email', validators=[EmailValidator])
    email_field.set('walter@mail.com')

    field_cont['name'] = name_field
    field_cont['email'] = email_field

    print(f"{field_cont.to_json(full_house=True)=}")
    print(f"{field_cont.get_items(full_house=True)=}")
