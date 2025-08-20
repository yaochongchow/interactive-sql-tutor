from rest_framework import serializers
from .models import ProblemAttempt

class ProblemAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemAttempt
        fields = ['id', 'user', 'problem', 'is_correct', 'attempt_time']