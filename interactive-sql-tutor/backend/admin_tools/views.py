from rest_framework import generics, permissions
from .models import SQLProblem
from .serializers import SQLProblemSerializer, UserListSerializer
from users.models import User
from .permissions import IsAdmin, IsAdminOrInstructor

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]

class CreateSQLProblemView(generics.CreateAPIView):
    serializer_class = SQLProblemSerializer
    permission_classes = [IsAdminOrInstructor]

class EditSQLProblemView(generics.RetrieveUpdateAPIView):
    queryset = SQLProblem.objects.all()
    serializer_class = SQLProblemSerializer
    permission_classes = [IsAdminOrInstructor]
    lookup_field = 'id'

class DeleteSQLProblemView(generics.DestroyAPIView):
    queryset = SQLProblem.objects.all()
    serializer_class = SQLProblemSerializer
    permission_classes = [IsAdminOrInstructor]
    lookup_field = 'id'