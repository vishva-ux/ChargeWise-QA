"""
API Client for Charging Station Discovery and Geospatial Queries.
"""
from typing import Optional, Dict, Any
import requests
from api.clients.base_client import BaseAPIClient
from config.settings import settings


class StationAPIClient(BaseAPIClient):
    """Client for Station discovery and geospatial search endpoints."""

    def __init__(self, base_url: str = settings.app.API_URL):
        super().__init__(base_url)

    def get_nearby_stations(
        self,
        lat: float = 13.0418,
        lng: float = 80.2341,
        radius_km: float = 50.0,
        expected_status: Optional[int] = None
    ) -> requests.Response:
        """
        Executes PostGIS ST_DWithin geospatial query for stations.
        Target endpoint: GET /api/v1/stations/nearby
        """
        params = {
            "lat": lat,
            "lng": lng,
            "radiusKm": radius_km
        }
        return self.get("stations/nearby", params=params, expected_status=expected_status)

    def get_station_details(self, station_id: str) -> requests.Response:
        """Fetches detailed specifications and live port availability for a station."""
        return self.get(f"stations/{station_id}")
