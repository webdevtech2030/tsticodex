from dataclasses import dataclass

from django.db import transaction

from bookings.models import Booking
from payments.models import Payment
from payments.providers import ProviderFactory


@dataclass
class PaymentInput:
    booking: Booking
    amount: float
    token: str


class PaymentService:
    @staticmethod
    @transaction.atomic
    def create_payment(payload: PaymentInput) -> Payment:
        provider = ProviderFactory.build()
        result = provider.charge(payload.amount, payload.token)
        payment = Payment.objects.create(
            booking=payload.booking,
            amount=payload.amount,
            approved=result.approved,
            provider_reference=result.reference,
        )
        if payment.approved:
            payment.booking.mark_confirmed()
        return payment
