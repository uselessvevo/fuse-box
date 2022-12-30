[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)
![Tests status](https://github.com/uselessvevo/fuse-box/actions/workflows/tests.yml/badge.svg)

[English readme](https://github.com/uselessvevo/fuse-box/tree/main/docs/en) • [Русский readme](https://github.com/uselessvevo/fuse-box/tree/main/docs/ru)

# Yet another library for processing and validating data

This package contains:
* Fields
* Handlers
* Validators
* Containers
* ORM Serializers

# Installing

`python -m pip install git+https://github.com/uselessvevo/fuse-box.git`

# Basic usage

```py
from fusebox.core.fields import FloatField


float_field = FloatField(name='base_float_field')
float_field.set('4 3/2')
```

You can find all examples in docs or just look in `tests` directory
