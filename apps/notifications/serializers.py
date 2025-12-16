from rest_framework import serializers
from apps.notifications.models import NotificationTemplate, ApiNotification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'
