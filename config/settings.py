"""
Configuration management module for ChargeWise QA Automation Framework.
Loads environment variables safely with robust defaults.
"""
from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of QA Framework
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class AppConfig:
    """System Under Test URLs and Endpoints"""
    BASE_URL: str = os.getenv("CHARGEWISE_BASE_URL", "http://localhost:3000").rstrip("/")
    API_URL: str = os.getenv("CHARGEWISE_API_URL", "http://localhost:8080/api/v1").rstrip("/")
    ML_URL: str = os.getenv("CHARGEWISE_ML_URL", "http://localhost:8000").rstrip("/")


@dataclass(frozen=True)
class UIConfig:
    """Selenium WebDriver and UI Execution Options"""
    BROWSER: str = os.getenv("SELENIUM_BROWSER", "chrome").lower()
    HEADLESS: bool = os.getenv("SELENIUM_HEADLESS", "true").lower() in ("true", "1", "yes")
    IMPLICIT_WAIT: int = int(os.getenv("SELENIUM_IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("SELENIUM_PAGE_LOAD_TIMEOUT", "30"))
    WINDOW_WIDTH: int = int(os.getenv("SELENIUM_WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT: int = int(os.getenv("SELENIUM_WINDOW_HEIGHT", "1080"))


@dataclass(frozen=True)
class AuthConfig:
    """Pre-configured Test User Credentials"""
    USER_USERNAME: str = os.getenv("TEST_USER_USERNAME", "user")
    USER_PASSWORD: str = os.getenv("TEST_USER_PASSWORD", "user")
    USER_PHONE: str = os.getenv("TEST_USER_PHONE", "+91 98765 43210")
    ADMIN_USERNAME: str = os.getenv("TEST_ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("TEST_ADMIN_PASSWORD", "admin123")


@dataclass(frozen=True)
class DatabaseConfig:
    """PostgreSQL Database Connection Parameters"""
    HOST: str = os.getenv("DB_HOST", "localhost")
    PORT: int = int(os.getenv("DB_PORT", "5432"))
    NAME: str = os.getenv("DB_NAME", "chargewise_db")
    USER: str = os.getenv("DB_USER", "postgres")
    PASSWORD: str = os.getenv("DB_PASSWORD", "postgrespassword")
    SSL_MODE: str = os.getenv("DB_SSL_MODE", "prefer")

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


@dataclass(frozen=True)
class RedisConfig:
    """Redis Cache and Distributed Lock Parameters"""
    HOST: str = os.getenv("REDIS_HOST", "localhost")
    PORT: int = int(os.getenv("REDIS_PORT", "6379"))


@dataclass(frozen=True)
class PathConfig:
    """File System Paths for Reports and Artifacts"""
    ROOT_DIR: Path = BASE_DIR
    REPORTS_DIR: Path = BASE_DIR / "reports"
    ALLURE_RESULTS_DIR: Path = BASE_DIR / os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
    SCREENSHOT_DIR: Path = BASE_DIR / os.getenv("SCREENSHOT_DIR", "reports/screenshots")
    DOCS_DIR: Path = BASE_DIR / "docs"


class Settings:
    """Central singleton settings accessor"""
    app = AppConfig()
    ui = UIConfig()
    auth = AuthConfig()
    db = DatabaseConfig()
    redis = RedisConfig()
    paths = PathConfig()


# Singleton instance
settings = Settings()
