from rest_framework import serializers
from apps.customers.models import Address



class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'