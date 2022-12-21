# Field

The `Field` class is the base class for validation, data handling and type conversion.

To work, we need to import the following:

```py
from fuse box import Email verification
from fusebox.core.etc import INDEX_ALL
from fuse box.the core.handlers import regular expression, cartographer
```

Creating an instance of the class:

```py
email_field = Field(
    handlers=[Regular expression(r'([\w+\.]+)@([\w+\.]+)', index=INDEX_ALL())]
)
```

We will set and output the value:

```
result py = email_field.set("coolemail@aol.com ")
print(result)

>>> ["coolemail", "aol.com "]
```
