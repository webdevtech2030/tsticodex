from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        model = Payment
        fields = ["id", "booking", "amount", "approved", "provider_reference", "token", "created_at"]
        read_only_fields = ["approved", "provider_reference", "created_at"]
