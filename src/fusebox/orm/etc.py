import datetime

SERIALIZER_META_ALL_FIELDS = '__all__'

SERIALIZER_META_MAIN_ATTRS = (
    'fields', 'model',
)

SERIALIZER_FIELDS_MAPPING = {
    int: 'IntegerField',
    float: 'FloatField',
    str: 'StringField',
    list: 'ArrayField',
    tuple: 'ArrayField',
    datetime.datetime: 'DateField',
}
