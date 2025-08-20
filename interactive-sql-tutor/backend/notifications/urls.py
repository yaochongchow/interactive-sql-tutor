from django.urls import path
from .views import NotificationListView, NotificationReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:id>/read/', NotificationReadView.as_view(), name='notification-read'),
]