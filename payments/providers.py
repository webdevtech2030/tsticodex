from dataclasses import dataclass

from django.conf import settings


@dataclass
class PaymentResult:
    approved: bool
    reference: str


class BaseProvider:
    def charge(self, amount: float, token: str) -> PaymentResult:
        raise NotImplementedError


class MockProvider(BaseProvider):
    def charge(self, amount: float, token: str) -> PaymentResult:
        approved = token == settings.PAYMENT_SUCCESS_CODE
        reference = f"mock-{int(amount * 100)}"
        return PaymentResult(approved=approved, reference=reference)


class StripeProvider(BaseProvider):
    def charge(self, amount: float, token: str) -> PaymentResult:
        if not settings.STRIPE_SECRET_KEY:
            raise ValueError("Missing STRIPE_SECRET_KEY")
        # Placeholder for real Stripe SDK charge/create_payment_intent flow.
        return PaymentResult(approved=True, reference=f"stripe-pi-{token[-8:]}")


class ProviderFactory:
    @staticmethod
    def build() -> BaseProvider:
        if settings.PAYMENT_PROVIDER == "stripe":
            return StripeProvider()
        return MockProvider()
