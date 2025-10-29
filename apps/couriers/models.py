from decimal import Decimal

from django.db import models


from apps.accounts.models import User
from core.models import BaseModel


class RiderProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    vehicle_type = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.00'))
    current_location = models.JSONField(null=True, blank=True)  # e.g., {"latitude": xx.xxxxxx, "longitude": yy.yyyyyy}

    def __str__(self):
        return f"RiderProfile of {self.user.email}"
    

class Vehicle(BaseModel):
    rider = models.ForeignKey(RiderProfile, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.vehicle_type} - {self.license_plate} of {self.rider.user.email}"

class DeliveryAssignment(BaseModel):
    delivery = models.OneToOneField('restaurants.Delivery', on_delete=models.CASCADE)
    rider = models.ForeignKey(RiderProfile, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"DeliveryAssignment of Delivery {self.delivery.id} to Rider {self.rider.user.email}"
    

    