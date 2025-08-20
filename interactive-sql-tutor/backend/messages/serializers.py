from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'is_read', 'timestamp']
        read_only_fields = ['id', 'sender', 'is_read', 'timestamp']