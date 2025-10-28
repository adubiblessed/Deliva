from django.db import models


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


class Cart(models.Model):
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='carts')
    restaurant = models.ForeignKey('restaurants.Restaurant', 
                                   on_delete=models.CASCADE, 
                                   related_name='carts')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def cal_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total = total
        

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
        self.cart.cal_total()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in {self.cart}"
    
    class Meta:
        unique_together = ('cart', 'menu_item')

class Order(BaseModel):
    customer = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='orders', 
                                 null=True, blank=True)
    restaurant = models.ForeignKey('restaurants.Restaurant', 
                                   on_delete=models.SET_NULL, 
                                   related_name='orders',
                                   blank=True, 
                                   null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rider = models.ForeignKey('couriers.Courier', 
                              on_delete=models.SET_NULL, 
                              null=True, 
                              blank=True, 
                              related_name='orders')
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    delivery_address = models.TextField()
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    placed_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    tracking_code = models.CharField(max_length=30, unique=True)
    payment_method = models.CharField(max_length=30, 
                                      choices=PaymentMethod.choices, 
                                      default=PaymentMethod.CASH_ON_DELIVERY)
    payment_status = models.CharField(max_length=30, 
                                      choices=PaymentStatus.choices, 
                                      default=PaymentStatus.PENDING)

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = self.tracking_code_generator()
        super().save(*args, **kwargs)

    def tracking_code_generator(self):
        import uuid
        return f"DLV-{uuid.uuid4().hex[:8].upper()}"
    
    def cal_total_amount(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total + self.delivery_fee
        

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

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} in Order {self.order.id}"