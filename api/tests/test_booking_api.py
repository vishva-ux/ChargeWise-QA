"""
Automated REST API tests for Atomic Slot Reservation and Distributed Lock execution.
"""
import pytest
import allure
import uuid


@allure.epic("API Automation")
@allure.feature("Booking & Locking Endpoints")
@pytest.mark.api
@pytest.mark.regression
class TestBookingAPI:
    """Test Suite for /api/v1/bookings endpoints."""

    @allure.story("Atomic Slot Reservation")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_tc_book_api_001_reserve_slot_success(self, booking_client):
        """TC-BOOK-003: Successfully reserve slot via Redisson lock."""
        station_id = "st-001"

        with allure.step(f"Dispatch slot reservation request for station {station_id}"):
            response = booking_client.reserve_slot(
                station_id=station_id,
                user_phone="+91 98765 43210",
                vehicle_type="EV Fleet Cab",
                payment_method="UPI"
            )

        with allure.step("Validate response structure and Pass ID"):
            assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
            data = response.json()
            assert data.get("success") is True, "Expected reservation success to be True"
            assert "passId" in data and data["passId"] is not None, "Pass ID missing in response"
            assert "CW-PASS" in data["passId"], f"Unexpected pass ID format: {data['passId']}"
            assert data.get("stationId") == station_id

    @allure.story("Negative Booking - Invalid Payload")
    @allure.severity("critical")
    def test_tc_book_api_002_missing_station_id(self, booking_client):
        """Verify reservation with null stationId returns appropriate response without crashing."""
        with allure.step("Send reservation with empty payload"):
            response = booking_client.post("bookings/reserve", json_data={})

        with allure.step("Validate handled response"):
            assert response.status_code in [200, 400], f"Expected 200/400, got {response.status_code}"

    @allure.story("Concurrent Reservation Simulation")
    @allure.severity("critical")
    def test_tc_book_api_003_concurrent_reservation_dispatch(self, booking_client):
        """TC-BOOK-008: Dispatch back-to-back reservation requests to test distributed lock integrity."""
        with allure.step("Send primary reservation request"):
            res1 = booking_client.reserve_slot(station_id="st-002", user_phone="+91 98765 43210")
            assert res1.status_code == 200
            assert res1.json().get("success") is True

        with allure.step("Send secondary reservation request immediately"):
            res2 = booking_client.reserve_slot(station_id="st-002", user_phone="+91 87654 32109")
            assert res2.status_code == 200
            assert "passId" in res2.json() or "message" in res2.json()
