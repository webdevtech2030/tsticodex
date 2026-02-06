from rest_framework import serializers

from bookings.models import Booking

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        model = Payment
        fields = ["id", "booking", "amount", "approved", "provider_reference", "token", "created_at"]
        read_only_fields = ["approved", "provider_reference", "created_at"]

    def validate_booking(self, booking: Booking) -> Booking:
        request = self.context["request"]
        if booking.user_id != request.user.id:
            raise serializers.ValidationError("You can only pay for your own booking.")
        if booking.status != Booking.Status.PENDING:
            raise serializers.ValidationError("Only pending bookings can be paid.")
        return booking
