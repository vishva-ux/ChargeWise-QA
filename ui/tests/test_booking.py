"""
Automated UI Tests for Slot Reservation, Payment Selection, and QR Pass Generation.
"""
import pytest
import allure
from ui.pages.login_page import LoginPage
from ui.pages.station_page import StationPage
from ui.pages.booking_page import BookingPage


@allure.epic("UI Automation")
@allure.feature("Slot Reservation & Booking")
@pytest.mark.ui
@pytest.mark.regression
class TestBookingUI:
    """Test Suite for UI Reservation Drawer, Payment Methods, and QR Code Validation."""

    @pytest.fixture(autouse=True)
    def setup_authenticated_session(self, driver):
        """Ensures driver is logged in."""
        login_page = LoginPage(driver)
        login_page.open()
        if login_page.is_login_modal_displayed():
            login_page.login_via_modal()

    @allure.story("Open Reservation Drawer")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_tc_book_001_open_reservation_drawer(self, driver):
        """TC-BOOK-001: Validate clicking 'RESERVE SLOT' opens the reservation panel."""
        station_page = StationPage(driver)
        booking_page = BookingPage(driver)

        with allure.step("Click RESERVE SLOT on current active station"):
            station_page.click_reserve_on_first_station()

        with allure.step("Verify reservation drawer is displayed"):
            assert booking_page.is_booking_panel_open(), "Reservation drawer did not open"

    @allure.story("Payment Selection & Confirmation")
    @allure.severity("critical")
    def test_tc_book_004_complete_reservation_and_verify_qr_pass(self, driver):
        """TC-BOOK-004: Select payment method, secure reservation, and verify QR pass generation."""
        station_page = StationPage(driver)
        booking_page = BookingPage(driver)

        with allure.step("Open reservation drawer"):
            station_page.click_reserve_on_first_station()
            assert booking_page.is_booking_panel_open()

        with allure.step("Select EV Fleet Wallet payment method"):
            booking_page.select_payment_method("FLEET_WALLET")

        with allure.step("Click Proceed to Secure Reservation"):
            booking_page.confirm_reservation()

        with allure.step("Verify QR Pass confirmation panel appears with pass code"):
            assert booking_page.is_booking_confirmed(), "Booking confirmation panel did not display"
            pass_id = booking_page.get_confirmed_pass_id()
            assert "PASS" in pass_id or len(pass_id) > 0, f"Invalid pass identifier: {pass_id}"

        with allure.step("Click Done to return to Discovery Map"):
            booking_page.finish_booking_flow()
            assert not booking_page.is_booking_confirmed()
