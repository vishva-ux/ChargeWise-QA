"""
Station Page Object representing BottomSheet station list, details, and selection.
"""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from ui.pages.base_page import BasePage


class StationPage(BasePage):
    """Page Object for station discovery, cards, and bottom sheet list."""

    # Bottom Sheet Elements
    BOTTOM_SHEET = (By.XPATH, "//*[contains(text(), 'Nearby Charging Hubs') or contains(@class, 'rounded-t-3xl')]")
    STATION_CARDS = (By.XPATH, "//div[contains(@class, 'rounded-2xl') and (.//*[contains(text(), 'kW')] or .//*[contains(text(), 'BOOK SLOT')])]")
    FIRST_STATION_TITLE = (By.XPATH, "(//div[contains(@class, 'rounded-2xl')]//h4)[1]")
    
    # Card Specific Actions
    BOOK_SLOT_BTN = (By.XPATH, "(//button[contains(., 'BOOK SLOT') or contains(., 'RESERVE')])[1]")
    RESET_FILTER_BTN = (By.XPATH, "//button[contains(text(), 'Clear') or contains(text(), 'Reset')]")
    AI_FILTER_BANNER = (By.XPATH, "//*[contains(text(), 'Route Optimizer Summary') or contains(text(), 'AI Filter')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def get_station_count(self) -> int:
        """Returns the number of station cards currently rendered."""
        cards = self.find_elements(self.STATION_CARDS, timeout=8)
        return len(cards)

    def select_station_by_name(self, name: str) -> None:
        """Clicks a station card matching the given name."""
        locator = (By.XPATH, f"//div[contains(@class, 'rounded-2xl') and .//*[contains(text(), '{name}')]]")
        self.click(locator)

    def click_reserve_on_first_station(self) -> None:
        """Clicks the BOOK SLOT button on the first station card."""
        self.click(self.BOOK_SLOT_BTN)

    def reset_ai_filter(self) -> None:
        """Resets conversational AI filter if active."""
        if self.is_visible(self.RESET_FILTER_BTN, timeout=3):
            self.click(self.RESET_FILTER_BTN)
