from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
              "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    #
    authentication_classes = []
    permission_classes = []


    def post(self, request):
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': str(user.id),
                'email': user.email
                }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class UserProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user_id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'phone_no': user.phone_no
        }, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        data = request.data

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone_no = data.get('phone_no', user.phone_no)
        user.save()

        return Response({
            'message': 'Profile updated successfully'
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        data = request.data

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone_no = data.get('phone_no', user.phone_no)
        user.save()

        return Response({
            'message': 'Profile partially updated successfully'
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)