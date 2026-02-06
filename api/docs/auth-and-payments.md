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
