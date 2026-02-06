from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.select_related("listing", "user").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
