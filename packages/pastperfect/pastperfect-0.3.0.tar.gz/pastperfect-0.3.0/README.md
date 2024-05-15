# Past Perfect

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

An experience on storing events.

## How to use ?

Create the [event table](./migrations/01%20-%20Initial.sql) in your database.

```python
from pastperfect import Events

db_session = ... # db_session from sqlachemy
events = Events(db_session)
events.append(
    Event(name="SomethingHappened", data={"key": "value"}),
)
```

## Setup Development Environment

You need the following tools installed on your machine:

- [Poetry](https://python-poetry.org) for Python package management.
- [Poetry Plugin: Export](https://github.com/python-poetry/poetry-plugin-export)
  for exporting dependencies.
- [Poetry Plugin: up](https://github.com/MousaZeidBaker/poetry-plugin-up)
  for updating dependencies.

Ensure you have Python 3.9 and above installed by running:

```bash
python --version
# Python 3.9.x
```
