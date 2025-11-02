from rest_framework import serializers

from .models import Restaurant, Delivery

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id', 'owner', 'name', 'description', 'logo', 'address', 
            'city', 'phone_number', 'email', 'is_active', 'rating', 
            'open_time', 'close_time', 'delivery_fee', 'min_order_amount'
        ]

        read_only_fields = ['id', 'is_active', 'rating']

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = [
            'id', 'restaurant', 'customer', 'courier', 'order', 
            'status', 'pickup_time', 'delivery_time', 'delivery_address'
        ]

