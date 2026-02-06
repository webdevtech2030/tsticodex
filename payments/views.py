from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from .services import PaymentInput, PaymentService


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.select_related("booking").filter(booking__user=self.request.user)

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
