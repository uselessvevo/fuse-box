from fusebox import EmailValidator
from fusebox.core.fields import Field
from fusebox.core.containers import FieldContainer


def test_container():
    field_cont = FieldContainer()

    name_field = Field(name='name')
    name_field.set('Name')

    email_field = Field(name='email', validators=[EmailValidator])
    email_field.set('walter@mail.com')

    field_cont['name'] = name_field
    field_cont['email'] = email_field

    print(f"{field_cont.as_json(full_house=True)=}")
    print(f"{field_cont.get_items(full_house=True)=}")
