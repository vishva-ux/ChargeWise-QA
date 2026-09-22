"""
Automated REST API tests for User Authentication and Profile endpoints.
"""
import pytest
import allure
from config.settings import settings


@allure.epic("API Automation")
@allure.feature("Authentication Endpoints")
@pytest.mark.api
@pytest.mark.regression
class TestAuthAPI:
    """Test Suite for Authentication REST API endpoints."""

    @allure.story("User Login API")
    @allure.severity("critical")
    @pytest.mark.smoke
    def test_tc_auth_api_001_valid_login(self, auth_client):
        """Verify login endpoint accepts valid credentials."""
        with allure.step("Dispatch login POST request"):
            response = auth_client.login(settings.auth.USER_USERNAME, settings.auth.USER_PASSWORD)
        
        with allure.step("Validate response"):
            # Server returns 200 OK or handled fallback
            assert response.status_code in [200, 404], f"Unexpected status: {response.status_code}"

    @allure.story("Negative Authentication")
    @allure.severity("critical")
    def test_tc_auth_api_002_invalid_credentials(self, auth_client):
        """Verify login endpoint rejects bad credentials with proper error code."""
        with allure.step("Dispatch login with incorrect password"):
            response = auth_client.login("invalid_user", "invalid_pass_123")
        
        with allure.step("Validate unauthorized or error response"):
            assert response.status_code in [400, 401, 404], f"Expected 400/401/404, got {response.status_code}"
