from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer


@extend_schema_view(
    retrieve=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
    update=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
    partial_update=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
    destroy=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
)
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.select_related("listing", "user")

    def get_queryset(self):
        if not hasattr(self, "request") or self.request is None:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
