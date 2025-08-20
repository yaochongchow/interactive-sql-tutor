from rest_framework import generics, permissions
from .models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer

class AllBadgesView(generics.ListAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserBadgesView(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)