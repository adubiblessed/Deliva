from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from apps.customers.models import Address

from apps.customers.serializers import UserAddressSerializer
# Create your views here.


class UserAddress(APIView):
    authentication_classes = []
    permission_classes = []


    def post(self, request, user_id):
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request, user_id):
        try:
            address = Address.objects.filter(user_id=user_id)
        except Address.DoesNotExist:
            return Response({"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

        serialiser = UserAddressSerializer(address, many=True)
        return Response(serialiser.data, status=status.HTTP_200_OK)