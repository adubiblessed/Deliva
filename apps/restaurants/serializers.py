from rest_framework import serializers

from .models import Restaurant 

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id', 'owner', 'name', 'description', 'logo', 'address', 
            'city', 'phone_number', 'email', 'is_active', 'rating', 
            'open_time', 'close_time', 'delivery_fee', 'min_order_amount'
        ]

        