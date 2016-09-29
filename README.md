# Migrator
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Afonasev/Migrator/edit/master/LICENSE)
[![Build Status](https://travis-ci.org/Afonasev/Migrator.svg?branch=master)](https://travis-ci.org/Afonasev/Migrator)

## Installing
```
$ pip install git+https://github.com/Afonasev/Migrator
$ python -m migrator
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  apply
  new
  rollback
  show
```

## Create migration
```
$ python -m migrator new
Migration "0001_migration.py" created.

$ python -m migrator new -n my_super_migration
Migration "0002_my_super_migration.py" created.
```

Then you can see created files:
```python
"""
Migration '0001_migration.py'
Created at 2016-08-19T17:52:55.852615
"""


def apply():
    raise NotImplementedError


def rollback():
    raise NotImplementedError
```

and change it:
```python
def apply():
    print('migration 0001_migration.py done!')


def rollback():
    print('migration 0001_migration.py rollbacked!')
```

## Apply migration
```
$ python -m migrator apply -n 1
migration 0001_migration.py done!
["0001_migration.py"] applied.
```
withount ``-n`` flag all migrations will be applied.

## List of migrations
```
$ python -m migrator show
Migration                                         Applied?
0002_my_super_migration.py                        False
0001_migration.py                                 True
```

## Rollback migration
```
$ python -m migrator rollback -n 1
migration 0001_migration.py rollbacked!
["0001_migration.py"] rollbacked.
```
withount ``-n`` flag all migrations will be rollbacked.

## Running the testsuite

The minimal requirement for running the testsuite is ``pytest``.  You can
install it with:

    pip install pytest

Then you can run the testsuite with:

    py.test
