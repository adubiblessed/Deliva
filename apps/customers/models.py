from decimal import Decimal

from django.db import models

from accounts.models import User
from core.models import BaseModel 


class Address(BaseModel):
    customer  = models.ManyToManyRelatedField(User, related_name='addresses', on_delete=models.CASCADE)
    label = models.CharField(max_length=100, null=True, blank=True) # e.g., Home, Work
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Nigeria')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ['city', 'state']

class CustomerProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, related_name='customer_profiles')
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))