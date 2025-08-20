from rest_framework import serializers
from .models import SQLProblem
from users.models import User  # Adjust path if needed

class SQLProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SQLProblem
        fields = '__all__'

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']