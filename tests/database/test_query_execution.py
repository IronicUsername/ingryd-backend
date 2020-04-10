from datetime import datetime

import psycopg2
import pytest

from ingryd.database import query


def test_query(database):
    """Test query execution function."""
    # Non parametric query
    with query('SELECT NOW();') as res:
        assert isinstance(res.fetchall()[0][0], datetime)

    # Parametric query
    with query('SELECT %s;', (1,)) as cur:
        res = cur.fetchall()
        assert len(res) == 1
        assert isinstance(res[0][0], int)

    # Test error
    with pytest.raises(psycopg2.ProgrammingError):
        with query('SELECT * FROM blabla') as cur:
            pass


def test_database_fixture(database):
    """Test 'database' fixture."""
    # Test connection status
    assert database.status == psycopg2.extensions.STATUS_READY
