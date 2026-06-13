# NIFTY100 AI Financial Intelligence Platform

A company-level financial analytics platform built for analyzing NIFTY 100 companies with AI-powered insights, ML scoring, and a full REST API.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0.5 |
| Database | PostgreSQL |
| REST API | Django REST Framework + drf-spectacular |
| ML Engine | scikit-learn, statsmodels, pandas |
| Charts | Plotly |
| Frontend | Bootstrap 5 + Glassmorphism UI |
| Authentication | HMAC-SHA256 + API Keys |
| Code Quality | black, isort, flake8, bandit, safety |
| Testing | pytest, pytest-django, pytest-cov |

---

## 📦 Project Structure

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/nifty100_financial_platform.git
cd nifty100_financial_platform
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in `django_app/backend/` with:

```env
SECRET_KEY=your-secret-key-here
DB_NAME=nifty100warehouse
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run database migrations

```bash
cd django_app/backend
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Create a test API partner

```bash
python manage.py create_test_partner
```

### 8. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the platform.

---

## 📱 Platform Modules

| # | Module | URL | Description |
|---|---|---|---|
| 1 | Home | `/` | Platform overview with KPI cards |
| 2 | Revenue Forecast | `/revenue-forecast/` | AI-powered revenue forecasting |
| 3 | Sector Analytics | `/sector-analytics/` | Sector comparison and rankings |
| 4 | Company Scorecard | `/company-scorecard/` | ML-scored company leaderboard |
| 5 | Company Deep Dive | `/company-deep-dive/` | Full financial analysis per company |
| 6 | Portfolio Builder | `/portfolio-builder/` | Risk-based portfolio construction |
| 7 | Executive Dashboard | `/executive-dashboard/` | Premium KPI dashboard |
| 8 | AI Investment Advisor | `/ai-investment-advisor/` | Buy/Hold/Sell signals |
| 9 | Risk Intelligence | `/risk-intelligence/` | Risk monitoring dashboard |
| 10 | News Sentiment | `/news-sentiment/` | Sentiment analysis |
| 11 | Financial Copilot | `/financial-copilot/` | AI financial assistant |
| 12 | Portfolio Optimizer | `/portfolio-optimizer/` | Portfolio optimization engine |
| 13 | Price Prediction | `/price-prediction/` | ML price forecasting |
| 14 | Financial Analyst | `/financial-analyst/` | AI-powered financial analysis |

---

## 🔐 API Management

### Base URL

`http://127.0.0.1:8000/api/v1/`

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/register/` | Register new API client |
| GET | `/api/v1/status/` | Get API status and usage |
| GET | `/api/v1/partner/` | Channel Partner data access |
| POST | `/api/v1/webhooks/create/` | Register webhook |
| GET | `/api/v1/webhooks/` | List all webhooks |
| POST | `/api/v1/keys/rotate/` | Rotate API key |
| GET | `/api/v1/logs/` | View request logs |

### Authentication

All API requests require the `X-API-Key` header:

```bash
curl -H "X-API-Key: your_api_key_here" http://127.0.0.1:8000/api/v1/status/
```

### Rate Limits by Plan

| Plan | Per Minute | Per Hour | Per Day |
|---|---|---|---|
| Basic | 10 | 100 | 500 |
| Premium | 60 | 1,000 | 10,000 |
| Enterprise | 300 | 10,000 | 1,00,000 |

### HMAC Authentication

Channel partner requests must include HMAC-SHA256 signature:

```python
import hmac
import hashlib

signature = "sha256=" + hmac.new(
    secret.encode(),
    request_body,
    hashlib.sha256
).hexdigest()

headers = {
    "X-API-Key": api_key,
    "X-Signature-256": signature
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test api_management

# Run with pytest and coverage
pytest api_management/tests.py -v

# View coverage report
pytest api_management/tests.py --cov=api_management --cov-report=term-missing
```

**Test Results:** 20/20 tests passing | 82% coverage

---

## 🔒 Security

```bash
# Run bandit security scan
bandit -r . -x ./venv

# Run safety vulnerability check
pip freeze > requirements.txt
safety check --file requirements.txt
```

**Security Status:** 0 high/medium issues | 0 vulnerabilities

---

## 🎨 Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8 api_management --exclude=migrations --max-line-length=120
```

---

## 🗄️ ETL Pipeline

```bash
# Step 1 - Extract data
python etl/01_extract_data.py

# Step 2 - Clean and transform
python etl/02_clean_transform.py

# Step 3 - Load to warehouse
python etl/03_load_to_warehouse.py
```

---

## 📊 API Documentation

Interactive Swagger UI available at:

`http://127.0.0.1:8000/api/docs/`

OpenAPI schema available at:

`http://127.0.0.1:8000/api/schema/`

---

## 🛠️ Admin Panel

`http://127.0.0.1:8000/admin/`

---

## 📋 Requirements

- Python 3.12+
- PostgreSQL 13+
- pip packages listed in `requirements.txt`

---

## 📁 Key Commands Reference

| Command | Purpose |
|---|---|
| `python manage.py runserver` | Start development server |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py create_test_partner` | Create test API partner |
| `python manage.py test api_management` | Run tests |
| `black .` | Format code |
| `isort .` | Sort imports |
| `bandit -r . -x ./venv` | Security scan |
| `pytest api_management/tests.py -v` | Run pytest |

---

## 🏢 Project Info

**Platform:** NIFTY100 AI Financial Intelligence Platform
**Version:** 1.0.0
**Stack:** Django + PostgreSQL + ML + REST API
**Status:** Production Ready

---

*NIFTY100 Financial Intelligence Platform — Bluestock Fintech*
