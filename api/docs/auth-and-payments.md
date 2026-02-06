# API Additions (Phase 1 Hardening)

## Authentication (SimpleJWT)

- `POST /api/v1/auth/token/` returns `access` and `refresh` JWT tokens.
- `POST /api/v1/auth/token/refresh/` rotates and blacklists refresh tokens.
- All `/api/v1/*` endpoints require bearer authentication by default.

## Modernized security defaults

- Refresh token rotation is enabled (`ROTATE_REFRESH_TOKENS=true`).
- Old refresh tokens are blacklisted after rotation (`BLACKLIST_AFTER_ROTATION=true`).
- `UPDATE_LAST_LOGIN=true` is enabled for better account activity tracking.

## Payments Provider Toggle

`payments.ProviderFactory` chooses payment backend by `PAYMENT_PROVIDER`:

- `mock` (default): accepts only token value equal to `PAYMENT_SUCCESS_CODE` (`Success123` default).
- `stripe`: uses `StripeProvider` integration placeholder and requires `STRIPE_SECRET_KEY`.

## Booking Confirmation

Successful payment (`approved=true`) automatically marks `booking.status="confirmed"`.
Only `pending` bookings owned by the current user may be paid.
