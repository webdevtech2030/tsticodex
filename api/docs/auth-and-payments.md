# API Additions (Phase 1 Hardening)

## Authentication

- `POST /api/v1/auth/token/` returns `access` and `refresh` JWT tokens.
- `POST /api/v1/auth/token/refresh/` rotates the access token.
- All `/api/v1/*` endpoints now require bearer authentication by default.

## Payments Provider Toggle

`payments.ProviderFactory` chooses payment backend by `PAYMENT_PROVIDER`:

- `mock` (default): accepts only token value equal to `PAYMENT_SUCCESS_CODE` (`Success123` default).
- `stripe`: uses `StripeProvider` placeholder and requires `STRIPE_SECRET_KEY`.

## Booking Confirmation

Successful payment (`approved=true`) automatically marks `booking.status="confirmed"`.
