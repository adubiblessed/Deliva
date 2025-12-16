from django.db import models
import re
# Create your models here.
from apps.accounts.models import User


class ChannelType(models.TextChoices):
    API = 'API', 'In-App Notification'
    # SMS = 'SMS', 'SMS'
    # EMAIL = 'EMAIL', 'Email'


# class TriggeredByType(models.TextChoices):
#     SYSTEM = 'SYSTEM', 'System Notification'
#     ADMIN = 'ADMIN', 'Admin Notification'


class TriggerEvent(models.TextChoices):
    WELCOME = 'WELCOME', 'Welcome'
    DELIVERY = 'DELIVERY', 'Delivery'
    PROMOTIONAL = 'PROMOTIONAL', 'Promotional'
    RESET_PASSWORD = 'RESET_PASSWORD', 'Reset Password'

class StatusType(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SUCCESS = 'SUCCESS', 'Success'
    FAILED = 'FAILED', 'Failed'

class NotificationTemplate(models.Model):
    title = models.CharField(max_length=255)
    template = models.TextField(help_text='Use placeholders like {{username}} for personalization.')
    channel = models.CharField(max_length=20, choices=ChannelType.choices, default=ChannelType.API)
    # triggered_by = models.CharField(max_length=20, choices=TriggeredByType.choices, default=TriggeredByType.SYSTEM)
    trigger_event = models.CharField(max_length=50, choices=TriggerEvent.choices, help_text='Event that triggers this template.')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_notifications')
    content = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='api_notifications')
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.PENDING)
    is_read = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

