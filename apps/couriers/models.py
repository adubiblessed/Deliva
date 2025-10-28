from decimal import Decimal

from django.db import models


from accounts.models import User
from core.models import BaseModel


class RiderProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    vehicle_type = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.00))
    current_location = models.JSONField(null=True, blank=True)  # e.g., {"latitude": xx.xxxxxx, "longitude": yy.yyyyyy}

    def __str__(self):
        return f"RiderProfile of {self.user.email}"