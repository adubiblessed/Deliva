from django.db import models

from core.models import BaseModel


class Restaurant(BaseModel):
    owner = models.OneToOneField('User', on_delete=models.CASCADE)
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
    open_time = models.TimeField()
    close_time = models.TimeField()
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    min_order_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name