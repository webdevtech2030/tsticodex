from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "user", "listing", "start_date", "end_date", "status"]
        read_only_fields = ["user", "status"]
