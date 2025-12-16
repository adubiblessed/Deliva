from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from apps.notifications.services import NotificationService
from apps.notifications.serializers import NotificationSerializer


class ApiNotification(APIView):
    
    def get(self):
        pass


class PushNotification(APIView):
    def post(self, request):
        serializer = NotificationSerializer
        if serializer.is_valid():
            serializer.save()
            return Response({
              "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)