"""
PyTest fixtures for API Automation testing tier.
"""
import pytest
from api.clients.auth_client import AuthAPIClient
from api.clients.station_client import StationAPIClient
from api.clients.booking_client import BookingAPIClient
from api.clients.ml_prediction_client import MLPredictionClient


@pytest.fixture(scope="session")
def auth_client():
    """Session-scoped Auth API client."""
    return AuthAPIClient()


@pytest.fixture(scope="session")
def station_client():
    """Session-scoped Station discovery API client."""
    return StationAPIClient()


@pytest.fixture(scope="session")
def booking_client():
    """Session-scoped Booking API client."""
    return BookingAPIClient()


@pytest.fixture(scope="session")
def ml_client():
    """Session-scoped Machine Learning API client."""
    return MLPredictionClient()


@pytest.fixture
def sample_station_payload():
    """Returns sample station data for ML recommendation requests."""
    return [
        {
            "id": "st-001",
            "name": "Relux Fast Charge - T. Nagar Node",
            "max_power_kw": 120.0,
            "price_per_kwh": 18.5,
            "distance_km": 1.2,
            "rating": 4.8,
            "predicted_wait_minutes": 4.0,
            "connector_type": "CCS2"
        },
        {
            "id": "st-002",
            "name": "Tata Power EZ Charge - Sriperumbudur Hub",
            "max_power_kw": 60.0,
            "price_per_kwh": 16.0,
            "distance_km": 34.5,
            "rating": 4.7,
            "predicted_wait_minutes": 12.0,
            "connector_type": "CCS2"
        }
    ]
