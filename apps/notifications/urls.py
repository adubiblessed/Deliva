from django.urls import path

from apps.notifications.views import CreateNotificationTemplate, PushNotification

urlpatterns = [
    path("template/", CreateNotificationTemplate.as_view(), name="notification_template"),
    path("", PushNotification.as_view(), name="notification_template"),
]