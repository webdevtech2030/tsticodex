from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey("listings.Listing", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=models.F("start_date")),
                name="booking_end_date_after_start_date",
            )
        ]
        indexes = [
            models.Index(fields=["user", "status"], name="bookings_bo_user_id_344f2d_idx"),
            models.Index(
                fields=["listing", "start_date", "end_date"],
                name="bookings_bo_listing_0fd8af_idx",
            ),
        ]

    def mark_confirmed(self) -> None:
        self.set_status(self.Status.CONFIRMED)

    def set_status(self, target_status: str) -> None:
        if self.status == self.Status.CANCELLED and target_status == self.Status.CONFIRMED:
            raise ValidationError("Cancelled bookings cannot be confirmed.")
        self.status = target_status
        self.save(update_fields=["status"])
