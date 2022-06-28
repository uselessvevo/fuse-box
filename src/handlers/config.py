__all__ = (
    'DEFAULT_ALLOWED_TYPES',
    'DEFAULT_ARRAY_SEPARATORS',
    'DEFAULT_NONE_VALUES',
    'DEFAULT_FLOAT_SEPARATORS',
    'AMERICAN_DATE_FORMAT',
    'AMERICAN_DATETIME_FORMAT',
    'EUROPEAN_DATE_FORMAT',
    'EUROPEAN_DATETIME_FORMAT',
    'DEFAULT_REGEX_INDEX',
    'INDEX_ALL',
    'ARRAY_NO_SIZE_LIMITS',
    'READABLE_TYPES_MAPPING',
    'DATE_REGEX'
)

# Типы данных по-умолчанию (`fields.Field`)
DEFAULT_ALLOWED_TYPES = (str, int, float,)

# Символ для деления строки (`fields.ArrayField`)
DEFAULT_ARRAY_SEPARATORS = ('-', '@', '—', ',')

# Нулёвые (ты нулевой) символы по-умолчанию (`fields.Field`)
DEFAULT_NONE_VALUES = ('-', '', ' ', 'N/AН/П', 'N/A\r\nН/П', None)

DEFAULT_FLOAT_SEPARATORS = (',',)

# Для возвращения всего массива
INDEX_ALL = type('INDEX_ALL', (), {})

# Индекс для регулярных выражение по-умолчанию
DEFAULT_REGEX_INDEX = 1

# Неограниченный размер массива
ARRAY_NO_SIZE_LIMITS = type('ARRAY_NO_SIZE_LIMITS', (), {})

# Типы данных для чтения человеками
READABLE_TYPES_MAPPING = {
    int: 'число',
    float: 'число',
    str: 'строка',
    list: 'список',
    tuple: 'список'
}

# Даты (европейский, американский)
DATE_REGEX = r'(\d+\S+\d+\S+\d+)'

EUROPEAN_DATE_FORMAT = '%d.%m.%Y'
EUROPEAN_DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

AMERICAN_DATE_FORMAT = '%Y-%m-%d'
AMERICAN_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATETIME_ATTRIBUTE = 'date'
DEFAULT_AS_INPUT = type('DEFAULT_AS_INPUT', (), {})
