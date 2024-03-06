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

    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(f'Creating database failed with: {ERRORS[db_init_error]}',
                    fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(f'The ioc-storage database is {db_path}',
                    fg=typer.colors.GREEN)


def get_iocer() -> ioc_storage.IOCer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "ioc_storage init" first',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_path.exists():
        return ioc_storage.IOCer(db_path)
    else:
        typer.secho(
            'Database not found. Please run "ioc_storage init" first',
            fg=typer.colors.RED
        )
    raise typer.Exit(1)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def add(
        input: List[str] = typer.Argument(...),
) -> None:
    """Add a new IOC to the database"""
    link, source = input
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
        'ID.  ',
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
                '-'  * len(headers),
                fg=typer.colors.BLUE
    )

    for id, ioc in enumerate(ioc_list, 1):
        link, source = ioc.values()
        typer.secho(
            f'{id}{(len(columns[0]) - len(str(id))) * " "}'
            f'| ({link}){(len(columns[1]) - len(str(link)) - 4) * " "}'
            f'| {source}{(len(columns[2]) - len(str(source)) - 2) * " "}',
            fg=typer.colors.BLUE
        )
        typer.secho(
                    '-' * len(headers) + '\n',
                    fg=typer.colors.BLUE
        )


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
