from django.db import models

from decimal import Decimal
from core.models import BaseModel

class MenuCategory(BaseModel):
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='menu_categories')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)

    # assign position based on existing categories
    def save(self, *args, **kwargs):
        if not self.position:
            max_position = MenuCategory.objects.filter(restaurant=self.restaurant).aggregate(models.Max('position'))['position__max']
            self.position = (max_position or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    

class MenuItem(BaseModel):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    prep_time_minutes = models.PositiveIntegerField(default=15)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.0'))

    def __str__(self):
        return f"{self.name} - {self.category.name}"
