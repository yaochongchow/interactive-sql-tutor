from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter comments by the problem_id provided in the URL
        problem_id = self.kwargs.get('problem_id')
        return Comment.objects.filter(problem_id=problem_id)

class CommentAddView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Retrieve the problem_id from the URL and set the user from the request
        problem_id = self.kwargs.get('problem_id')
        serializer.save(user=self.request.user, problem_id=problem_id)