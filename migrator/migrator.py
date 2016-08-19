import os
import datetime as dt

from .state import State, IState


MIGRATION_TEMPLATE = '''"""
Migration %r
Created at %s
"""


def apply():
    raise NotImplementedError


def rollback():
    raise NotImplementedError
'''


class ISearcher:

    def get_names(self) -> [str]:
        pass


class ICreator:

    def new(self, name: str, number: int) -> str:
        pass


class IExecutor:

    def apply(self, migration: str):
        pass


class Migrator:

    def __init__(
        self,
        searcher: ISearcher,
        creator: ICreator,
        executor: IExecutor,
    ):
        self._searcher = searcher
        self._creator = creator
        self._executor = executor

    def create_new_migration(self, name: str) -> str:
        exists = self._searcher.get_names()
        return self._creator.new(name, number=len(exists) + 1)

    def apply(self, n: int):
        exists = self._searcher.get_names()
        for migration in exists:
            if not self._executor.apply(migration) or n is None:
                continue
            n -= 1
            if n == 0:
                # Выполнено заданное кол-во миграций
                break


def migrator_factory(path: str) -> Migrator:
    return Migrator(
        Searcher(path),
        Creator(path),
        Executor(path, State('.migrator')),
    )


class Searcher(ISearcher):

    def __init__(self, path: str):
        self._path = path

    def get_names(self) -> [str]:
        names = self._get_list(self._path)
        names.remove('__init__.py')

        for n in list(names):
            if not n.endswith('.py'):
                names.remove(n)

        return names

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

    def __init__(self, path: str, state: IState):
        self._path = path
        self._state = state

    def apply(self, migration: str) -> bool:
        if migration in self._state['applied']:
            return False
        self._get_module(self._path, migration).apply()
        self._state['applied'].append(migration)
        self._state['history'].append(('migrate', migration, 'date'))
        self._state.save()
        return True

    def _get_module(self, name):
        *_, package_name = self._path.split('/')
        return getattr(__import__(package_name), name.replace('.py', ''))

    # def rollback(self, n: int):
    #         self._get_migration(migration).rollback()
    #         state['applied'].remove(migration)
    #         state['history'].append(('rollback', migration, 'date'))
    #         state.save()

    #         if n is None:
    #             continue

    #         n -= 1
    #         if not n:
    #             break
