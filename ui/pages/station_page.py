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
    BOTTOM_SHEET = (By.XPATH, "//*[contains(@class, 'bottom-sheet') or contains(@class, 'rounded-t-3xl') or contains(., 'Available Stations')]")
    STATION_CARDS = (By.XPATH, "//div[contains(@class, 'rounded-2xl') and (.//*[contains(text(), 'kW')] or .//*[contains(text(), '₹')])]")
    FIRST_STATION_TITLE = (By.XPATH, "(//div[contains(@class, 'rounded-2xl')]//h3 | //div[contains(@class, 'rounded-2xl')]//h4 | //div[contains(@class, 'rounded-2xl')]//span[contains(@class, 'font-bold')])[1]")
    
    # Card Specific Actions
    RESERVE_BTN = (By.XPATH, "//button[contains(., 'RESERVE SLOT') or contains(., 'Book') or contains(., 'Reserve')]")
    RESET_FILTER_BTN = (By.XPATH, "//button[contains(., 'Reset') or contains(., 'Clear')]")
    AI_FILTER_BADGE = (By.XPATH, "//*[contains(text(), 'AI Filter') or contains(text(), 'Showing')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def get_station_count(self) -> int:
        """Returns the number of station cards currently rendered."""
        cards = self.find_elements(self.STATION_CARDS, timeout=6)
        return len(cards)

    def select_station_by_name(self, name: str) -> None:
        """Clicks a station card matching the given name."""
        locator = (By.XPATH, f"//div[contains(@class, 'rounded-2xl') and .//*[contains(text(), '{name}')]]")
        self.click(locator)

    def click_reserve_on_first_station(self) -> None:
        """Clicks the RESERVE SLOT button on the currently active station card."""
        self.click(self.RESERVE_BTN)

    def reset_ai_filter(self) -> None:
        """Resets conversational AI filter if active."""
        if self.is_visible(self.RESET_FILTER_BTN, timeout=3):
            self.click(self.RESET_FILTER_BTN)
