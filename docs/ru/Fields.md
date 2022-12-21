# Field

Класс `Field` является базовым классом, дающий возможность валидации, обработки данных и конвертации данных в нужный тип данных.

К примеру:

Для работы нам нужно импортировать следующее:

```py
from fusebox import EmailValidator
from fusebox.core.etc import INDEX_ALL
from fusebox.core.handlers import Regex, Mapper
```

Создадим экземпляр класса:

```py
email_field = Field(
    handlers=[Regex(r'([\w+\.]+)@([\w+\.]+)', index=INDEX_ALL())]
)
```

Зададим и выведем значение:

```py
result = email_field.set("coolemail@aol.com")
print(result)

>>> ["coolemail", "aol.com"]
```
