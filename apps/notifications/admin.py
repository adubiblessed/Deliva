from django.contrib import admin

# Register your models here.
from apps.notifications.models import Notification, NotificationTemplate

admin.site.register(Notification)
admin.site.register(NotificationTemplate)