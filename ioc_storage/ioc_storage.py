"""This module provides the IOC storage's model-controller."""
# ioc_storage/ioc_storage.py

from typing import Any, Dict, NamedTuple, List
from ioc_storage import DB_READ_ERROR, ID_ERROR, SUCCESS
from ioc_storage.database import DatabaseHandler


class CurrentIOC(NamedTuple):
    ioc: Dict[str, Any]
    error: int


class IOCer:
    def __init__(self) -> None:
        self._db_handler = DatabaseHandler()

    def add(self, link: str, source: str) -> CurrentIOC:
        """ Add a new IOC to the database """
        try:
            self._db_handler.write_new_url_with_source(link, source)
        except ValueError:
            return CurrentIOC({}, DB_READ_ERROR)
        return CurrentIOC({'link': link, 'source': source}, SUCCESS)

    def get_ioc_list(self) -> List[Dict[str, Any]]:
        """Return a current list of IOCs"""
        ioc_list = self._db_handler.list_all_ips_and_urls_with_sources()
        return [{'link': record[0], 'source': record[1]} for record in ioc_list]

    def remove(self, link: str) -> CurrentIOC:
        """Remove an IOC from the database using its link"""
        try:
            self._db_handler.delete_url(link)
        except ValueError:
            return CurrentIOC({}, ID_ERROR)
        return CurrentIOC({'link': link}, SUCCESS)

    def remove_all(self) -> CurrentIOC:
        """Remove all IOCs from the database"""
        self._db_handler.delete_all_records()
        return CurrentIOC({}, SUCCESS)
