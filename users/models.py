from datetime import timedelta
from secrets import randbelow

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_host = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.phone_number


class VerificationCode(models.Model):
    class Purpose(models.TextChoices):
        LOGIN = "login", "Login"
        SIGNUP = "signup", "Signup"

    phone_number = models.CharField(max_length=20, db_index=True)
    code_hash = models.CharField(max_length=255)
    purpose = models.CharField(max_length=20, choices=Purpose.choices)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    consumed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["phone_number", "purpose", "expires_at"],
                name="users_verif_phone_n_703a5e_idx",
            )
        ]

    @classmethod
    def create_code(cls, phone_number: str, purpose: str) -> tuple["VerificationCode", str]:
        raw_code = f"{randbelow(10**6):06d}"
        instance = cls.objects.create(
            phone_number=phone_number,
            purpose=purpose,
            code_hash=make_password(raw_code),
            expires_at=timezone.now() + timedelta(minutes=3),
        )
        return instance, raw_code

    def verify(self, code: str) -> bool:
        if self.consumed_at is not None or self.expires_at < timezone.now() or self.attempts >= 5:
            return False
        self.attempts += 1
        self.save(update_fields=["attempts"])
        if not check_password(code, self.code_hash):
            return False
        self.consumed_at = timezone.now()
        self.save(update_fields=["consumed_at"])
        return True
