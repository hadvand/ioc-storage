"""This module provides the IOC storage's database functionality."""
# ioc_storage/database.py

import configparser
from pathlib import Path

import json

from ioc_storage import DB_WRITE_ERROR, SUCCESS
from typing import Any, Dict, List, NamedTuple

from ioc_storage import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath('.' + Path.home().stem + 'ioc_storage.json')


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the ioc-storage database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser['General']['database'])


def init_database(db_path: Path) -> int:
    """Create the ioc-storage database."""
    try:
        db_path.write_text('[]') # empty storage
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    ioc_list: List[Dict[str, Any]]
    error: int


class DatabseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_iocs(self) -> DBResponse:
        try:
            with self._db_path.open('r') as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_iocs(self, ioc_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open('w') as db:
                json.dump(ioc_list, db, indent=4)
            return DBResponse(ioc_list, SUCCESS)
        except OSError:
            return DBResponse([], DB_WRITE_ERROR)
