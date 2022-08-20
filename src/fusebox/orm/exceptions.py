class ValidationError(ValueError):

    def __init__(
        self,
        message: str = 'Validation error',
        code_name: str = 'error',
        detailed_exception: bool = False
    ) -> None:
        self._message = message
        self._code_name = code_name
        self._detailed_exception = detailed_exception

    def __str__(self):
        return self._message

    @property
    def error(self):
        if self._detailed_exception:
            return {'message': self._message, 'code_name': self._code_name}
        return self._message


class UndeclaredField(AttributeError):

    def __init__(self, field_name: str) -> None:
        self._field_name = field_name

    def __str__(self):
        return f'Undeclared field `{self._field_name}`'
