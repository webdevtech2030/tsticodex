# API Additions (Security + Phone Auth)

## Phone-first authentication

- `POST /api/v1/users/auth/send-code/`
  - payload: `{ "phone_number": "09xxxxxxxxx", "purpose": "signup|login" }`
  - sends verification code via SMS provider abstraction.
- `POST /api/v1/users/auth/verify-code/`
  - payload: `{ "phone_number": "09xxxxxxxxx", "purpose": "signup|login", "code": "123456", "username": "optional" }`
  - verifies one-time code, marks phone verified, and returns JWT tokens + user payload.

## JWT security defaults

- JWT required for `/api/v1/*` endpoints by default.
- Refresh token rotation + blacklisting enabled.
- Access token lifetime shortened to 15 minutes.

## Payment security and domain constraints

- Only booking owner can pay.
- Only `pending` bookings are payable.
- Approved payment confirms booking status.

## Mobile compatibility notes (React Native / Flutter)

- Auth and resources are JSON-first DRF endpoints.
- Versioned prefix (`/api/v1/`) maintained for backward-compatible evolution.
- CORS settings are env-driven (`CORS_ALLOWED_ORIGINS`) for mobile/web client control.

## Jalali date in UI

- HTML templates use `jalali` template filter for rendering Jalali dates in server-rendered pages.
- API remains ISO-8601 for mobile client interoperability.

## Containerization

- Production-ready multi-stage `Dockerfile` with non-root runtime user, slim image, and migration-aware entrypoint.
- `docker-compose.yml` includes app + PostGIS database, healthchecks, persistent volumes, and env-driven secrets.
- Copy `.env.example` to `.env` and update credentials before running in real environments.

## UI/UX and frontend conventions

- Root layout lives in `templates/base.html` and each app keeps its own local templates under `app/templates/app/`.
- Bootstrap 5.3.8 (RTL build) is used for modern, responsive, mobile-first UI.
- Any visible date in server-rendered templates should pass through `|jalali`.

## API compatibility for React Native / Flutter

- API remains JSON-first with JWT bearer auth.
- Pagination is enabled for collection endpoints (`PAGE_SIZE=20`).
- Throttling defaults are enabled to protect public/user APIs.
- URLs remain versioned with `/api/v1/`.
