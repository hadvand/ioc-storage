"""This module provides the IOC storage's model-controller."""
# ioc_storage/ioc_storage.py

from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from ioc_storage import DB_READ_ERROR, ID_ERROR
from ioc_storage.database import DatabseHandler


class CurrentIOC(NamedTuple):
    ioc: Dict[str, Any]
    error: int


class IOCer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabseHandler(db_path)

    def add(self, link: List[str], source: List[str]) -> CurrentIOC:
        """ Add a new IOC to the database """
        ioc = {
            'link': link,
            'source': source
        }
        read = self._db_handler.read_iocs()
        if read.error == DB_READ_ERROR:
            return CurrentIOC(ioc, read.error)

        read.ioc_list.append(ioc)
        write = self._db_handler.write_iocs(read.ioc_list)
        return CurrentIOC(ioc, write.error)

    def get_ioc_list(self) -> List[Dict[str, Any]]:
        """Return a current list of IOCs"""
        read = self._db_handler.read_iocs()
        return read.ioc_list

    def remove(self, ioc_id: int) -> CurrentIOC:
        """Remove an IOC from the database using its ID"""
        read = self._db_handler.read_iocs()
        if read.error == DB_READ_ERROR:
            return CurrentIOC({}, read.error)

        try:
            ioc = read.ioc_list.pop(ioc_id - 1)
        except IndexError:
            return CurrentIOC({}, ID_ERROR)

        write = self._db_handler.write_iocs(read.ioc_list)
        return CurrentIOC(ioc, write.error)

    def remove_all(self) -> CurrentIOC:
        """Remove all IOCs from the database"""
        write = self._db_handler.write_iocs([])
        return CurrentIOC({}, write.error)

