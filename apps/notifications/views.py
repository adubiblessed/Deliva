from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from apps.notifications.services import NotificationService
from apps.notifications.serializers import NotificationSerializer, NotificationTemplateSerializer




class ApiNotification(APIView):
    
    def get(self):
        pass

class CreateNotificationTemplate(APIView):
    def post(self, request):
        serializer = NotificationTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
              "message": "Notification Template registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PushNotification(APIView):
    def post(self, request):
        
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()

            notify = NotificationService()
            final =  notify.notification_contents(template=notification.content.template,payload=notification.payload)
            print(final)

            return Response({
            "message": "Notification sent successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)