from django.urls import path
from .views import register_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import CustomTokenObtainPairView, LogoutView, UserUpdateView

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh token
    path("logout/", LogoutView.as_view(), name="logout"), # logout
    path('update/', UserUpdateView.as_view(), name='user-update'),
]