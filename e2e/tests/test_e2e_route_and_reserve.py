"""
End-to-End Test Suite: AI Conversational Search to Station Reservation.
Flow: User Login -> Filter Stations via Natural Language AI -> Select Filtered Station -> Book Slot.
"""
import pytest
import allure
from ui.pages.login_page import LoginPage
from ui.pages.home_page import HomePage
from ui.pages.station_page import StationPage
from ui.pages.booking_page import BookingPage


@allure.epic("E2E Integration")
@allure.feature("AI Search & Booking")
@pytest.mark.e2e
@pytest.mark.regression
class TestE2EAISearchAndReserve:
    """E2E User Journey: Natural Language Query -> Filtered Reservation."""

    @allure.story("E2E-002: AI Filter to Reservation")
    @allure.severity("critical")
    def test_e2e_002_ai_search_and_reserve(self, driver):
        """
        E2E-002: Filter stations by AI conversational query and reserve the top recommended node.
        """
        login_page = LoginPage(driver)
        home_page = HomePage(driver)
        station_page = StationPage(driver)
        booking_page = BookingPage(driver)

        with allure.step("Authenticate driver"):
            login_page.open()
            if login_page.is_login_modal_displayed():
                login_page.login_via_modal()

        with allure.step("Submit AI query 'fast charger under 18'"):
            home_page.execute_ai_search("fast charger under 18")

        with allure.step("Open reservation drawer for recommended station"):
            station_page.click_reserve_on_first_station()
            assert booking_page.is_booking_panel_open()

        with allure.step("Select Fleet Wallet and Confirm"):
            booking_page.select_payment_method("FLEET_WALLET")
            booking_page.confirm_reservation()

        with allure.step("Verify QR Pass Confirmation"):
            assert booking_page.is_booking_confirmed()
            booking_page.finish_booking_flow()
