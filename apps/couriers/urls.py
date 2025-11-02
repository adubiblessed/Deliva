from django.urls import path

#not tested yet

from .views import (RiderProfileView, EachRiderProfileView, 
                    DeliveryAssignmentViewAll, VehicleView, 
                    DeliveryAssignmentView, RiderDeliveriesView, 
                    DeliveryStatusUpdateView, DeliveryTrackView
                    #DeliveryListView
                    )

urlpatterns = [
    path('', RiderProfileView.as_view(), name='rider-profile'),
    path('<str:pk>/', EachRiderProfileView.as_view(), name='each-rider-profile'),
    path('assign/', DeliveryAssignmentView.as_view(), name='create-delivery-assignment'),
    path('delivery-assignments/', DeliveryAssignmentViewAll.as_view(), name='delivery-assignment'),
    path('vehicles/', VehicleView.as_view(), name='vehicle'),
    path('<str:id>/deliveries/', RiderDeliveriesView.as_view(), name='rider-deliveries'),
    #path('deliveries/', DeliveryListView.as_view(), name='delivery-list'),
    path('deliveries/<str:id>/status/', DeliveryStatusUpdateView.as_view(), name='delivery-status-update'),
    path('deliveries/<str:id>/track/', DeliveryTrackView.as_view(), name='delivery-track'),
]
