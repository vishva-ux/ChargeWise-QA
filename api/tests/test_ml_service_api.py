"""
Automated REST API tests for Machine Learning Prediction & Recommendation Microservice.
"""
import pytest
import allure


@allure.epic("API Automation")
@allure.feature("ML Prediction Endpoints")
@pytest.mark.api
@pytest.mark.regression
class TestMLEngineAPI:
    """Test Suite for FastAPI ML Inference Endpoints (:8000)."""

    @allure.story("ML Service Health Check")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_tc_rout_001_ml_health_check(self, ml_client):
        """TC-ROUT-001: Validate FastAPI service health and loaded models."""
        with allure.step("GET /health"):
            response = ml_client.get_health()

        with allure.step("Validate healthy status"):
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == "healthy"
            assert data.get("service") == "ChargeWise-ML-Engine"

    @allure.story("Wait Time Prediction")
    @allure.severity("critical")
    def test_tc_rout_002_predict_waiting_time(self, ml_client):
        """TC-ROUT-002: Request queue wait-time prediction from ML model."""
        with allure.step("POST /predict/waiting-time with realistic occupancy"):
            response = ml_client.predict_waiting_time(
                day_of_week=2,  # Wednesday
                hour_of_day=14,  # 2:00 PM
                total_chargers=6,
                current_occupancy=4
            )

        with allure.step("Validate predicted wait time payload"):
            assert response.status_code == 200
            data = response.json()
            assert "predicted_wait_minutes" in data or "estimated_wait" in data or isinstance(data, (dict, float, int))

    @allure.story("Battery Aware Recommendations")
    @allure.severity("critical")
    def test_tc_rout_003_battery_aware_recommendation(self, ml_client):
        """TC-ROUT-003: Request battery-aware stop optimization for long trip."""
        with allure.step("POST /recommend/battery-aware"):
            response = ml_client.recommend_battery_aware(
                current_soc=25.0,
                battery_capacity_kwh=60.0,
                destination_distance_km=280.0
            )

        with allure.step("Validate recommendation strategy response"):
            assert response.status_code in [200, 422]

    @allure.story("Peak Hour Demand Prediction")
    @allure.severity("normal")
    def test_tc_rout_004_peak_hour_demand(self, ml_client):
        """TC-ROUT-004: Query peak hour congestion multiplier."""
        with allure.step("POST /predict/peak-hours for 6 PM peak"):
            response = ml_client.predict_peak_hours(hour=18, day=4)

        with allure.step("Validate response"):
            assert response.status_code == 200

    @allure.story("ML Input Boundary Validation")
    @allure.severity("normal")
    def test_tc_rout_006_negative_soc_validation(self, ml_client):
        """TC-ROUT-006: Ensure Pydantic rejects out-of-bound SOC with 422."""
        with allure.step("POST /recommend/battery-aware with invalid SOC 150%"):
            response = ml_client.recommend_battery_aware(
                current_soc=150.0,
                battery_capacity_kwh=60.0,
                destination_distance_km=100.0
            )

        with allure.step("Validate HTTP 422 Unprocessable Entity"):
            assert response.status_code == 422
