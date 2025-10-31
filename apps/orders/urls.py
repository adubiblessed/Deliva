from django.urls import path

from .views import (
    CartView,
    # CartItemCreateView,
    # CartItemEachView,
    # CheckoutView,
    # OrderListView,
    # OrderDetailView,
    # OrderStatusUpdateView,
    # OrderTrackingView,
    # RefundRequestView,
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='current_cart'),
    # path('cart/items/', CartItemCreateView.as_view(), name='add_cart_item'),
    # path('cart/items/<int:id>/', CartItemEachView.as_view(), name='each_cart_item'),
    # path('checkout/', CheckoutView.as_view(), name='place_order'),
    # path('orders/', OrderListView.as_view(), name='list_user_orders'),
    # path('orders/<int:id>/', OrderDetailView.as_view(), name='order_details'),
    # path('orders/<int:id>/status/', OrderStatusUpdateView.as_view(), name='update_order_status'),
    # path('orders/<int:id>/track/', OrderTrackingView.as_view(), name='track_order'),
    # path('orders/<int:id>/refund/', RefundRequestView.as_view(), name='request_refund'),
]
