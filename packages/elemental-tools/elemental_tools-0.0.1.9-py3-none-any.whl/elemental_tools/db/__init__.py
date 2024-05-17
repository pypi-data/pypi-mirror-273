import logging
import re
from typing import Optional

import certifi

from sqlalchemy import DDL as RAW_DDL, create_engine, MetaData, select, update, delete, func, Result, and_, or_, null
from sqlalchemy.exc import IntegrityError as DuplicateKeyError
from sqlalchemy.orm import sessionmaker, Mapped
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.dialects.postgresql import insert

from elemental_tools.tools import get_package_name
from elemental_tools.db.types import JSONColumn, List, Dict, SQLEnum

from sqlalchemy import inspect
from psycopg2.errors import UndefinedTable
from sqlalchemy.exc import ProgrammingError

from elemental_tools.config import config_initializer
from elemental_tools.exceptions import InternalException
from elemental_tools.logger import Logger
from elemental_tools.db.types import *
from elemental_tools.db.orm import SQLModel, ForeignKey, relationship, AppendableTableArgs

database_extensions = ["CITEXT", "pgcrypto"]
max_retry_times = 3


class Connect:

    config = config_initializer()

    __logger__ = Logger(app_name="postgresql", origin="database", owner=config.app_name).log
    __logger__(level="info", message=f"Connecting to:\n\tURI: {config.db_url}\n\tDatabase: {config.db_name}")

    def __init__(self, uri: str = config.db_url, database: str = config.db_name, environment: str = None):

        if uri is None and database is None:
            raise Exception("Invalid Database Configuration.\n\tPlease Check Your Environment File.")

        last_backslash_pattern = r"\/$"
        _connection_uri = f"{re.sub(last_backslash_pattern, '', uri)}/{database}"

        # Define a regular expression pattern to match a forward slash at the end of the URI
        clean_log = False
        if environment is not None:
            clean_log = environment.lower() == "production"
            if environment.lower() == "production":
                _connection_uri += "?sslmode=require"
            elif environment.lower() == "debug":
                _connection_uri += f"?sslrootcert={certifi.where()}"

        self.engine = create_engine(_connection_uri)

        if self.config.debug:
            sqlalchemy_engine_logger = Logger(app_name=self.config.app_name, origin="sqlalchemy.engine", owner=get_package_name(__name__))
            sqlalchemy_engine_logger.get_logger("sqlalchemy.engine", level="info", clean=clean_log)

        self.metadata = MetaData()
        self.session = sessionmaker(bind=self.engine)

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

    def create_table(self):
        return SQLModel.metadata.create_all(self.engine)
