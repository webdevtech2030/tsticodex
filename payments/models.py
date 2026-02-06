from django.db import models


class Payment(models.Model):
    booking = models.ForeignKey("bookings.Booking", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved = models.BooleanField(default=False)
    provider_reference = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
