from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfile, UserLogoutView, MeProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('me/', MeProfileView.as_view(), name='me_profile'),
]