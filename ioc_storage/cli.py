"""This module provides the IOC storage's CLI."""
# ioc_storage/cli.py

from pathlib import Path
from typing import Optional, List
import typer
from ioc_storage import (
    __app_name__,
    __version__,
    ERRORS,
    config,
    database,
    ioc_storage
)

app = typer.Typer()


@app.command()
def init(
        db_path: str = typer.Option(
            str(database.DEFAULT_DB_FILE_PATH),
            '--db-path',
            '-db',
            prompt='ioc-storage database path'
        ),
) -> None:
    """Initialize ioc-storage database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(f'Creating config file failed with: {ERRORS[app_init_error]}',
                    fg=typer.colors.RED)
        raise typer.Exit(1)

    db_init_error = database.DatabaseHandler()
    db_init_error.create_tables()
    if db_init_error:
        typer.secho(f'Creating database failed with: {ERRORS[db_init_error]}',
                    fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(f'The ioc-storage database is {db_path}',
                    fg=typer.colors.GREEN)


def get_iocer() -> ioc_storage.IOCer:
    return ioc_storage.IOCer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def add(
        link: str = typer.Argument(...),
        source: str = typer.Argument(...)
) -> None:
    """Add a new IOC to the database"""
    iocer = get_iocer()
    ioc, error = iocer.add(link, source)
    if error:
        typer.secho(
            f'Adding ioc failed with: {ERRORS[error]}',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f'''ioc "{ioc['link']}" was added\n'''
            f'''from source: "{ioc['source']}"''',
            fg=typer.colors.GREEN
        )


@app.command(name='list')
def list_all() -> None:
    """List all IOCs in the database"""
    iocer = get_iocer()
    ioc_list = iocer.get_ioc_list()

    if len(ioc_list) == 0:
        typer.secho('No IOCs found',
                    fg=typer.colors.YELLOW)
        raise typer.Exit()

    typer.secho(
        '\nIOC list:\n',
        fg=typer.colors.BLUE,
        bold=True
    )
    columns = (
        'ID  ',
        'Link  ',
        'Source  '
    )
    headers = ''.join(columns)

    typer.secho(
                headers,
                fg=typer.colors.BLUE,
                bold=True
    )
    typer.secho(
                '-' * len(headers),
                fg=typer.colors.BLUE
    )

    for id, ioc in enumerate(ioc_list, 1):
        link, source = ioc.values()
        typer.secho(
            f'{id}{(len(columns[0]) - len(str(id))) * " "}'
            f'| ({link}){(len(columns[1]) - len(str(link)) - 4) * " "} '
            f'| {source}{(len(columns[2]) - len(str(source)) - 2) * " "}',
            fg=typer.colors.BLUE
        )


@app.command()
def remove(
        ioc_id: int = typer.Argument(...),
        force: bool = typer.Option(
            False,
            '--force',
            '-f',
            help='Force deletion without confirmation'
        )
) -> None:
    """Remove an IOC using the given ID"""
    iocer = get_iocer()

    def _remove():
        ioc, error = iocer.remove(ioc_id)
        if error:
            typer.secho(
                f'Removing ioc # {ioc_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f'''IOC # {ioc_id}: "{ioc['link']}" was removed''',
                fg=typer.colors.GREEN
            )

    if force:
        _remove()
    else:
        ioc_list = iocer.get_ioc_list()
        try:
            ioc = ioc_list[ioc_id-1]
        except IndexError:
            typer.secho(
                'Invalid IOC ID',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        delete = typer.confirm(
            f'''Delete IOC # {ioc_id}: {ioc['link']}?'''
        )
        if delete:
            _remove()
        else:
            typer.secho(
                'Operation cancelled',
                fg=typer.colors.YELLOW
            )


@app.command(name='clear')
def remove_all(
        force: bool = typer.Option(
            ...,
            prompt='Delete all IOCs?',
            help='Force deletion without confirmation'
        )
) -> None:
    """Remove all IOCs"""
    iocer = get_iocer()
    if force:
        error = iocer.remove_all().error
        if error:
            typer.secho(
                f'Removing IOCs failed with "{ERRORS[error]}"',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f'All IOCs were removed',
                fg=typer.colors.GREEN
            )
    else:
        typer.echo('Operation canceled')

if __name__ == "__main__":
    app()
