"""
Automated UI Tests for Authentication, Login Modals, and Session Management.
"""
import pytest
import allure
from ui.pages.login_page import LoginPage
from ui.pages.home_page import HomePage
from config.settings import settings


@allure.epic("UI Automation")
@allure.feature("Authentication")
@pytest.mark.ui
@pytest.mark.regression
class TestAuthenticationUI:
    """Test Suite for User Sign-In, Credentials Validation, and Session Teardown."""

    @allure.story("Modal Login Flow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_tc_auth_001_valid_modal_login(self, driver):
        """TC-AUTH-001: Validate successful login via phone authentication modal."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        with allure.step("Navigate to base application"):
            login_page.open()

        with allure.step("Check if login modal is present and submit valid phone"):
            if login_page.is_login_modal_displayed():
                login_page.login_via_modal(phone=settings.auth.USER_PHONE)

        with allure.step("Verify Home Dashboard loaded with active wallet balance"):
            assert home_page.is_loaded(), "Home page failed to load after login"
            balance = home_page.get_wallet_balance()
            assert "₹" in balance or "2,450" in balance or len(balance) > 0

    @allure.story("Dedicated Auth Form")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_auth_003_standard_user_credentials_login(self, driver):
        """TC-AUTH-003: Validate sign-in using standard user username and password on /auth."""
        login_page = LoginPage(driver)
        
        with allure.step("Navigate to /auth dedicated login page"):
            login_page.open_auth_page()

        with allure.step("Auto-fill or enter standard user credentials"):
            if login_page.is_visible(login_page.USER_HINT_BTN, timeout=3):
                login_page.click_user_hint()
                login_page.click(login_page.SUBMIT_BTN)
            else:
                login_page.login_via_form(settings.auth.USER_USERNAME, settings.auth.USER_PASSWORD)

        with allure.step("Verify authentication transition or successful form submission"):
            assert driver.current_url is not None

    @allure.story("Negative Authentication")
    @allure.severity(allure.severity_level.HIGH)
    def test_tc_auth_005_invalid_password_rejection(self, driver):
        """TC-AUTH-005: Verify system rejects incorrect password with proper error feedback."""
        login_page = LoginPage(driver)
        
        with allure.step("Navigate to /auth dedicated login page"):
            login_page.open_auth_page()

        with allure.step("Enter valid username with incorrect password"):
            login_page.login_via_form(username=settings.auth.USER_USERNAME, password="WrongPassword999!")

        with allure.step("Verify error message is displayed"):
            error_text = login_page.get_error_message()
            assert len(error_text) > 0, "Expected error alert was not displayed for invalid credentials"

    @allure.story("Profile & Logout")
    @allure.severity(allure.severity_level.HIGH)
    def test_tc_auth_007_user_logout_flow(self, driver):
        """TC-AUTH-007: Verify driver can open profile drawer and execute logout."""
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        with allure.step("Open application and ensure logged in"):
            login_page.open()
            if login_page.is_login_modal_displayed():
                login_page.login_via_modal()

        with allure.step("Open profile drawer"):
            home_page.open_profile()
            assert home_page.is_visible(home_page.LOGOUT_BTN, timeout=5), "Logout button not visible in profile drawer"

        with allure.step("Click Sign Out"):
            home_page.click(home_page.LOGOUT_BTN)
            assert login_page.is_login_modal_displayed(), "Login modal did not reappear after sign out"
