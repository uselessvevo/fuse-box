__all__ = (
    'DEFAULT_ARRAY_SEPARATORS',
    'DEFAULT_FLOAT_SEPARATORS',
    'AMERICAN_DATE_FORMAT',
    'AMERICAN_DATETIME_FORMAT',
    'EUROPEAN_DATE_FORMAT',
    'EUROPEAN_DATETIME_FORMAT',
    'DEFAULT_REGEX_INDEX',
    'INDEX_ALL',
    'LIMITLESS_ARRAY',
    'DATE_REGEX',
    'EMPTY_VALUE',
    'DEFAULT_FROM_INPUT'
)

# Default empty value
EMPTY_VALUE = type('EMPTY_VALUE', (), {})

# Raw field instance
RAW_FIELDS = type('RAW_FIELDS', (), {})

# Return input value if error occurred
DEFAULT_FROM_INPUT = type('DEFAULT_AS_INPUT', (), {})

# Default separators for `ArrayField`
DEFAULT_ARRAY_SEPARATORS = ('-', '@', '—', ',')

# Default separators for `FloatField`
DEFAULT_FLOAT_SEPARATORS = (',', '.')

# To get all values from iterable field's result
INDEX_ALL = type('INDEX_ALL', (), {})

# Default regex group index for `Regex` handler
DEFAULT_REGEX_INDEX = 1

# To disable `ArrayField` size limit
LIMITLESS_ARRAY = type('ARRAY_NO_SIZE_LIMITS', (), {})

# Date regex, formats
DATE_REGEX = r'(\d+\S+\d+\S+\d+)'

EUROPEAN_DATE_FORMAT = '%d.%m.%Y'
EUROPEAN_DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

AMERICAN_DATE_FORMAT = '%Y-%m-%d'
AMERICAN_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATETIME_ATTRIBUTE = 'date'
