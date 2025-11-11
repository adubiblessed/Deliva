from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from .serializers import RiderProfileSerializer, DeliveryAssignmentSerializer, VehicleSerializer
from .models import RiderProfile, DeliveryAssignment, Vehicle
from apps.restaurants.models import Delivery
from apps.restaurants.serializers import DeliverySerializer


class RiderProfileView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = RiderProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        couriers = RiderProfile.objects.all()
        serializer = RiderProfileSerializer(couriers, many=True)
        return Response(serializer.data)
    
class EachRiderProfileView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            rider = RiderProfile.objects.get(pk=pk)
        except RiderProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RiderProfileSerializer(rider)
        return Response(serializer.data)

class DeliveryAssignmentView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = DeliveryAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeliveryAssignmentViewAll(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        assignments = DeliveryAssignment.objects.all()
        serializer = DeliveryAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    

class VehicleView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #also add the rider that owns or man the vehicle
    def get(self, request):
        vehicles = Vehicle.objects.all()
        for each in vehicles:
            each.rider = RiderProfileSerializer(each.rider).data
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    

class RiderDeliveriesView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        deliveries = Delivery.objects.filter(rider_id=id)
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)


class DeliveryStatusUpdateView(APIView):
    authentication_classes = [TokenAuthentication]

    def patch(self, request, id):
        try:
            delivery = Delivery.objects.get(id=id)
        except Delivery.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DeliverySerializer(delivery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeliveryTrackView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        try:
            delivery = Delivery.objects.get(id=id)
        except Delivery.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

class DeliveryByRiderView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, rider_id):
        deliveries = Delivery.objects.filter(rider_id=rider_id)
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)
