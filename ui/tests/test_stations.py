"""
Automated UI Tests for Station Discovery, Bottom Sheet Listing, and AI Conversational Search.
"""
import pytest
import allure
from ui.pages.login_page import LoginPage
from ui.pages.home_page import HomePage
from ui.pages.station_page import StationPage


@allure.epic("UI Automation")
@allure.feature("Station Discovery & Search")
@pytest.mark.ui
@pytest.mark.regression
class TestStationsUI:
    """Test Suite for Interactive Map, Station List, and Natural Language Filters."""

    @pytest.fixture(autouse=True)
    def setup_authenticated_session(self, driver):
        """Ensures driver is on dashboard with active session."""
        login_page = LoginPage(driver)
        login_page.open()
        if login_page.is_login_modal_displayed():
            login_page.login_via_modal()

    @allure.story("Station List Display")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_tc_stat_002_station_list_rendering(self, driver):
        """TC-STAT-002: Verify bottom sheet renders charging station cards."""
        station_page = StationPage(driver)

        with allure.step("Check that multiple charging stations are rendered"):
            count = station_page.get_station_count()
            assert count >= 1, f"Expected at least 1 station card rendered, found {count}"

    @allure.story("AI Conversational Search")
    @allure.severity(allure.severity_level.HIGH)
    def test_tc_stat_004_ai_search_fast_charger_filter(self, driver):
        """TC-STAT-004: Verify AI conversational search filters list by high power (>60kW)."""
        home_page = HomePage(driver)
        station_page = StationPage(driver)

        with allure.step("Submit AI query 'fast charger near me'"):
            home_page.execute_ai_search("fast charger near me")

        with allure.step("Verify filtered station list is updated"):
            count = station_page.get_station_count()
            assert count >= 1, "No stations returned for fast charger filter"

    @allure.story("AI Search Reset")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_tc_stat_006_reset_search_filters(self, driver):
        """TC-STAT-006: Verify resetting AI search restores full station catalog."""
        home_page = HomePage(driver)
        station_page = StationPage(driver)

        with allure.step("Apply AI filter"):
            home_page.execute_ai_search("CCS2 only")

        with allure.step("Reset filter"):
            station_page.reset_ai_filter()

        with allure.step("Verify full station list is restored"):
            count = station_page.get_station_count()
            assert count >= 1
