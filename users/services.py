from dataclasses import dataclass

from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, VerificationCode


class SmsProvider:
    def send_code(self, phone_number: str, code: str) -> None:
        # Replace with real SMS provider integration in production.
        return None


@dataclass
class AuthTokens:
    refresh: str
    access: str


class PhoneAuthService:
    sms_provider = SmsProvider()

    @classmethod
    def send_code(cls, phone_number: str, purpose: str) -> None:
        _instance, raw_code = VerificationCode.create_code(phone_number=phone_number, purpose=purpose)
        cls.sms_provider.send_code(phone_number=phone_number, code=raw_code)

    @classmethod
    @transaction.atomic
    def verify_code(cls, phone_number: str, purpose: str, code: str, username: str = "") -> tuple[User, AuthTokens]:
        pending = (
            VerificationCode.objects.filter(
                phone_number=phone_number,
                purpose=purpose,
                consumed_at__isnull=True,
            )
            .order_by("-created_at")
            .first()
        )
        if not pending or not pending.verify(code):
            raise ValueError("Invalid or expired verification code")

        user, _ = User.objects.get_or_create(phone_number=phone_number)
        if username and not user.username:
            user.username = username
        user.is_phone_verified = True
        user.save(update_fields=["username", "is_phone_verified"])

        refresh = RefreshToken.for_user(user)
        return user, AuthTokens(refresh=str(refresh), access=str(refresh.access_token))
