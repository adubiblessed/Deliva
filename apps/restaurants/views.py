from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .models import Restaurant
from apps.menu.models import MenuItem, MenuCategory
from apps.menu.serialisers import MenuItemSerializers
from .serializers import RestaurantSerializer


class RestaurantsApiView(APIView):
    authentication_classes=[TokenAuthentication]
    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        restaurants = Restaurant.objects.filter(owner=request.user)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllRestaurantsApiView(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EachRestaurantApiView(APIView):
    authentication_classes=[TokenAuthentication]
    
    def get_object(self, pk, user):
        try:
            return Restaurant.objects.get(pk=pk, owner=user)
        except Restaurant.DoesNotExist:
            return None

    def get(self, request, pk):
        restaurant = self.get_object(pk, request.user)
        if not restaurant:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        restaurant = self.get_object(pk, request.user)
        if not restaurant:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(pk, request.user)
        if not restaurant:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# return all items that belongs to a restaurant
class RestaurantMenuApiView(APIView):
    def get(self, request, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response({"detail": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
        
        categories = MenuCategory.objects.filter(restaurant=restaurant, is_active=True).order_by('position')
        menu_data = []
        for category in categories:
            items = MenuItem.objects.filter(category=category, is_available=True)
            item_serializer = MenuItemSerializers(items, many=True)
            menu_data.append({
                'category': category.name,
                'items': item_serializer.data
            })
        
        return Response({'restaurant': restaurant.name, 'menu': menu_data}, status=status.HTTP_200_OK)
