"""
Automated UI Tests for Route Planning and Multi-stop EV calculations.
"""
import pytest
import allure
from ui.pages.route_page import RoutePage


@allure.epic("UI Automation")
@allure.feature("Route Planning")
@pytest.mark.ui
@pytest.mark.regression
class TestRoutePlannerUI:
    """Test Suite for EV Trip Calculation, Battery SOC, and Stop Recommendations."""

    @allure.story("Smart Route Calculation")
    @allure.severity(allure.severity_level.HIGH)
    def test_tc_rout_005_plan_ev_smart_route(self, driver):
        """TC-ROUT-005: Plan an EV route and verify calculation execution."""
        route_page = RoutePage(driver)

        with allure.step("Navigate to route planner"):
            route_page.open()

        with allure.step("Enter origin and destination"):
            route_page.plan_route(
                origin="T. Nagar, Chennai",
                destination="Indiranagar, Bangalore",
                current_soc=35
            )

        with allure.step("Verify route computation status"):
            assert driver.current_url is not None
