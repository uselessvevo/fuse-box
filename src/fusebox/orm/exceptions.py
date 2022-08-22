class UndeclaredField(AttributeError):

    def __init__(self, field_name: str) -> None:
        self._field_name = field_name

    def __str__(self):
        return f'Undeclared field `{self._field_name}`'
