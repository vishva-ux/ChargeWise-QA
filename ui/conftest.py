"""
PyTest fixtures and WebDriver lifecycle management for UI Automation.
Includes automatic Allure failure screenshot hooks and browser configuration.
"""
import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import allure

from config.settings import settings


@pytest.fixture(scope="function")
def driver(request):
    """
    Initializes and manages the Selenium WebDriver instance.
    Automatically captures screenshot on failure and attaches to Allure report.
    """
    chrome_options = ChromeOptions()
    
    # Headless and CI Flags
    if settings.ui.HEADLESS:
        chrome_options.add_argument("--headless=new")
    
    chrome_options.add_argument(f"--window-size={settings.ui.WINDOW_WIDTH},{settings.ui.WINDOW_HEIGHT}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")

    # Initialize Driver with Manager
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        # Fallback to direct path or default system chromedriver
        chrome_options.add_argument("--headless=new")
        driver_instance = webdriver.Chrome(options=chrome_options)

    driver_instance.implicitly_wait(settings.ui.IMPLICIT_WAIT)
    driver_instance.set_page_load_timeout(settings.ui.PAGE_LOAD_TIMEOUT)

    # Yield driver instance to test
    yield driver_instance

    # Teardown: Capture screenshot if test failed and quit driver
    try:
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name
            screenshot_path = settings.paths.SCREENSHOT_DIR / f"{test_name}_{timestamp}.png"
            settings.paths.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            
            driver_instance.save_screenshot(str(screenshot_path))
            
            allure.attach(
                driver_instance.get_screenshot_as_png(),
                name=f"Failure_Screenshot_{test_name}",
                attachment_type=allure.attachment_type.PNG
            )
    except Exception:
        pass
    finally:
        driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test execution status for post-mortem screenshot capture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
