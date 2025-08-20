# comments/serializers.py

from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'problem_id', 'user', 'content', 'timestamp']
        read_only_fields = ['comment_id', 'user', 'timestamp']