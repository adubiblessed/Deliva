from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from .serialisers import MenuItemSerializers, MenuCategorySerializers
from .models import MenuItem, MenuCategory



class MenuItemsApiView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializers(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = MenuItemSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class MenuItemDetailView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return None

    def get(self, request, pk):
        menu_item = self.get_object(pk)
        if not menu_item:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializers(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        menu_item = self.get_object(pk)
        if not menu_item:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializers(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu_item = self.get_object(pk)
        if not menu_item:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class MenuCategoryView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = MenuCategory.objects.all()
        serializer = MenuCategorySerializers(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MenuCategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Details for each category and adds all items in that category
class MenuCategoryDetailView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MenuCategory.objects.get(pk=pk)
        except MenuCategory.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'error': 'Menu category not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuCategorySerializers(category)
        data = serializer.data
        data['menu_items'] = MenuItemSerializers(category.menu_items.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'error': 'Menu category not found'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)