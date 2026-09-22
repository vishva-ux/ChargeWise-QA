"""
Login Page Object encapsulating Modal Login and Dedicated Auth Page interactions.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from ui.pages.base_page import BasePage
from config.settings import settings


class LoginPage(BasePage):
    """Page Object for ChargeWise Authentication interfaces."""

    # Modal Login Locators (Rapido Style Modal)
    PHONE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='98765 43210'], input[type='tel'], input[placeholder*='Phone']")
    VEHICLE_SELECT = (By.CSS_SELECTOR, "select, button[role='combobox']")
    MODAL_LOGIN_BTN = (By.XPATH, "//button[contains(., 'Continue to Fleet App') or contains(., 'Sign In') or contains(., 'Continue')]")
    VEHICLE_OPTION_CAB = (By.XPATH, "//option[contains(text(), 'EV Fleet Cab') or contains(text(), 'Cab')]")

    # Legacy / Dedicated Auth Page Locators (/auth)
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='user or admin' or @type='text']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SUBMIT_BTN = (By.XPATH, "//button[@type='submit' and contains(., 'Sign In')]")
    USER_HINT_BTN = (By.XPATH, "//button[contains(., 'user / user')]")
    ADMIN_HINT_BTN = (By.XPATH, "//button[contains(., 'admin / admin123')]")
    ERROR_ALERT = (By.CSS_SELECTOR, ".text-rose-600, .bg-rose-50, [role='alert']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.url = settings.app.BASE_URL

    def open(self) -> "LoginPage":
        """Opens the base application."""
        self.navigate_to(self.url)
        return self

    def open_auth_page(self) -> "LoginPage":
        """Navigates directly to the /auth route."""
        self.navigate_to(f"{self.url}/auth")
        return self

    def is_login_modal_displayed(self) -> bool:
        """Checks if login modal is currently displayed."""
        return self.is_visible(self.PHONE_INPUT, timeout=5)

    def login_via_modal(self, phone: str = "+91 98765 43210") -> None:
        """Submits login via modal prompt."""
        if self.is_visible(self.PHONE_INPUT, timeout=5):
            self.send_keys(self.PHONE_INPUT, phone)
            self.click(self.MODAL_LOGIN_BTN)

    def login_via_form(self, username: str, password: str) -> None:
        """Submits username and password on standard login form."""
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BTN)

    def click_user_hint(self) -> None:
        """Auto-fills test user credentials via hint card."""
        self.click(self.USER_HINT_BTN)

    def click_admin_hint(self) -> None:
        """Auto-fills admin credentials via hint card."""
        self.click(self.ADMIN_HINT_BTN)

    def get_error_message(self) -> str:
        """Returns visible error text if login failed."""
        return self.get_text(self.ERROR_ALERT, timeout=5)
