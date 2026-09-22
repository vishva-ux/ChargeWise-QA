# ⚡ ChargeWise AI - QA Automation & Quality Engineering Framework

[![CI/CD QA Pipeline](https://github.com/vishva-ux/ChargeWise-QA/actions/workflows/qa-tests.yml/badge.svg)](https://github.com/vishva-ux/ChargeWise-QA/actions/workflows/qa-tests.yml)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Testing Framework](https://img.shields.io/badge/Framework-PyTest%208.x-orange.svg)](https://pytest.org/)
[![UI Automation](https://img.shields.io/badge/UI-Selenium%20WebDriver-green.svg)](https://www.selenium.dev/)
[![Reports](https://img.shields.io/badge/Reporting-Allure%202.x-yellowgreen.svg)](https://allurereport.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> **An independent, production-grade Quality Engineering & SDET Automation Repository** engineered specifically to test the **ChargeWise AI** Electric Vehicle (EV) Smart Charging and Distributed Locking ecosystem.

---

## 📌 1. Project Overview & Architecture

This repository is completely decoupled from the production application code and acts as an autonomous QA testing engine. It tests the **System Under Test (SUT)** across all technical layers: Frontend UI, REST API Microservices, Machine Learning Inference Engines, PostgreSQL/PostGIS Spatial Database, and Redisson Distributed Locking.

### System Under Test (SUT) vs QA Automation Architecture

```mermaid
flowchart TD
    subgraph SUT["System Under Test (ChargeWise AI Platform)"]
        FE["Frontend (Next.js/React - :3000)"]
        BE["Backend (Spring Boot - :8080)"]
        ML["ML Service (FastAPI - :8000)"]
        DB[("PostgreSQL + PostGIS (:5432)")]
        RD[("Redis 7.2 Cache (:6379)")]

        FE -->|REST API| BE
        FE -->|Inference API| ML
        BE -->|Geospatial ST_DWithin| DB
        BE -->|Redisson Distributed Lock| RD
    end

    subgraph QAFramework["QA Automation Framework (chargewise-qa-automation)"]
        CONF["config/settings.py (.env)"]
        
        UI_POM["UI Automation (Selenium + POM)"]
        API_TESTS["API Automation (Requests + PyTest)"]
        DB_TESTS["Database Testing (Psycopg2 + SQL)"]
        E2E_TESTS["E2E User Journeys"]
        PERF_TESTS["Performance (JMeter + Benchmarks)"]

        CONF --> UI_POM
        CONF --> API_TESTS
        CONF --> DB_TESTS
        CONF --> E2E_TESTS
        CONF --> PERF_TESTS
    end

    subgraph ExecutionReports["Reporting & CI/CD"]
        ALLURE["Allure Interactive Reports"]
        GHA["GitHub Actions CI/CD Matrix"]
        DEFECTS["Defect Reports & Bug Tracking"]
    end

    UI_POM -.->|Validates DOM & Flows| FE
    API_TESTS -.->|Validates Contracts & Codes| BE
    API_TESTS -.->|Validates Predictions| ML
    DB_TESTS -.->|Validates Constraints & Rows| DB
    E2E_TESTS -.->|Cross-Tier Validation| SUT

    QAFramework --> ALLURE
    QAFramework --> GHA
    QAFramework --> DEFECTS
```

---

## 🛠️ 2. Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language & Runtime** | Python 3.10+ | Core scripting and test architecture |
| **Test Runner & Harness** | PyTest 8.x | Test lifecycle, fixtures, parameterization, and markers |
| **UI Automation** | Selenium WebDriver 4.x | Page Object Model (POM) browser automation |
| **API Automation** | Requests 2.x + Pydantic | REST HTTP contract and schema validation |
| **Database Testing** | Psycopg2 + PostgreSQL | Direct SQL constraint, trigger, and state assertion |
| **Reporting Engine** | Allure Framework 2.x | Rich HTML test reports with screenshots and request logs |
| **Performance Testing** | Apache JMeter 5.6 + Concurrency Runner | Throughput, latency percentiles (p95), and lock contention |
| **Continuous Integration** | GitHub Actions | Automated multi-tier matrix testing on push/PR |

---

## 📁 3. Repository Structure

```text
chargewise-qa-automation/
├── .github/
│   └── workflows/
│       └── qa-tests.yml            # Multi-tier CI/CD workflow matrix
├── api/
│   ├── clients/                    # Reusable HTTP API client wrappers
│   │   ├── base_client.py          # Session management & Allure logging
│   │   ├── auth_client.py          # User authentication endpoints
│   │   ├── station_client.py       # Geospatial station discovery
│   │   ├── booking_client.py       # Atomic slot booking & lock endpoints
│   │   └── ml_prediction_client.py # FastAPI wait-time & stop recommendation
│   ├── tests/                      # API automated test suites
│   │   ├── test_auth_api.py
│   │   ├── test_station_api.py
│   │   ├── test_booking_api.py
│   │   └── test_ml_service_api.py
│   └── conftest.py                 # API test fixtures
├── config/
│   ├── __init__.py
│   └── settings.py                 # Environment settings & .env parser
├── database/
│   ├── db_client.py                # PostgreSQL connection pool & query executor
│   ├── conftest.py                 # DB connection fixtures
│   └── tests/                      # Database test suites
│       ├── test_booking_database.py
│       └── test_station_database.py
├── docs/
│   ├── chargewise-system-analysis.md # Comprehensive SUT technical breakdown
│   ├── test-plan.md                # Master Quality Engineering Test Plan
│   ├── test-cases.md               # 50+ Detailed Test Case specifications
│   ├── test-cases.csv              # Spreadsheet compatible test case export
│   ├── performance-test-report.md  # Concurrency benchmark & latency results
│   └── bug-reports.md              # Discovered defects & RCA documentation
├── e2e/
│   ├── conftest.py
│   └── tests/                      # Cross-service end-to-end user journeys
│       ├── test_e2e_booking_lifecycle.py
│       ├── test_e2e_route_and_reserve.py
│       └── test_e2e_booking_cancellation.py
├── performance/
│   ├── chargewise_load_test.jmx    # Apache JMeter load test plan
│   └── run_performance_benchmark.py# Standalone Python concurrency benchmark
├── reports/
│   ├── allure-results/             # Allure raw JSON/XML execution artifacts
│   └── screenshots/                # Automatic failure screenshots
├── ui/
│   ├── pages/                      # Page Object Model (POM) classes
│   │   ├── base_page.py            # Explicit waits, locator wrappers
│   │   ├── login_page.py           # Modal & /auth page interactions
│   │   ├── home_page.py            # Header, profile, AI search module
│   │   ├── station_page.py         # BottomSheet listing & card filters
│   │   ├── booking_page.py         # Reservation drawer & QR pass view
│   │   └── route_page.py           # Route planner & battery optimizer
│   ├── tests/                      # Selenium UI automated test suites
│   │   ├── test_login.py
│   │   ├── test_stations.py
│   │   ├── test_booking.py
│   │   └── test_route_planner.py
│   └── conftest.py                 # WebDriver fixture & failure hooks
├── .env.example                    # Environment variable template
├── .gitignore
├── conftest.py                     # Root fixture & Allure environment setup
├── pytest.ini                      # PyTest CLI options and markers
├── requirements.txt                # Python dependencies
└── README.md                       # Master Documentation
```

---

## 🚀 4. Quick Start & Setup

### Prerequisites
- Python 3.10+ installed
- Google Chrome browser installed
- Git installed
- Java Runtime (Optional, for running Apache JMeter)
- Allure CLI (Optional, for generating HTML report: `brew install allure` or `npm install -g allure-commandline`)

### 1. Clone & Set Up Environment

```bash
# Clone the QA repository
git clone https://github.com/vishva-ux/ChargeWise-QA.git
cd ChargeWise-QA

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all test dependencies
pip install -r requirements.txt
```

### 2. Configure Test Targets

Copy `.env.example` to `.env` and adjust the URLs according to your local or deployed environment:

```bash
cp .env.example .env
```

Key environment variables:
```ini
CHARGEWISE_BASE_URL=http://localhost:3000
CHARGEWISE_API_URL=http://localhost:8080/api/v1
CHARGEWISE_ML_URL=http://localhost:8000
SELENIUM_HEADLESS=true
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chargewise_db
DB_USER=postgres
DB_PASSWORD=postgrespassword
```

---

## 🧪 5. Running Automated Tests

### Run All Tests
```bash
pytest
```

### Run by Specific Test Layer
```bash
# 1. Run REST API Tests
pytest api/tests -v -m "api"

# 2. Run UI Automation Tests (Headless Chrome)
pytest ui/tests -v -m "ui"

# 3. Run Database Integrity Tests
pytest database/tests -v -m "db"

# 4. Run End-to-End User Journeys
pytest e2e/tests -v -m "e2e"
```

### Run Smoke or Critical Suites
```bash
# Run Smoke Sanity Tests
pytest -v -m "smoke"

# Run Full Regression Suite
pytest -v -m "regression"
```

---

## 📊 6. Allure Test Reporting

Execution results are automatically captured in `reports/allure-results`.

### View Live Report
```bash
allure serve reports/allure-results
```

### Generate Static HTML Report
```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

---

## ⚡ 7. Performance Testing

### Option A: Standalone Python Benchmark (No JMeter needed)
```bash
python performance/run_performance_benchmark.py
```
*Outputs a formatted table showing Throughput (RPS), Average Latency, and p95 Latencies across 10, 50, and 100 concurrent users.*

### Option B: Apache JMeter GUI / CLI
```bash
# Run JMeter in Non-GUI mode
jmeter -n -t performance/chargewise_load_test.jmx -l performance/results.jtl -e -o performance/html_report
```

---

## 🎓 8. College Viva & SDET Interview Defense Notes

### Q1: Why is QA placed in a completely separate repository?
> **Answer:** In professional SDET workflows, decoupling QA prevents circular dependency hell, allows independent CI/CD test schedules, enables testing across multiple environments (Dev, Staging, Production) without touching application build pipelines, and enforces strict black-box/gray-box testing principles.

### Q2: How does the framework handle flakiness in UI Automation?
> **Answer:** We eliminate arbitrary `time.sleep()` calls and use Selenium's `WebDriverWait` with Expected Conditions (`EC.visibility_of_element_located`, `EC.element_to_be_clickable`). The BasePage also catches `StaleElementReferenceException` with automatic retries, and failed tests automatically capture DOM screenshots attached to Allure.

### Q3: How do you verify distributed locking without double-booking?
> **Answer:** In `api/tests/test_booking_api.py` and `performance/chargewise_load_test.jmx`, we dispatch concurrent threads against `/api/v1/bookings/reserve`. We assert that the Redisson lock enforces atomic isolation so that overlapping requests are serialized or safely rejected with informative messages rather than corrupting database inventory.

### Q4: How do you test PostGIS geospatial queries in PostgreSQL?
> **Answer:** In `database/tests/test_station_database.py`, we query PostgreSQL metadata directly to verify that the `location` column is defined as `ST_Point` with SRID 4326 (`WGS 84`) and that spatial indexes (`GIST`) exist to accelerate `ST_DWithin` corridor calculations.

---

## 📄 License & Attribution

Distributed under the **MIT License**. Created for the **ChargeWise AI** Quality Engineering Portfolio.
