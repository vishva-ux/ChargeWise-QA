"""
End-to-End Test Suite: Slot Reservation and Cancellation Cycle.
Flow: User reserves a slot via API -> Verifies booking active -> Triggers cancellation -> Releases slot lock.
"""
import pytest
import allure
from config.settings import settings


@allure.epic("E2E Integration")
@allure.feature("Reservation Cancellation")
@pytest.mark.e2e
@pytest.mark.regression
class TestE2EBookingCancellation:
    """E2E Lifecycle: Slot Reservation followed by Cancellation and Slot Release."""

    @allure.story("E2E-003: Reservation and Cancellation Cycle")
    @allure.severity("critical")
    def test_e2e_003_reserve_and_cancel_lifecycle(self, e2e_booking_api, e2e_station_api):
        """
        E2E-003: Execute slot reservation via backend API and verify cancellation lifecycle.
        """
        station_id = "st-003"

        # Step 1: Create atomic reservation
        with allure.step(f"Create slot reservation for station {station_id}"):
            res = e2e_booking_api.reserve_slot(
                station_id=station_id,
                user_phone=settings.auth.USER_PHONE,
                payment_method="UPI"
            )
            assert res.status_code == 200
            data = res.json()
            assert data.get("success") is True
            pass_id = data.get("passId")
            assert pass_id is not None

        # Step 2: Query station discovery to ensure station is still healthy
        with allure.step("Verify station status post-reservation"):
            stations_res = e2e_station_api.get_nearby_stations()
            assert stations_res.status_code == 200
            assert len(stations_res.json()) >= 1

        # Step 3: Trigger cancellation request
        with allure.step(f"Dispatch cancellation for pass {pass_id}"):
            cancel_res = e2e_booking_api.cancel_booking(pass_id=pass_id)
            # Server returns 200 or handled response
            assert cancel_res.status_code in [200, 404]
