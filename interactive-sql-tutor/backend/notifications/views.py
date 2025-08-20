from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer, NotificationReadSerializer

# List notifications for the authenticated user
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return notifications for the current user
        return Notification.objects.filter(user=self.request.user)

# Mark a notification as read
class NotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_url_kwarg = 'id'

    def patch(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, id=kwargs.get('id'), user=request.user)
        serializer = self.get_serializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_read=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)