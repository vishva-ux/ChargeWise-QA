"""
Automated REST API tests for Station Discovery and PostGIS Geospatial endpoints.
"""
import pytest
import allure


@allure.epic("API Automation")
@allure.feature("Station Discovery Endpoints")
@pytest.mark.api
@pytest.mark.regression
class TestStationAPI:
    """Test Suite for /api/v1/stations endpoints."""

    @allure.story("Nearby Station Discovery")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_tc_stat_api_001_get_nearby_stations(self, station_client):
        """TC-STAT-001: Fetch stations using coordinates around Chennai corridor."""
        with allure.step("Send GET /api/v1/stations/nearby"):
            response = station_client.get_nearby_stations(lat=13.0418, lng=80.2341, radius_km=50.0)

        with allure.step("Validate status 200 and station payload"):
            assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
            stations = response.json()
            assert isinstance(stations, list), "Response body must be an array of stations"
            assert len(stations) > 0, "Expected at least 1 charging station in response"

            first_station = stations[0]
            assert "id" in first_station, "Station object missing 'id'"
            assert "name" in first_station, "Station object missing 'name'"
            assert "latitude" in first_station, "Station object missing 'latitude'"
            assert "longitude" in first_station, "Station object missing 'longitude'"
            assert "availablePorts" in first_station, "Station object missing 'availablePorts'"
            assert "pricePerKwh" in first_station, "Station object missing 'pricePerKwh'"

    @allure.story("Default Query Parameters")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_tc_stat_api_002_default_parameters(self, station_client):
        """Verify endpoint works with default parameters."""
        with allure.step("Send GET /api/v1/stations/nearby with no params"):
            response = station_client.get("stations/nearby")

        with allure.step("Validate response status 200"):
            assert response.status_code == 200
            stations = response.json()
            assert len(stations) >= 1

    @allure.story("Boundary Values")
    @allure.severity(allure.severity_level.LOW)
    def test_tc_stat_api_003_extreme_coordinates(self, station_client):
        """Verify API handles extreme float coordinates without crashing."""
        with allure.step("Send GET with boundary coordinates"):
            response = station_client.get_nearby_stations(lat=90.0, lng=180.0, radius_km=10.0)

        with allure.step("Validate server returns valid response without 500"):
            assert response.status_code in [200, 400], f"Unexpected 500 error: {response.status_code}"
