# Business Tracker Backend Architecture

## Overview
This backend application is structured according to enterprise-grade Django best practices designed for maintainability, clean separation of concerns, and team scalability.

## Directory Layout
```
business-backend/
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── .env
├── .env.example
├── .gitignore
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       ├── production.py
│       └── test.py
├── apps/
│   ├── __init__.py
│   ├── core/                   # Shared utilities, abstract models, custom pagination & handlers
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── exceptions.py
│   │   └── pagination.py
│   └── users/                  # Custom user domain app
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── selectors.py         # Read queries
│       ├── services.py          # Business logic / write actions
│       ├── serializers.py      # Thin DRF data validation & presentation
│       ├── views.py            # Thin DRF API orchestrators
│       ├── urls.py
│       ├── tasks.py             # Celery async tasks
│       ├── migrations/
│       └── tests/
├── static/
├── media/
├── templates/
└── docs/
```

## Architectural Patterns

### 1. Selectors & Services Pattern
- **`selectors.py`**: Pure functions responsible for fetching and querying database objects. No state mutations or side-effects happen in selectors.
- **`services.py`**: Pure functions handling business logic execution, atomic transactions (`@transaction.atomic`), validation checks, and state modifications.
- **Views & Serializers**: DRF Views and Serializers act as thin orchestration layers parsing request data, passing parameters to services/selectors, and rendering responses.

### 2. Custom User Model (`AbstractUser`)
A custom `User` model (`apps.users.models.User`) is defined from day one. Authentication uses `email` as the primary identifier.

### 3. Environment-Based Settings Split & Database Wiring
Settings are modularly separated into:
- `config/settings/base.py`: Core configuration reading environment variables via `django-environ`.
- `config/settings/local.py`: Local developer extensions.
- `config/settings/production.py`: Hardened security settings (HSTS, SSL headers, Secure Cookies).
- `config/settings/test.py`: Fast in-memory SQLite database setup for test suites.

### 4. PostgreSQL & Docker Setup
The database is configured via `DATABASE_URL` in `.env`:
```env
DATABASE_URL=postgres://business_user:strongpassword@localhost:5432/business_db
```
Included [`docker-compose.yml`](file:///d:/Projects/BussinessTracker/business-backend/docker-compose.yml) spins up isolated PostgreSQL 16 & Redis containers:
```bash
docker compose up -d
python manage.py migrate
```

