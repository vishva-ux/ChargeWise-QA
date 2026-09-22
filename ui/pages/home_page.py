"""
Home Page Object representing the main map interface and floating modules.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from ui.pages.base_page import BasePage
from config.settings import settings


class HomePage(BasePage):
    """Page Object for ChargeWise Main Dashboard & Navigation."""

    # Header Elements
    HEADER = (By.CSS_SELECTOR, "header")
    WALLET_BADGE = (By.XPATH, "//header//*[contains(text(), '₹')]")
    PROFILE_BTN = (By.XPATH, "//header//button[@title='Account Profile & Logout' or .//*[name()='svg' and contains(@class, 'lucide-user')]]")
    NOTIFICATION_BTN = (By.XPATH, "//header//button[@title='Notifications']")

    # AI Search Module
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Where to'], input[placeholder*='Ask']")
    SEARCH_SUBMIT_BTN = (By.XPATH, "//button[@title='Search EV Stations' or @type='submit']")
    FAST_CCS2_CHIP = (By.XPATH, "//button[contains(., 'Fast CCS2 Hubs')]")
    ROUTE_CHIP = (By.XPATH, "//button[contains(., 'Chennai ➔ Blr Route')]")

    # Profile Drawer / Modal Elements
    PROFILE_DRAWER = (By.XPATH, "//*[contains(text(), 'Rapido Driver Profile') or contains(text(), 'Driver Profile')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(., 'LOGOUT') or contains(., 'Sign Out')]")

    # Map Canvas
    MAP_CONTAINER = (By.CSS_SELECTOR, ".leaflet-container, [id*='map'], .map-viewport")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = settings.app.BASE_URL

    def is_loaded(self) -> bool:
        """Verifies if Home Map interface is loaded."""
        return self.is_visible(self.HEADER, timeout=8) or self.is_visible(self.SEARCH_INPUT, timeout=8)

    def get_wallet_balance(self) -> str:
        """Returns displayed wallet balance string."""
        return self.get_text(self.WALLET_BADGE, timeout=5)

    def execute_ai_search(self, query: str) -> None:
        """Enters prompt into AI natural language search box and submits."""
        self.send_keys(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_SUBMIT_BTN)

    def click_fast_charger_chip(self) -> None:
        """Clicks the Fast CCS2 Hubs preset chip."""
        self.click(self.FAST_CCS2_CHIP)

    def open_profile(self) -> None:
        """Opens user profile drawer."""
        self.click(self.PROFILE_BTN)

    def logout(self) -> None:
        """Logs out from profile drawer."""
        self.open_profile()
        self.click(self.LOGOUT_BTN)
