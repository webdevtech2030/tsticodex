from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone_number", "username", "email", "is_host", "is_phone_verified"]


class SendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    purpose = serializers.ChoiceField(choices=["login", "signup"])


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=["login", "signup"])
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
