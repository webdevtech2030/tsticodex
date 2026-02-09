# Property Platform API

Django REST API for a property platform with users, listings, bookings, payments, and blogs.

## Features
- JWT authentication (`/api/v1/auth/token/`, `/api/v1/auth/token/refresh/`)
- User profile endpoint (`/api/v1/users/me/`)
- CRUD APIs for listings, bookings, payments, and blog posts
- OpenAPI schema + Redoc docs
- Pluggable payment provider (mock/stripe-ready contract)

## Tech stack
- Python + Django
- Django REST Framework
- drf-spectacular
- Simple JWT

## Project structure
- `config/` - settings, root URL config, WSGI/ASGI
- `users/` - custom user model and profile endpoint
- `listings/` - property listing API
- `bookings/` - booking API
- `payments/` - payment API and provider abstraction
- `blogs/` - blog post API

## Setup
1. Create and activate a virtualenv.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start development server:
   ```bash
   python manage.py runserver
   ```

## Environment variables
- `DJANGO_SECRET_KEY` (default: `dev-only-secret`)
- `DJANGO_DEBUG` (`true`/`false`, default: `true`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated, default: `*`)

### Database
If `POSTGRES_DB` is set, PostgreSQL is used with:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST` (default: `localhost`)
- `POSTGRES_PORT` (default: `5432`)

Otherwise SQLite is used (`db.sqlite3`).

### Payments
- `PAYMENT_PROVIDER` (default: `mock`)
- `PAYMENT_SUCCESS_CODE` (default: `Success123`)
- `STRIPE_SECRET_KEY` (optional)

## API docs
- Schema: `GET /api/schema/`
- Redoc UI: `GET /api/docs/`

## Main API routes
All application routes are merged under `/api/v1/`:
- `auth/token/`
- `auth/token/refresh/`
- `users/`
- `listings/`
- `bookings/`
- `payments/`
- `blogs/`

## Quick auth flow
1. Create a user (via admin/shell/seed).
2. Obtain token pair:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/v1/auth/token/ \
     -H 'Content-Type: application/json' \
     -d '{"email":"user@example.com","password":"password"}'
   ```
3. Use `access` token:
   ```bash
   curl http://127.0.0.1:8000/api/v1/users/me/ \
     -H 'Authorization: Bearer <access-token>'
   ```
