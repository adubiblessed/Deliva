from django.urls import path

#not tested yet 

from .views import (
    CartView,
    CartItemView,
    CartItemEachView,
    OrderCheckoutView,
    OrderView,
    OrderDetailsView,
    OrderStatusUpdateView,
    DeliveryTrackView,
    # RefundRequestView,
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='current_cart'),
    path('cart/items/', CartItemView.as_view(), name='add_cart_item'),
    path('cart/items/<str:id>/', CartItemEachView.as_view(), name='each_cart_item'),
    path('checkout/', OrderCheckoutView.as_view(), name='place_order'),
    path('orders/', OrderView.as_view(), name='list_user_orders'),
    path('orders/<str:id>/', OrderDetailsView.as_view(), name='order_details'),
    path('orders/<str:id>/status/', OrderStatusUpdateView.as_view(), name='update_order_status'),
    path('orders/<str:id>/track/', DeliveryTrackView.as_view(), name='track_order'),
    # path('orders/<str:id>/refund/', RefundRequestView.as_view(), name='request_refund'),
]
