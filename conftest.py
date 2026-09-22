"""
Root PyTest configuration and Allure Environment Properties Generator.
"""
import os
import platform
import pytest
from pathlib import Path
from config.settings import settings


def pytest_configure(config):
    """Generates environment.properties for Allure Reporting."""
    allure_dir = settings.paths.ALLURE_RESULTS_DIR
    allure_dir.mkdir(parents=True, exist_ok=True)

    env_properties_path = allure_dir / "environment.properties"
    try:
        with open(env_properties_path, "w") as f:
            f.write(f"System.Under.Test=ChargeWise AI Platform\n")
            f.write(f"Frontend.URL={settings.app.BASE_URL}\n")
            f.write(f"Backend.API.URL={settings.app.API_URL}\n")
            f.write(f"ML.Service.URL={settings.app.ML_URL}\n")
            f.write(f"Database.Host={settings.db.HOST}:{settings.db.PORT}\n")
            f.write(f"Browser={settings.ui.BROWSER.capitalize()}\n")
            f.write(f"Headless.Mode={settings.ui.HEADLESS}\n")
            f.write(f"OS={platform.system()} {platform.release()}\n")
            f.write(f"Python.Version={platform.python_version()}\n")
            f.write(f"Test.Framework=PyTest + Selenium + Requests + Psycopg2\n")
    except Exception:
        pass
