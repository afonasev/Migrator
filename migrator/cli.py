import os

import click

from .application import MIGRATIONS_PATH, STATE_PATH, migrator_factory

LIST_NAME_LENGTH = 50

path_option = click.option(
    '--path', '-p', default=MIGRATIONS_PATH, help='migrations path',
)
state_path_option = click.option(
    '--state', '-s', default=STATE_PATH, help='migrator state path',
)
number_option = click.option(
    '--number', '-n', type=int, default=None, help='migrations number',
)


class Color:
    RED = 'red'
    GREEN = 'green'


@click.group()
def cli():
    pass


@cli.command()
@path_option
@state_path_option
@click.option('--name', '-n', default='migration', help='new migration name')
def new(path, state, name):
    create_package(path)
    migration_name = migrator_factory(path, state).create_new_migration(name)
    click.echo('Migration "%s" created.' % migration_name)


@cli.command()
@path_option
@state_path_option
@number_option
def apply(path, state, number):
    applied_migrations = migrator_factory(path, state).apply(number)
    click.echo('%s applied.' % applied_migrations)


@cli.command()
@path_option
@state_path_option
@number_option
def rollback(path, state, number):
    rollbacked_migrations = migrator_factory(path, state).rollback(number)
    click.echo('%s rollbacked.' % rollbacked_migrations)


@cli.command()
@path_option
@state_path_option
@number_option
def show(path, state, number):
    migrations = migrator_factory(path, state).get_migrations(number)

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
