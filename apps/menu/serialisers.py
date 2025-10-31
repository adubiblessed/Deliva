from rest_framework import serializers

from .models import MenuItem, MenuCategory    

class MenuItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 
            'is_available', 'category', 'image'
        ]

class MenuCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = [
            'id', 'restaurant', 'name', 'description', 'is_active', 
            'position'
        ]