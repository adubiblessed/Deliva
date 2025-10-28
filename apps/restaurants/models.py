from django.db import models

from enum import Enum

from core.models import BaseModel

class DeliveryStatus(Enum):
    PENDING = 'pending'
    PICKED_UP = 'picked_up'
    EN_ROUTE = 'en_route'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class Restaurant(BaseModel):
    owner = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='restaurant_logos/', null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    #zone = models.ForeignKey('Zone', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField()
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    min_order_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name



class Delivery(BaseModel):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE)
    rider = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    pickup_location = models.JSONField()
    dropoff_location = models.JSONField()
    status = models.CharField(max_length=50, default=DeliveryStatus.PENDING.value)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Delivery for Order {self.order.id} - Status: {self.status}"
    


class DeliveryTracking(BaseModel):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tracking for Delivery {self.delivery.id} at {self.timestamp}"
    
