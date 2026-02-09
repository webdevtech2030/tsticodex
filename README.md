# Property Platform (Django + DRF)

A modular monolith property booking platform built with Django/DRF, designed for:

- **Web UI** (Django templates + Bootstrap RTL)
- **Mobile clients** (React Native / Flutter) via versioned JSON APIs (`/api/v1/`)

## Apps

- `users` → phone-first auth + OTP verification
- `listings` → property catalog
- `bookings` → booking lifecycle (`pending`, `confirmed`, `cancelled`)
- `payments` → provider-based charging + booking confirmation
- `blogs` → content / engagement

---

## Tech Stack

- Django 6.x
- Django REST Framework
- SimpleJWT
- drf-spectacular (OpenAPI schema/docs)
- PostgreSQL / PostGIS (via Docker Compose)
- Bootstrap 5.3 RTL (server-rendered templates)

---

## Quick Start for Developers

## 1) Clone and configure env

```bash
git clone <your-repo-url>
cd tsticodex
cp .env.example .env
```

Update values in `.env` (especially secrets and DB credentials).

---

## 2) Run with Docker (recommended)

### Build and start

```bash
docker compose up --build
```

App will be available at:

- `http://localhost:8000/`
- API docs: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

### Stop services

```bash
docker compose down
```

### Stop and remove volumes (destructive)

```bash
docker compose down -v
```

---

## 3) Run locally without Docker

> Requires Python 3.12+ and PostgreSQL (or SQLite fallback if `POSTGRES_DB` is unset).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

---

## Environment Variables

See `.env.example` for defaults.

Key variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `PAYMENT_PROVIDER` (`mock` / `stripe`)
- `PAYMENT_SUCCESS_CODE` (default dev bypass: `Success123`)
- `STRIPE_SECRET_KEY`
- `CORS_ALLOWED_ORIGINS`

---

## Auth Flow (Phone + OTP)

1. Request code
   - `POST /api/v1/users/auth/send-code/`
2. Verify code and receive tokens
   - `POST /api/v1/users/auth/verify-code/`
3. Use JWT access token for protected endpoints
   - `Authorization: Bearer <access_token>`

---

## Developer Checks

```bash
python -m py_compile $(rg --files -g '*.py')
python manage.py check
```

---

## Project Structure

- `templates/base.html` → global layout
- `*/templates/<app_name>/...` → app-local templates
- `api/docs/` → internal docs
- `docker-compose.yml`, `Dockerfile`, `docker/entrypoint.sh` → container runtime

---

## Notes

- UI dates should be rendered in **Jalali** in templates.
- API remains **JSON-first + versioned** for mobile compatibility.
- For production, set `DJANGO_DEBUG=false` and secure all secrets.
