from django.urls import path
from .views import RestaurantsApiView, AllRestaurantsApiView, EachRestaurantApiView, RestaurantMenuApiView

urlpatterns = [
    path('', RestaurantsApiView.as_view(), name='restaurant-list'),
    path('all/', AllRestaurantsApiView.as_view(), name='all-restaurant-list'),
    path('<str:pk>/', EachRestaurantApiView.as_view(), name='restaurant-detail'),
    path('<str:pk>/menu/', RestaurantMenuApiView.as_view(), name='restaurant-menu'),
]