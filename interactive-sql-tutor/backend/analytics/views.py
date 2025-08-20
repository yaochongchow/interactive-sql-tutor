from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import ProblemAttempt
from .serializers import ProblemAttemptSerializer
from admin_tools.models import SQLProblem

class UserAnalyticsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        attempts = ProblemAttempt.objects.filter(user=request.user)
        correct = attempts.filter(is_correct=True).count()
        total = attempts.count()
        return Response({
            "total_attempts": total,
            "correct_attempts": correct,
            "accuracy": f"{(correct / total * 100):.2f}%" if total > 0 else "N/A"
        })

class ProblemAnalyticsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, problem_id):
        attempts = ProblemAttempt.objects.filter(problem__id=problem_id)
        correct = attempts.filter(is_correct=True).count()
        total = attempts.count()
        return Response({
            "problem_id": problem_id,
            "total_attempts": total,
            "correct_attempts": correct,
            "accuracy": f"{(correct / total * 100):.2f}%" if total > 0 else "N/A"
        })