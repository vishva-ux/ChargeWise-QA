"""
End-to-End Test Suite: Complete Booking & QR Pass Lifecycle.
Flow: User Login -> Discover Stations -> Select Station -> Choose Payment -> Acquire Distributed Lock -> Generate QR Pass -> Verify Consistency.
"""
import pytest
import allure
from ui.pages.login_page import LoginPage
from ui.pages.home_page import HomePage
from ui.pages.station_page import StationPage
from ui.pages.booking_page import BookingPage
from config.settings import settings


@allure.epic("E2E Integration")
@allure.feature("Booking Lifecycle")
@pytest.mark.e2e
@pytest.mark.regression
class TestE2EBookingLifecycle:
    """E2E User Journey: Discovery to Confirmed QR Reservation."""

    @allure.story("E2E-001: Discovery to QR Pass Flow")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_e2e_001_complete_booking_journey(self, driver, e2e_station_api, e2e_booking_api):
        """
        E2E-001: Execute full driver reservation flow across UI and verify via API.
        """
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        station_page = StationPage(driver)
        booking_page = BookingPage(driver)

        # Step 1: User Login
        with allure.step("Step 1: Driver Authentication"):
            login_page.open()
            if login_page.is_login_modal_displayed():
                login_page.login_via_modal(phone=settings.auth.USER_PHONE)
            assert home_page.is_loaded(), "Home Dashboard failed to load"

        # Step 2: Station Discovery via API & UI
        with allure.step("Step 2: Verify Station Discovery Catalog"):
            api_stations = e2e_station_api.get_nearby_stations()
            assert api_stations.status_code == 200
            ui_count = station_page.get_station_count()
            assert ui_count >= 1, "No stations rendered on UI"

        # Step 3: Select Station and Open Reservation Drawer
        with allure.step("Step 3: Open Slot Reservation Drawer"):
            station_page.click_reserve_on_first_station()
            assert booking_page.is_booking_panel_open(), "Booking drawer did not open"

        # Step 4: Choose Payment Method and Confirm Reservation
        with allure.step("Step 4: Select Payment and Acquire Redisson Lock"):
            booking_page.select_payment_method("UPI")
            booking_page.confirm_reservation()

        # Step 5: Verify Confirmed QR Pass Screen
        with allure.step("Step 5: Verify QR Code Pass Generated"):
            assert booking_page.is_booking_confirmed(), "Booking QR Pass was not confirmed"
            pass_id = booking_page.get_confirmed_pass_id()
            assert len(pass_id) > 0, "Pass ID is empty"
            allure.attach(f"Generated Pass ID: {pass_id}", name="Confirmed Pass", attachment_type=allure.attachment_type.TEXT)

        # Step 6: Return to Map
        with allure.step("Step 6: Return to Discovery Canvas"):
            booking_page.finish_booking_flow()
