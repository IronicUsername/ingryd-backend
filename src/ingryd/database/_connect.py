from contextlib import contextmanager
import logging
import os
import threading
from time import sleep
from typing import Any, Dict, Tuple, Union

from cachetools.func import ttl_cache
import psycopg2
from psycopg2.extras import DictCursor

from .migration import get_ordered_migration_steps


_DSN = {
    'database': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'host': os.environ['DB_HOST'],
    'password': os.environ['DB_PASS'],
}
_LOGGER = logging.getLogger(__package__)


@ttl_cache(maxsize=128, ttl=60)
def _connection(tid: int) -> psycopg2.extensions.connection:
    return psycopg2.connect(**_DSN, cursor_factory=DictCursor)


@contextmanager
def query(q: str, param: Union[Dict[str, Any], Tuple[Any, ...]] = ()) -> psycopg2.extensions.cursor:
    """Execute a sql query. Can't drop databases/tables.

    Usage
    -----
    ```
    from database import query

    with query('SELECT NOW();') as res:
        print(res.fetchall())
    ```

    Parameters
    ----------
    q: String
        SQL query to execute with %s for param placeholders.
    param: Dict[str, Any] or Tuple[Any, ...]
        Parameters to be substituted for %s in query, parameter count must match %s count.

    Returns
    -------
    cursor: psycopg2.extensions.cursor
        Cursor with execution result.
    """
    try:
        with _connection(threading.get_ident()) as con, con.cursor() as cur:
            cur.execute(q, param)
            yield cur
    except psycopg2.Error as e:
        if isinstance(e, psycopg2.OperationalError) and (e.pgcode is None or e.pgcode.startswith('08')):
            _LOGGER.exception(f'Something went wrong during query execution. Error code: {e.pgcode}\n{e}\n'
                              f'Query was: \n{q}\n'
                              f'Parameters where: \n{param}')
            _connection.cache_clear()
        raise


def create_db():
    """Create tables and initial records in database.

    The setup takes 1 step:
        1) If no tables are present, read in base schema `schema.sql` and execute it. Should never happen after first setup/with data already present.
        2) Get current database schema version from `production_db_version` table and all available `migration_steps`.
        3) Migrate from `current_version` all the way to `len(migration_steps)`.

    Returns
    -------
    version: int
        Current schema version. `0` is base schema `./schema.sql`, `i` represents base schema with all migrations up to `i` applied to it.
    """
    while True:
        try:
            with psycopg2.connect(**_DSN) as con, con.cursor() as cur:
                cur.execute('SELECT 1;')
            break
        except psycopg2.OperationalError:
            _LOGGER.info('Service could not connect to database; retrying in 3 seconds.')
            sleep(3)

    with psycopg2.connect(**_DSN) as con, con.cursor() as cur:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [r[0] for r in cur.fetchall()]

        if not tables:
            schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')

            with open(schema_path, 'r') as f:
                schema = f.read()

            cur.execute(schema)
            con.commit()
            _LOGGER.info(f'Successfully initialized database with `schema.sql` (version 0).')

    with psycopg2.connect(**_DSN) as con, con.cursor() as cur:
        cur.execute('SELECT version FROM production_db_version;')
        current_version = int(cur.fetchall()[0][0])

    migration_steps = get_ordered_migration_steps()[current_version:]
    new_version = current_version
    for migration in migration_steps:
        new_version += 1
        with psycopg2.connect(**_DSN) as con, con.cursor() as cur:
            try:
                cur.execute(migration)
                cur.execute('UPDATE production_db_version SET version = %s;', (new_version,))
                con.commit()
            except (psycopg2.IntegrityError, psycopg2.ProgrammingError) as ex:  # pragma: no cover
                _LOGGER.exception('Something went wrong during database migration!!!\n'
                                  f'Tried to apply migration step {new_version}:\n{migration}\n'
                                  f'Error was:\n{ex}\n'
                                  'Database might have lost consistency!!!\n'
                                  'Attempting to clean up now...')
                con.rollback()
                _LOGGER.info(f'Successfully rolled back migration step {new_version}. Raising error....')
                raise
            else:
                _LOGGER.info(f'Successfully applied migration step {new_version}.')

    return new_version
