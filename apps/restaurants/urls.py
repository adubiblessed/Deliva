from django.urls import path
from .views import RestaurantsApiView, AllRestaurantsApiView

urlpatterns = [
    path('restaurants/', RestaurantsApiView.as_view(), name='restaurant-list'),
    path('all/', AllRestaurantsApiView.as_view(), name='all-restaurant-list'),
]