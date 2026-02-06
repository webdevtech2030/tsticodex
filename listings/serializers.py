from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["id", "owner", "title", "nightly_price", "created_at"]
        read_only_fields = ["owner", "created_at"]
