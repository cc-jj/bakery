#! /usr/bin/env python3
import os
import dotenv

import alembic.command
import alembic.config
import click
import uvicorn


def correct_cwd():
    """alembic and SQLALCHEMY_DATABASE_URL requires running from the root directory"""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != root_dir:
        click.echo('Changing current working directory to', root_dir)
        os.chdir(root_dir)


def load_env(env_file: str):
    click.echo(f"ENV file: {env_file}")
    dotenv.load_dotenv(env_file)


@click.group()
def cli():
    pass


@click.group()
def app():
    pass


@click.command()
@click.option('-e', '--env-file', 'env_file', type=click.Path(exists=True), default=None)
def launch(env_file):
    if env_file:
        load_env(env_file)
    correct_cwd()
    uvicorn.run('src.main:app', host='localhost', port=3000)


app.add_command(launch)


@click.group()
def db():
    pass


@click.command()
@click.option('-e', '--env-file', 'env_file', type=click.Path(exists=True), default=None)
def update(env_file):
    if env_file:
        load_env(env_file)
    correct_cwd()
    from src.settings import SQLALCHEMY_DATABASE_URL
    click.echo(f'Confirm migration of {SQLALCHEMY_DATABASE_URL}')
    if click.prompt("'y' to continue\n") == 'y':
        cfg = alembic.config.Config('alembic.ini')
        alembic.command.upgrade(cfg, 'head')
    else:
        click.echo('aborted')


@click.command()
@click.option('-e', '--env-file', 'env_file', type=click.Path(exists=True), default=None)
def create_migration(env_file):
    if env_file:
        load_env(env_file)
    correct_cwd()
    click.echo('Auto-generating migration revision')
    message = click.prompt("Enter a revision message:\n")
    if message.strip() == "":
        raise ValueError("message cannot be empty")
    cfg = alembic.config.Config("alembic.ini")
    alembic.command.revision(cfg, message, autogenerate=True)


db.add_command(update)
db.add_command(create_migration)


cli.add_command(app)
cli.add_command(db)


if __name__ == '__main__':
    cli()
