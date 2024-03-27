"""This module provides the IOC storage's database functionality."""
# ioc_storage/database.py

import configparser
import psycopg2

from ioc_storage import DB_WRITE_ERROR, SUCCESS
from typing import Any, Dict, List, NamedTuple

from ioc_storage import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS


class DatabaseHandler:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="db_user",
                password="123"
            )
        return self.connection

    def create_tables(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ips (
                    id SERIAL PRIMARY KEY,
                    ip INET NOT NULL,
                    source_id INTEGER REFERENCES sources(id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL,
                    source_id INTEGER REFERENCES sources(id)
                );
            """)
            self.get_connection().commit()

    def delete_ip(self, ip: str):
        with self.get_connection().cursor() as cursor:
            cursor.execute("DELETE FROM ips WHERE ip = %s", (ip,))
            self.get_connection().commit()

    def delete_url(self, url: str):
        with self.get_connection().cursor() as cursor:
            cursor.execute("DELETE FROM urls WHERE url = %s", (url,))
            self.get_connection().commit()

    def delete_all_records(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute("DELETE FROM ips;")
            cursor.execute("DELETE FROM urls;")
            self.get_connection().commit()

    def write_new_ip_with_source(self, ip: str, source_name: str):
        source = self.get_source_by_name(source_name)
        if source:
            with self.get_connection().cursor() as cursor:
                cursor.execute("INSERT INTO ips (ip, source_id) VALUES (%s, %s)", (ip, source["id"]))
                self.get_connection().commit()
        else:
            raise ValueError(f"Source '{source_name}' not found.")

    def write_new_url_with_source(self, url: str, source_name: str):
        source = self.get_source_by_name(source_name)
        if source:
            with self.get_connection().cursor() as cursor:
                cursor.execute("INSERT INTO urls (url, source_id) VALUES (%s, %s)", (url, source["id"]))
                self.get_connection().commit()
        else:
            raise ValueError(f"Source '{source_name}' not found.")

    def get_source_by_name(self, source_name: str):
        with self.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM sources WHERE name = %s;", (source_name,))
            source = cursor.fetchone()
            if source:
                source_id, _ = source
                return {"id": source_id, "name": source_name}

    def list_all_ips_and_urls_with_sources(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute("""
                SELECT ips.ip, sources.name AS source_name
                FROM ips
                JOIN sources ON ips.source_id = sources.id;
            """)
            ip_records = cursor.fetchall()
            cursor.execute("""
                SELECT urls.url, sources.name AS source_name
                FROM urls
                JOIN sources ON urls.source_id = sources.id;
            """)
            url_records = cursor.fetchall()

            return ip_records + url_records

    def list_all_unique_sources(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM sources;")
            sources = cursor.fetchall()
            return [source[1] for source in sources]

    def show_total_of_ips_and_urls(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM ips;")
            total_ips =cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM urls;")
            total_urls = cursor.fetchone()[0]

            return total_ips + total_urls
