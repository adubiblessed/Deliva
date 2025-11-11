from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from apps.restaurants.models import Restaurant
from .models import Cart, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer, OrderItemSerializer

class CartView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        cart = Cart.objects.filter(customer=request.user).first()
        item = OrderItem.objects.filter(cart=cart)
        if not cart:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        itemserializer = OrderItemSerializer(item, many=True)
        serializer = CartSerializer(cart)
        serializer_data = serializer.data
        serializer_data['items'] = itemserializer.data
        return Response(serializer_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CartItemEachView(APIView):
    authentication_classes = [TokenAuthentication]

    def put(self, request, pk):
        try:
            item = OrderItem.objects.get(pk=pk, cart__user=request.user)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = OrderItem.objects.get(pk=pk, cart__user=request.user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class OrderDetailsView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class OrderCheckoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        cart = Cart.objects.filter(customer=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            customer=request.user,
            restaurant=cart.restaurant,
            delivery_address=request.data.get('delivery_address', ''),
            delivery_fee=request.data.get('delivery_fee', 0.0),
            payment_method=request.data.get('payment_method', 'CASH_ON_DELIVERY')
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.subtotal
            )

        cart.items.all().delete()  # Clear the cart after checkout

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class OrderStatusUpdateView(APIView):
    authentication_classes = [TokenAuthentication]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
