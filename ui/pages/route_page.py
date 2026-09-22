"""
Route Page Object representing the EV Route Planner interface.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from ui.pages.base_page import BasePage
from config.settings import settings


class RoutePage(BasePage):
    """Page Object for AI Route Planning and Battery Stop Optimization."""

    # Route Planner Elements
    ORIGIN_INPUT = (By.XPATH, "//input[@placeholder='Enter starting location' or contains(@placeholder, 'Origin')]")
    DESTINATION_INPUT = (By.XPATH, "//input[@placeholder='Enter destination city or landmark' or contains(@placeholder, 'Destination')]")
    SOC_INPUT = (By.XPATH, "//input[@type='number' or contains(@placeholder, 'SOC')]")
    PLAN_ROUTE_BTN = (By.XPATH, "//button[contains(., 'Calculate Smart Route') or contains(., 'Plan Route')]")
    STOP_CARDS = (By.XPATH, "//*[contains(@class, 'stop-card') or contains(., 'Stop 1') or contains(., 'Charging Stop')]")
    SUMMARY_METRICS = (By.XPATH, "//*[contains(text(), 'Total Trip Distance') or contains(text(), 'Est. Travel Time')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = f"{settings.app.BASE_URL}/route-planner"

    def open(self) -> "RoutePage":
        """Navigates to route planner page."""
        self.navigate_to(self.url)
        return self

    def plan_route(self, origin: str, destination: str, current_soc: int = 40) -> None:
        """Enters origin, destination, and battery SOC to compute route."""
        if self.is_visible(self.ORIGIN_INPUT, timeout=5):
            self.send_keys(self.ORIGIN_INPUT, origin)
            self.send_keys(self.DESTINATION_INPUT, destination)
            if self.is_visible(self.SOC_INPUT, timeout=2):
                self.send_keys(self.SOC_INPUT, str(current_soc))
            self.click(self.PLAN_ROUTE_BTN)
