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
        return PaymentResult(approved=approved, reference="mock-txn")


class StripeProvider(BaseProvider):
    def charge(self, amount: float, token: str) -> PaymentResult:
        if not settings.STRIPE_SECRET_KEY:
            raise ValueError("Missing STRIPE_SECRET_KEY")
        return PaymentResult(approved=True, reference="stripe-placeholder")


class ProviderFactory:
    @staticmethod
    def build() -> BaseProvider:
        if settings.PAYMENT_PROVIDER == "stripe":
            return StripeProvider()
        return MockProvider()
