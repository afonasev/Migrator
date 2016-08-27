import os
import re
import json




import datetime as dt
import collections

from .domain import Migrator, IState, ISearcher, ICreator, IExecutor


STATE_PATH = '.migrator'

MIGRATION_TEMPLATE = '''"""
Migration %r
Created at %s
"""


def apply():
    raise NotImplementedError


def rollback():
    raise NotImplementedError
'''


def migrator_factory(path: str) -> Migrator:
    return Migrator(
        State(STATE_PATH),
        Searcher(path),
        Creator(path),
        Executor(path),
    )


class State(IState):

    JSON_INDENT = 4

    def __init__(self, path: str):
        if os.path.exists(path):
            with open(path) as f:
                self._data = json.load(f)
        else:
            self._data = collections.defaultdict(list)

        self._path = path

    def __getitem__(self, k):
        return self._data[k]

    def __setitem__(self, k, v):
        self._data[k] = v

    def save(self):
        with open(self._path, 'w') as f:
            json.dump(self._data, f, indent=self.JSON_INDENT)


class Searcher(ISearcher):

    def __init__(self, path: str):
        self._path = path

    def get_names(self) -> [str]:
        names = self._get_list(self._path)
        names.remove('__init__.py')

        for n in list(names):
            if not n.endswith('.py'):
                names.remove(n)

        return sorted(names)

    def _get_list(self, path):
        return os.listdir(self._path)


class Creator(ICreator):

    def __init__(self, path: str):
        self._path = path

    def new(self, name: str, number: int) -> str:
        filename = '%04d_%s.py' % (number, name)
        created_at = dt.datetime.now().isoformat()

        with open(os.path.join(self._path, filename), 'w') as f:
            f.write(MIGRATION_TEMPLATE % (filename, created_at))

        return filename


class Executor(IExecutor):

    def __init__(self, path: str):
        self._path = path

    def apply(self, migration: str):
        self._get_module(migration).apply()

    def rollback(self, migration: str):
        self._get_module(migration).rollback()

    def _get_module(self, migration):
        *_, package_name = self._path.split('/')
        migration_name = migration.replace('.py', '')
        package = __import__('.'.join([package_name, migration_name]))
        return getattr(package, migration_name)
