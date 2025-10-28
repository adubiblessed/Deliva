from django.db import models
from enum import Enum
import uuid

# Create your models here.
from core.models import BaseModel

class PaymentMethod(Enum):
    CREDIT_CARD = 'Credit Card'
    CASH_ON_DELIVERY = 'Cash on Delivery'
    PAYPAL = 'PayPal'
    STRIPE = 'Stripe'

class PaymentStatus(Enum):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    REFUNDED = 'Refunded'


class Payment(BaseModel):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway = models.CharField(max_length=50, choices=[(tag.value, tag.value) for tag in PaymentMethod])
    status =  models.CharField(max_length=50, choices=[(tag.value, tag.value) for tag in PaymentStatus], default=PaymentStatus.PENDING.value)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference =   models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.reference} - {self.status}"