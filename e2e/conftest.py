"""
PyTest fixtures for End-to-End multi-tier integration testing.
Combines UI WebDriver, API clients, and Database client.
"""
import pytest
from api.clients.station_client import StationAPIClient
from api.clients.booking_client import BookingAPIClient
from database.db_client import DatabaseClient


@pytest.fixture(scope="session")
def e2e_station_api():
    return StationAPIClient()


@pytest.fixture(scope="session")
def e2e_booking_api():
    return BookingAPIClient()


@pytest.fixture(scope="session")
def e2e_db_client():
    client = DatabaseClient()
    yield client
    client.close()
