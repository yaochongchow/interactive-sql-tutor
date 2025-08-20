from django.urls import path
from messages.views import MessageListView, MessageSendView

urlpatterns = [
    path('', MessageListView.as_view(), name='message-list'),
    path('send/', MessageSendView.as_view(), name='message-send'),
]