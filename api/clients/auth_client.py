"""
API Client for Authentication and User Profile operations.
"""
from typing import Dict, Any, Optional
import requests
from api.clients.base_client import BaseAPIClient
from config.settings import settings


class AuthAPIClient(BaseAPIClient):
    """Client for user authentication, registration, and profile endpoints."""

    def __init__(self, base_url: str = settings.app.API_URL):
        super().__init__(base_url)

    def login(self, username: str = settings.auth.USER_USERNAME, password: str = settings.auth.USER_PASSWORD) -> requests.Response:
        """Executes credential authentication request."""
        payload = {"username": username, "password": password}
        return self.post("auth/login", json_data=payload)

    def register(self, email: str, password: str, full_name: str, vehicle_model: str = "Tesla Model 3") -> requests.Response:
        """Registers a new EV driver account."""
        payload = {
            "email": email,
            "password": password,
            "fullName": full_name,
            "vehicleModel": vehicle_model,
            "batteryCapacityKwh": 60,
            "preferredConnector": "CCS2"
        }
        return self.post("auth/register", json_data=payload)

    def get_profile(self) -> requests.Response:
        """Retrieves authenticated user profile."""
        return self.get("users/me")
