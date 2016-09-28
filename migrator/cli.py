import enum
import os

import click

from .application import migrator_factory


MIGRATIONS_PATH = './migrations'
LIST_NAME_LENGTH = 50


path_option = click.option(
    '--path', '-p', default=MIGRATIONS_PATH, help='migrations path',
)
number_option = click.option(
    '--number', '-n', type=int, default=None, help='migrations number',
)


class Color(enum.Enum):
    RED = 'red'
    GREEN = 'green'


@click.group()
def cli():
    pass


@cli.command()
@path_option
@click.option('--name', '-n', default='migration', help='new migration name')
def new(path, name):
    create_package(path)
    migration_name = migrator_factory(path).create_new_migration(name)
    click.echo('Migration "%s" created.' % migration_name)


@cli.command()
@path_option
@number_option
def apply(path, number):
    applied_migrations = migrator_factory(path).apply(number)
    click.echo('%s applied.' % applied_migrations)


@cli.command()
@path_option
@number_option
def rollback(path, number):
    rollbacked_migrations = migrator_factory(path).rollback(number)
    click.echo('%s rollbacked.' % rollbacked_migrations)


@cli.command()
@path_option
@number_option
def show(path, number):
    migrations = migrator_factory(path).get_migrations(number)

    click.echo('Migration' + ' ' * (LIST_NAME_LENGTH - 9) + 'Applied?')
    for name, applied in migrations:
        msg = name + ' ' * (LIST_NAME_LENGTH - len(name)) + str(applied)
        color = Color.GREEN if applied else Color.RED
        click.echo(click.style(msg, fg=color))


def create_package(path: str):
    if os.path.exists(path):
        return

    os.mkdir(path)
    with open(os.path.join(path, '__init__.py'), 'w') as f:
        f.write('')
