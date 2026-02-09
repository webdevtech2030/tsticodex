from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SendCodeSerializer, UserSerializer, VerifyCodeSerializer
from .services import PhoneAuthService


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class SendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PhoneAuthService.send_code(
            phone_number=serializer.validated_data["phone_number"],
            purpose=serializer.validated_data["purpose"],
        )
        return Response({"detail": "Verification code sent."}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, tokens = PhoneAuthService.verify_code(
                phone_number=serializer.validated_data["phone_number"],
                purpose=serializer.validated_data["purpose"],
                code=serializer.validated_data["code"],
                username=serializer.validated_data.get("username", ""),
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        payload = UserSerializer(user).data
        payload["tokens"] = {"refresh": tokens.refresh, "access": tokens.access}
        return Response(payload, status=status.HTTP_200_OK)


def login_page(request):
    return render(request, "users/login.html", {"now": timezone.now()})
