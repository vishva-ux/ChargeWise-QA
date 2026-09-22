"""
Base Page Object providing reusable interactions, explicit waits, and resilient locator strategies.
"""
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects in the ChargeWise QA framework."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to(self, url: str) -> None:
        """Navigates to the specified URL."""
        logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def get_title(self) -> str:
        """Returns the current page title."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        return self.driver.current_url

    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Finds an element with explicit wait for visibility."""
        wait_time = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time}s: {locator}")
            raise

    def find_present_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Finds an element with explicit wait for presence in DOM."""
        wait_time = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not present in DOM within {wait_time}s: {locator}")
            raise

    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """Finds all matching elements once at least one is present."""
        wait_time = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            logger.warning(f"No elements found within {wait_time}s: {locator}")
            return []

    def click(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """Waits for element to be clickable and clicks it."""
        wait_time = timeout if timeout is not None else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.debug(f"Clicked element: {locator}")
        except StaleElementReferenceException:
            logger.warning(f"Stale element encountered on {locator}. Retrying click...")
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()

    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """Waits for element, optionally clears, and sends keys."""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.debug(f"Entered text '{text}' into element: {locator}")

    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """Extracts visible text from an element."""
        element = self.find_element(locator, timeout)
        return element.text.strip()

    def is_visible(self, locator: Tuple[str, str], timeout: int = 4) -> bool:
        """Checks if an element is visible within a brief timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_present(self, locator: Tuple[str, str], timeout: int = 4) -> bool:
        """Checks if an element is present in the DOM."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_into_view(self, locator: Tuple[str, str]) -> None:
        """Scrolls the page until the element is in view."""
        element = self.find_present_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
