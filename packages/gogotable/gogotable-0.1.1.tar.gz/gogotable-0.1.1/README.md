# GoGoTable

[![PyPI version](https://badge.fury.io/py/gogotable.svg)](https://badge.fury.io/py/gogotable)
[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)


Converts structured data to a table.

## How to use ?

```python
    from gogotable import gogotable

    headers = ["Month", "Day"]
    rows = [["March", "31"], ["April", "25"], ["May", "1"], ["May", "30"]]

    table = gogotable(headers, rows)

    for line in table:
        print(line)
```
This code will print the following table:

    |-------------|
    | Month | Day |
    |-------------|
    | March |  31 |
    | April |  25 |
    |   May |   1 |
    |   May |  30 |
    |-------------|

## Setup Development Environment

You need the following tools installed on your machine:

- [Poetry](https://python-poetry.org) for Python package management.
- [Poetry Plugin: Export](https://github.com/python-poetry/poetry-plugin-export)
  for exporting dependencies.
- [Poetry Plugin: up](https://github.com/MousaZeidBaker/poetry-plugin-up)
  for updating dependencies.

Ensure you have Python 3.9 or above installed by running:

```bash
python --version
# Python 3.9.x
```

