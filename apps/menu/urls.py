from django.urls import path

from .views import MenuItemsApiView, MenuCategoryView, MenuItemDetailView, MenuCategoryDetailView

urlpatterns = [
    path('items/', MenuItemsApiView.as_view(), name='menu-items'),
    path('categories/', MenuCategoryView.as_view(), name='menu-categories'),
    path('items/<str:pk>/', MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('categories/<str:pk>/', MenuCategoryDetailView.as_view(), name='menu-category-detail'),
]