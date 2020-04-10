import logging
import os

import psycopg2
import pytest
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from ingryd.api import create_app
from ingryd.database._connect import _connection
from ingryd.database._connect import _DSN as _DSN_QUERY
from ingryd.database.migration import get_ordered_migration_steps

_DSN = {
    'user': os.environ['DB_USER'],
    'host': os.environ['DB_HOST'],
    'password': os.environ['DB_PASS'],
}
_LOGGER = logging.getLogger(__package__)


@pytest.fixture(scope='session')
def base_path() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


@pytest.fixture
def client():
    return Client(create_app(), BaseResponse)


@pytest.fixture
def clean_database():
    db_name = f'test_db'
    _DSN['database'] = db_name
    _DSN_QUERY['database'] = db_name

    def clean():
        # Connect to default DB, to drop test DB
        with psycopg2.connect(user=_DSN['user'], password=_DSN['password'], host=_DSN['host'], database='postgres') as con, con.cursor() as cur:
            con.set_isolation_level(0)
            # Terminate all connections beforehand.
            cur.execute('SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = %s;', (db_name,))
            cur.execute(f'DROP DATABASE IF EXISTS {db_name};')
            cur.execute(f'CREATE DATABASE {db_name};')

    clean()
    _connection.cache_clear()

    with psycopg2.connect(**_DSN) as con:
        con.autocommit = True
        yield con

    clean()


@pytest.fixture
def database(base_path, clean_database):
    with open(os.path.join(base_path, 'src', 'ingryd', 'database', 'schema.sql'), 'r') as f:
        schema = f.read()

    with clean_database.cursor() as cur:
        cur.execute(schema)
        cur.execute('SELECT version FROM production_db_version;')
        current_version = int(cur.fetchall()[0][0])
    migration_steps = get_ordered_migration_steps()[current_version:]
    new_version = current_version

    for migration in migration_steps:
        new_version += 1
        with clean_database.cursor() as cur:
            cur.execute(migration)
            cur.execute('UPDATE production_db_version SET version = %s;', (new_version,))

    clean_database.commit()

    return clean_database
