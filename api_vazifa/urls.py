from django.urls import path
from .views import UserListAPIView, UserDetailAPIView, ObHavoAPIView

urlpatterns = [
    path('api/users/', UserListAPIView.as_view()),
    path('api/users/<int:user_id>/', UserDetailAPIView.as_view()),
    path('api/ob-havo/', ObHavoAPIView.as_view()),
]