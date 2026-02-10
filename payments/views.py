from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from .services import PaymentInput, PaymentService


@extend_schema_view(
    retrieve=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
    update=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
    partial_update=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
    destroy=extend_schema(parameters=[OpenApiParameter(name="id", type=int, location=OpenApiParameter.PATH)]),
)
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.select_related("booking")

    def get_queryset(self):
        if not hasattr(self, "request") or self.request is None:
            return self.queryset
        return self.queryset.filter(booking__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = PaymentService.create_payment(
            PaymentInput(
                booking=serializer.validated_data["booking"],
                amount=serializer.validated_data["amount"],
                token=serializer.validated_data["token"],
            )
        )
        output = self.get_serializer(payment)
        return Response(output.data, status=status.HTTP_201_CREATED)
