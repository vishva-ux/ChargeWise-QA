"""
PyTest fixtures for Database Automation Testing tier.
"""
import pytest
from database.db_client import DatabaseClient


@pytest.fixture(scope="session")
def db_client():
    """Session-scoped database connection fixture."""
    client = DatabaseClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def is_db_available(db_client):
    """Returns True if PostgreSQL is online and responsive."""
    conn = db_client.get_connection()
    return conn is not None
