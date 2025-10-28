from decimal import Decimal

from django.db import models

from accounts.models import User
from core.models import BaseModel 

from enum import Enum


class TransactionType(Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'


class Address(BaseModel):
    customer  = models.ManyToManyField(User, related_name='addresses')
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
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, 
                                    related_name='customer_profiles', 
                                    blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))


    def __str__(self):
        return f"CustomerProfile of {self.user.email}"
    
    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"


class Wallet(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))

    def __str__(self):
        return f"Wallet of {self.customer.email} - Balance: {self.balance}"
    
    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"


class Transaction(BaseModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[(tag.value, tag.name) for tag in TransactionType])
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.reference_generator()

        if self.transaction_type == TransactionType.CREDIT.value:
            self.wallet.balance += self.amount
        elif self.transaction_type == TransactionType.DEBIT.value:
            self.wallet.balance -= self.amount
        self.wallet.save()
        super().save(*args, **kwargs)

    def reference_generator(self):
        import uuid
        return str(uuid.uuid4()).replace('-', '').upper()[:12]


    def __str__(self):
        return f"Transaction of {self.amount} - Type: {self.transaction_type}"
    
    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"