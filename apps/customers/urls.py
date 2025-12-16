from django.urls import path
from .views import UserAddress

urlpatterns = [
 path("<int:user_id>/address/", UserAddress.as_view(), name="user_address"),
]