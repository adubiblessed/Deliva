import uuid
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from decimal import Decimal

from core.models import BaseModel


class OrderStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    PREPARING = 'Preparing', 'Preparing'
    OUT_FOR_DELIVERY = 'Out for Delivery', 'Out for Delivery'
    DELIVERED = 'Delivered', 'Delivered'
    CANCELLED = 'Cancelled', 'Cancelled'

class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    COMPLETED = 'Completed', 'Completed'
    FAILED = 'Failed', 'Failed'

class PaymentMethod(models.TextChoices):
    CREDIT_CARD = 'Credit Card', 'Credit Card'
    CASH_ON_DELIVERY = 'Cash on Delivery', 'Cash on Delivery'


class Cart(BaseModel):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='carts')
    restaurant = models.ForeignKey('restaurants.Restaurant', 
                                   on_delete=models.CASCADE, 
                                   related_name='carts')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_total(self):
        """
        Calculates the total and saves it to the database.
        """
        # This does the math in the DB, not in python memory
        aggregate = self.items.aggregate(total_price=models.Sum('subtotal'))
        self.total = aggregate['total_price'] or Decimal('0.00')
        self.save(update_fields=['total', 'updated_at'])    
    def __str__(self):
        return f"Cart of {self.customer} at {self.restaurant}"
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        self.subtotal = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in {self.cart}"
    
    class Meta:
        unique_together = ('cart', 'menu_item')  

@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart_total_on_change(sender, instance, **kwargs):
    """
    Automatically updates the Cart total whenever a CartItem is 
    created, updated, or deleted.
    """
    if instance.cart:
        instance.cart.update_total()

  

class Order(BaseModel):
    customer = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, related_name='orders', 
                                 null=True, blank=True)
    restaurant = models.ForeignKey('restaurants.Restaurant', 
                                   on_delete=models.SET_NULL, 
                                   related_name='orders_restaurant',
                                   blank=True, 
                                   null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rider = models.ForeignKey('accounts.User', 
                              on_delete=models.SET_NULL, 
                              null=True, 
                              blank=True, 
                              related_name='orders_riders')
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    delivery_address = models.TextField()
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    placed_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    tracking_code = models.CharField(max_length=30, unique=True, blank=True)
    payment_method = models.CharField(max_length=30, 
                                      choices=PaymentMethod.choices, 
                                      default=PaymentMethod.CASH_ON_DELIVERY)
    payment_status = models.CharField(max_length=30, 
                                      choices=PaymentStatus.choices, 
                                      default=PaymentStatus.PENDING)
        
        
    @transaction.atomic
    def populate_from_cart(self, cart):
        """
        method to convert a cart to an order.
        """
        #Create Order Items from Cart Items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=self,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price # Snapshot the price!
            )
        
        #Calculate Total (Now that items actually exist in DB)
        aggregate = self.items.aggregate(total_price=models.Sum('subtotal'))
        self.total_amount = (aggregate['total_price'] or Decimal(0.00)) + self.delivery_fee
        #Save the final amount
        self.save(update_fields=['total_amount'])
        #Clear the cart
        cart.items.all().delete()
        cart.update_total()

    @staticmethod
    def tracking_code_generator():
        return f"DLV-{uuid.uuid4().hex[:12].upper()}"

    def save(self, *args, **kwargs):
        # 1. Generate tracking code if not already set
        if not self.tracking_code:
            self.tracking_code = self.tracking_code_generator()
        
        # 2. Call parent save
        super().save(*args, **kwargs)

    def tracking_code_generator(self):
        import uuid
        return f"DLV-{uuid.uuid4().hex[:8].upper()}"
        
        

    def __str__(self):
        return f"Order {self.id} by {self.customer} with tracking {self.tracking_code}"
    
    class Meta:
        ordering = ['-placed_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
    
    def get_menu_item_name(self):
        return self.menu_item.name if self.menu_item else "Item no longer available"
    
    def __str__(self):
        return f"{self.quantity} x {self.get_menu_item_name()} in Order {self.order.id}"