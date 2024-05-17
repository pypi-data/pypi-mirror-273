import sqlite3
from logging import getLogger
import time
import random
from pathlib import Path
from typing import Type, Dict, Iterable
import json

log = getLogger()


class MSQLiteMaxRetriesError(sqlite3.OperationalError):
    pass


type_to_sqlite_type = {
    int: "INTEGER",
    "int": "INTEGER",
    float: "REAL",
    "float": "REAL",
    str: "TEXT",
    "str": "TEXT",
    bytes: "BLOB",
    "bytes": "BLOB",
    bool: "INTEGER",
    "bool": "INTEGER",
    json: "JSON",
    "JSON": "JSON",
    type(None): "NULL",
    "None": "NULL",
}


def _convert_column_dict_to_sqlite(column_spec: str, column_type: Type) -> str:
    """
    Convert a column specification to a SQLite column specification.
    :param column_spec: column name and optional constraints. Example: "id PRIMARY KEY"
    :param column_type: column type (Python types such as int, float, str, etc.). Example: int
    :return: column specification string for SQLite
    """
    column_spec_parts = column_spec.split()
    assert len(column_spec_parts) > 0  # at least the column name
    column_name = column_spec_parts[0]
    if (column_type_string := type_to_sqlite_type.get(column_type)) is None:
        raise ValueError(f"{column_type} (type={type(column_type)}) is not a supported SQLite column type (see msqlite.type_to_sqlite_type for supported types)")
    if len(column_spec_parts) > 1:
        constraints = column_spec_parts[1:]
    else:
        constraints = []
    spec_components = [column_name, column_type_string]
    spec_components.extend(constraints)
    spec = " ".join(spec_components)
    return spec


class MSQLite:
    """
    A context manager around sqlite3 access that handles multithreading and multiprocessing. Also, automatically creates a table if it does not exist.
    """

    def __init__(self, db_path: Path, table_name: str, schema: dict[str, Type] | None = None, retry_scale: float = 0.01, retry_limit: int | None = None):
        """
        :param db_path: database file path
        :param table_name: table name
        :param schema: dictionary of column names and types. Example: {"id PRIMARY KEY": int, "name": str, "color": str, "year": int}
        :param retry_scale: scale factor for retrying to connect to the database (1.0 is an average of 1 second)
        """
        self.db_path = db_path
        self.table_name = table_name
        self.retry_scale = retry_scale
        self.retry_limit = retry_limit
        self.schema = schema
        self.execution_times = []  # type: list[float]
        self.retry_count = 0
        self.artificial_delay = None  # type: float | None
        self.conn = None  # type: sqlite3.Connection | None
        self.cursor = None  # type: sqlite3.Cursor | None

    def __enter__(self):
        while self.conn is None:
            if self.retry_limit is not None and self.retry_count > self.retry_limit:
                raise MSQLiteMaxRetriesError(f"Exceeded maximum retries of {self.retry_limit}")
            try:
                self.conn = sqlite3.connect(self.db_path, isolation_level="EXCLUSIVE")
                self.cursor = self.conn.cursor()
                if self.schema is not None:
                    columns = ",".join([_convert_column_dict_to_sqlite(column_spec, column_type) for column_spec, column_type in self.schema.items()])
                    statement = f"CREATE TABLE IF NOT EXISTS {self.table_name}({columns})"
                    self.cursor.execute(statement)
                self.conn.execute("BEGIN EXCLUSIVE TRANSACTION")  # lock the database
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    self.conn.rollback()
                    self.retry_count += 1
                    self.conn = None
                    time.sleep(self.retry_scale * 2.0 * random.random())
                else:
                    # some other exception
                    raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        if self.conn is not None:
            self.conn.close()
        if len(self.execution_times) > 0:
            max_execution_time = max(self.execution_times)
        else:
            max_execution_time = None
        log.info(f"{max_execution_time=}")
        log.info(f"{self.retry_count=}")

    def set_artificial_delay(self, delay: float):
        """
        Set an artificial delay for testing purposes to keep the DB file locked for a period of time. Useful for testing, but not to be used in normal operation.
        :param delay: delay in seconds
        """
        self.artificial_delay = delay

    def execute(self, statement: str, parameters: Dict | Iterable | None = None) -> sqlite3.Cursor:
        """
        Execute statements on a sqlite3 database, with an auto-commit and a retry mechanism to handle multiple threads/processes.

        :param statement: SQL statement to execute
        :param parameters: parameters for the SQL statement
        :return: sqlite3.Cursor after execute statement
        """

        start = time.time()
        assert self.conn is not None
        if self.artificial_delay is not None:
            time.sleep(self.artificial_delay)  # only for testing
        assert self.cursor is not None
        if parameters is None:
            new_cursor = self.cursor.execute(statement)
        else:
            new_cursor = self.cursor.execute(statement, parameters)
        self.execution_times.append(time.time() - start)
        return new_cursor
