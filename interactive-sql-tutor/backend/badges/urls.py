from django.urls import path
from .views import AllBadgesView, UserBadgesView

urlpatterns = [
    path('', AllBadgesView.as_view(), name='all-badges'),
    path('user/', UserBadgesView.as_view(), name='user-badges'),
]