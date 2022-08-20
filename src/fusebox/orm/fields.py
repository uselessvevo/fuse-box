"""
NOTE: Do not import fields from orm
and core packages together if you're going to use serializers
"""

from fusebox.core import fields


__all__ = ('Field', 'StringField', 'IntegerField',
           'FloatField', 'DateField', 'ArrayField',)


class Field(fields.Field):

    __new_slots__ = ('_required', '_read_only', '_write_only')

    def __init__(
        self, *,
        required: bool = False,
        read_only: bool = False,
        write_only: bool = False,
        **kwargs
    ):
        # Check if value is required
        self._required = required

        # Those two flags will be used in `sort_fields` method
        self._write_only = write_only
        self._read_only = read_only

        super().__init__(**kwargs)

    @property
    def required(self):
        return self._required


StringField = type('StringField', (Field, fields.StringField), {})
IntegerField = type('IntegerField', (Field, fields.IntegerField), {})
FloatField = type('FloatField', (Field, fields.FloatField), {})
ArrayField = type('ArrayField', (Field, fields.ArrayField), {})
DateField = type('DateField', (Field, fields.DateField), {})

