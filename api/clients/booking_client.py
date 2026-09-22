"""
API Client for Slot Booking, Atomic Reservation, and Cancellation.
"""
from typing import Optional, Dict, Any
import requests
from api.clients.base_client import BaseAPIClient
from config.settings import settings


class BookingAPIClient(BaseAPIClient):
    """Client for Booking & Redisson lock reservation endpoints."""

    def __init__(self, base_url: str = settings.app.API_URL):
        super().__init__(base_url)

    def reserve_slot(
        self,
        station_id: str,
        user_phone: str = settings.auth.USER_PHONE,
        vehicle_type: str = "EV Fleet Cab",
        payment_method: str = "UPI",
        expected_status: Optional[int] = None
    ) -> requests.Response:
        """
        Executes atomic slot reservation via Redisson lock.
        Target endpoint: POST /api/v1/bookings/reserve
        """
        payload = {
            "stationId": station_id,
            "userPhone": user_phone,
            "vehicleType": vehicle_type,
            "paymentMethod": payment_method
        }
        return self.post("bookings/reserve", json_data=payload, expected_status=expected_status)

    def get_my_bookings(self, user_phone: Optional[str] = None) -> requests.Response:
        """Fetches active and historical bookings for the user."""
        params = {"userPhone": user_phone} if user_phone else None
        return self.get("bookings/my-reservations", params=params)

    def cancel_booking(self, pass_id: str) -> requests.Response:
        """Cancels active reservation and releases slot lock."""
        return self.post(f"bookings/{pass_id}/cancel")
