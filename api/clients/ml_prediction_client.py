"""
API Client for ChargeWise Machine Learning Microservice (FastAPI).
"""
from typing import Optional, Dict, Any, List
import requests
from api.clients.base_client import BaseAPIClient
from config.settings import settings


class MLPredictionClient(BaseAPIClient):
    """Client for XGBoost & Scikit-learn predictive model endpoints."""

    def __init__(self, base_url: str = settings.app.ML_URL):
        super().__init__(base_url)

    def get_health(self) -> requests.Response:
        """GET /health"""
        return self.get("health")

    def predict_waiting_time(
        self,
        day_of_week: int,
        hour_of_day: int,
        total_chargers: int,
        current_occupancy: int,
        expected_status: Optional[int] = None
    ) -> requests.Response:
        """POST /predict/waiting-time"""
        payload = {
            "day_of_week": day_of_week,
            "hour_of_day": hour_of_day,
            "total_chargers": total_chargers,
            "current_occupancy": current_occupancy
        }
        return self.post("predict/waiting-time", json_data=payload, expected_status=expected_status)

    def recommend_stations(
        self,
        user_lat: float,
        user_lng: float,
        stations: List[Dict[str, Any]],
        battery_soc: float = 30.0,
        preferred_connector: str = "CCS2"
    ) -> requests.Response:
        """POST /recommend/stations"""
        payload = {
            "user_lat": user_lat,
            "user_lng": user_lng,
            "battery_soc": battery_soc,
            "preferred_connector": preferred_connector,
            "stations": stations
        }
        return self.post("recommend/stations", json_data=payload)

    def predict_peak_hours(self, hour: int, day: int) -> requests.Response:
        """POST /predict/peak-hours"""
        payload = {"hour": hour, "day": day}
        return self.post("predict/peak-hours", json_data=payload)

    def recommend_battery_aware(
        self,
        current_soc: float,
        battery_capacity_kwh: float,
        destination_distance_km: float,
        expected_status: Optional[int] = None
    ) -> requests.Response:
        """POST /recommend/battery-aware"""
        payload = {
            "current_soc": current_soc,
            "battery_capacity_kwh": battery_capacity_kwh,
            "destination_distance_km": destination_distance_km
        }
        return self.post("recommend/battery-aware", json_data=payload, expected_status=expected_status)
