from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from apps.notifications.services import NotificationService
from apps.notifications.serializers import NotificationSerializer


class ApiNotification(APIView):
    
    def get(self):
        pass