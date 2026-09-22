"""
Booking Page Object encapsulating Slot Reservation drawer and QR Pass validation.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from ui.pages.base_page import BasePage


class BookingPage(BasePage):
    """Page Object for Slot Reservation Drawer and QR Pass Confirmation Panel."""

    # Panel B: Reservation Drawer Elements
    BOOKING_PANEL = (By.XPATH, "//*[contains(text(), 'SELECT PAYMENT METHOD') or contains(text(), 'Smart Slot Reservation') or contains(text(), 'RESERVATION')]")
    UPI_RADIO = (By.XPATH, "//label[.//div[contains(text(), 'UPI')]]//input[@type='radio'] | //label[contains(., 'UPI')]")
    WALLET_RADIO = (By.XPATH, "//label[.//div[contains(text(), 'Wallet')]]//input[@type='radio'] | //label[contains(., 'Wallet')]")
    CARD_RADIO = (By.XPATH, "//label[.//div[contains(text(), 'Credit') or contains(text(), 'Card')]]//input[@type='radio'] | //label[contains(., 'Card')]")
    
    PROCEED_RESERVE_BTN = (By.XPATH, "//button[contains(., 'PROCEED TO SECURE RESERVATION') or contains(., 'Pay & Confirm') or contains(., 'Securing')]")
    BACK_TO_DISCOVERY_BTN = (By.XPATH, "//button[contains(., 'Back') or contains(., 'Return')]")

    # Panel C: QR Pass View Elements
    CONFIRMATION_TITLE = (By.XPATH, "//*[contains(text(), 'Booking Confirmed') or contains(text(), 'Confirmed!')]")
    QR_SVG = (By.CSS_SELECTOR, "svg[role='img'], .p-4 svg, svg")
    PASS_ID_LABEL = (By.XPATH, "//span[contains(@class, 'font-mono') and (contains(text(), 'CW-PASS') or contains(text(), 'DEMO') or string-length(text()) > 5)]")
    DONE_BTN = (By.XPATH, "//button[contains(., 'Done & Return to Map') or contains(., 'Done & View My Bookings') or contains(., 'Done')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_booking_panel_open(self) -> bool:
        """Verifies if the reservation drawer is displayed."""
        return self.is_visible(self.BOOKING_PANEL, timeout=6)

    def select_payment_method(self, method: str = "UPI") -> None:
        """Selects payment option: 'UPI', 'WALLET', or 'CARD'."""
        if method.upper() == "UPI":
            self.click(self.UPI_RADIO)
        elif "WALLET" in method.upper():
            self.click(self.WALLET_RADIO)
        elif "CARD" in method.upper():
            self.click(self.CARD_RADIO)

    def confirm_reservation(self) -> None:
        """Clicks proceed button to acquire lock and finalize reservation."""
        self.click(self.PROCEED_RESERVE_BTN)

    def is_booking_confirmed(self) -> bool:
        """Verifies if QR confirmation screen is reached."""
        return self.is_visible(self.CONFIRMATION_TITLE, timeout=10)

    def get_confirmed_pass_id(self) -> str:
        """Extracts generated QR Pass identifier."""
        return self.get_text(self.PASS_ID_LABEL, timeout=8)

    def finish_booking_flow(self) -> None:
        """Closes QR pass and returns to map view."""
        self.click(self.DONE_BTN)
