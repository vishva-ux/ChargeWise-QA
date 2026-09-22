"""
Database Client for direct PostgreSQL & PostGIS query execution and integrity validation.
"""
from typing import List, Dict, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseClient:
    """Client for executing parameterized SQL against ChargeWise PostgreSQL database."""

    def __init__(
        self,
        host: str = settings.db.HOST,
        port: int = settings.db.PORT,
        dbname: str = settings.db.NAME,
        user: str = settings.db.USER,
        password: str = settings.db.PASSWORD
    ):
        self.conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
            "connect_timeout": 5
        }
        self._connection = None

    def get_connection(self):
        """Initializes or returns active PostgreSQL connection."""
        if self._connection is None or self._connection.closed != 0:
            try:
                self._connection = psycopg2.connect(**self.conn_params)
                self._connection.autocommit = True
            except Exception as e:
                logger.warning(f"Unable to connect to PostgreSQL at {self.conn_params['host']}:{self.conn_params['port']}: {e}")
                return None
        return self._connection

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Executes a SELECT query and returns rows as dictionaries."""
        conn = self.get_connection()
        if conn is None:
            logger.warning("PostgreSQL connection not established. Returning empty list.")
            return []

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or ())
            return [dict(row) for row in cursor.fetchall()]

    def execute_scalar(self, query: str, params: Optional[tuple] = None) -> Any:
        """Executes a query returning a single scalar value."""
        conn = self.get_connection()
        if conn is None:
            return None

        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result[0] if result else None

    def table_exists(self, table_name: str) -> bool:
        """Checks if a table exists in the public schema."""
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = %s
            );
        """
        return bool(self.execute_scalar(query, (table_name,)))

    def close(self):
        """Closes the connection pool."""
        if self._connection and self._connection.closed == 0:
            self._connection.close()
