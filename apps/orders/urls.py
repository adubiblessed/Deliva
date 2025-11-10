from django.urls import path

#not tested yet 

from .views import (
    CartView,
    CartItemView,
    CartItemEachView,
    OrderCheckoutView,
    OrderView,
    # OrderDetailView,
    # OrderStatusUpdateView,
    # OrderTrackingView,
    # RefundRequestView,
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='current_cart'),
    path('cart/items/', CartItemView.as_view(), name='add_cart_item'),
    path('cart/items/<str:id>/', CartItemEachView.as_view(), name='each_cart_item'),
    path('checkout/', OrderCheckoutView.as_view(), name='place_order'),
    path('orders/', OrderView.as_view(), name='list_user_orders'),
    # path('orders/<int:id>/', OrderDetailView.as_view(), name='order_details'),
    # path('orders/<int:id>/status/', OrderStatusUpdateView.as_view(), name='update_order_status'),
    # path('orders/<int:id>/track/', OrderTrackingView.as_view(), name='track_order'),
    # path('orders/<int:id>/refund/', RefundRequestView.as_view(), name='request_refund'),
]
