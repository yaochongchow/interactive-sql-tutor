from django.urls import path
from .views import UserAnalyticsView, ProblemAnalyticsView

urlpatterns = [
    path('', UserAnalyticsView.as_view(), name='user-analytics'),
    path('<int:problem_id>/', ProblemAnalyticsView.as_view(), name='problem-analytics'),
]