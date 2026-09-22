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
    HEADER = (By.CSS_SELECTOR, "header, .mobile-canvas-frame header")
    USER_PHONE_LABEL = (By.XPATH, "//header//*[contains(text(), '+91') or contains(text(), 'Fleet')]")
    WALLET_BADGE = (By.XPATH, "//header//*[contains(text(), '₹') or contains(text(), '2,450')]")
    PROFILE_BTN = (By.XPATH, "//header//button[.//img or contains(@aria-label, 'Profile') or contains(., '+91') or position()=1]")
    NOTIFICATION_BTN = (By.XPATH, "//header//button[contains(@aria-label, 'Notifications') or .//*[name()='svg' and contains(@class, 'lucide-bell')]]")

    # AI Search Module
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Ask ChargeWise AI'], input[placeholder*='Search']")
    SEARCH_SUBMIT_BTN = (By.XPATH, "//input[contains(@placeholder, 'Ask')]/following-sibling::button | //button[contains(., 'Search') or .//*[name()='svg']]")
    CURRENT_LOCATION_LABEL = (By.XPATH, "//*[contains(text(), 'Current Location') or contains(text(), 'T. Nagar')]")

    # Profile Drawer / Modal Elements
    PROFILE_DRAWER = (By.XPATH, "//*[contains(text(), 'Driver Profile') or contains(text(), 'Fleet Driver')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(., 'Sign Out') or contains(., 'Logout')]")
    DRAWER_CLOSE_BTN = (By.XPATH, "//button[contains(., '✕') or .//*[name()='svg' and contains(@class, 'lucide-x')]]")

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

    def open_profile(self) -> None:
        """Opens user profile drawer."""
        self.click(self.PROFILE_BTN)

    def logout(self) -> None:
        """Logs out from profile drawer."""
        self.open_profile()
        self.click(self.LOGOUT_BTN)
