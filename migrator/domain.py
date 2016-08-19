
class IState:

    def __getitem__(self, k):
        pass

    def __setitem__(self, k, v):
        pass

    def save(self):
        pass


class ISearcher:

    def get_names(self) -> [str]:
        pass


class ICreator:

    def new(self, name: str, number: int) -> str:
        pass


class IExecutor:

    def apply(self, migration: str):
        pass

    def rollback(self, migration: str):
        pass


class Migrator:

    def __init__(
        self,
        state: IState,
        searcher: ISearcher,
        creator: ICreator,
        executor: IExecutor,
    ):
        self._state = state
        self._searcher = searcher
        self._creator = creator
        self._executor = executor

    def create_new_migration(self, name: str) -> str:
        exists = self._searcher.get_names()
        return self._creator.new(name, number=len(exists) + 1)

    def apply(self, number: int) -> [str]:
        migrations = self._searcher.get_names()
        return self._execute(migrations, self._apply, number)

    def rollback(self, number: int) -> [str]:
        migrations = reversed(self._searcher.get_names())
        return self._execute(migrations, self._rollback, number)

    def get_migrations(self, number: int) -> [{str: True}]:
        exists = self._searcher.get_names()
        result = []
        for migration in list(reversed(exists))[:number]:
            result.append((migration, migration in self._state['applied']))
        return result

    def _execute(self, migrations, handler, number):
        executed = []
        for migration in migrations:
            if not handler(migration):
                continue
            self._state.save()
            executed.append(migration)

            if number is None:
                continue
            number -= 1
            if number == 0:
                break

        return executed

    def _apply(self, migration):
        if migration in self._state['applied']:
            return False
        self._executor.apply(migration)
        self._state['applied'].append(migration)
        return True

    def _rollback(self, migration):
        if migration not in self._state['applied']:
            return False
        self._executor.rollback(migration)
        self._state['applied'].remove(migration)
        return True
