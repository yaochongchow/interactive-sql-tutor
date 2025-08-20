from rest_framework import generics, permissions, serializers
from .models import Message
from .serializers import MessageSerializer

class MessageListView(generics.ListAPIView):
    """
    Lists messages for the authenticated user.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return messages where the recipient is the current user
        return Message.objects.filter(recipient=self.request.user)


class MessageSendView(generics.CreateAPIView):
    """
    Allows sending a new message with role-based restrictions.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        recipient = serializer.validated_data.get('recipient')
        
        # Admin (or superuser) can send messages to anyone.
        if sender.role == 'admin' or sender.is_superuser:
            serializer.save(sender=sender)
            return
        
        # Instructors can send messages to instructors and students.
        if sender.role == 'instructor':
            if recipient.role in ['instructor', 'student', 'admin']:
                serializer.save(sender=sender)
                return
            else:
                raise serializers.ValidationError("Invalid Permission.")
        
        # Students can only send messages to instructors.
        if sender.role == 'student':
            if recipient.role == 'instructor':
                serializer.save(sender=sender)
                return
            else:
                raise serializers.ValidationError("Invalid Permission: Students can only send messages to instructors.")
        
        raise serializers.ValidationError("You are not allowed to send messages.")