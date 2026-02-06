from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Payment
from .providers import ProviderFactory
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.select_related("booking").all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = ProviderFactory.build()
        result = provider.charge(float(serializer.validated_data["amount"]), serializer.validated_data["token"])
        payment = Payment.objects.create(
            booking=serializer.validated_data["booking"],
            amount=serializer.validated_data["amount"],
            approved=result.approved,
            provider_reference=result.reference,
        )
        if result.approved:
            payment.booking.mark_confirmed()
        output = self.get_serializer(payment)
        return Response(output.data, status=status.HTTP_201_CREATED)
