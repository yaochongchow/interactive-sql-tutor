# comments/urls.py
from django.urls import path
from .views import CommentListView, CommentAddView

urlpatterns = [
    path('<int:problem_id>/', CommentListView.as_view(), name='comment-list'),
    path('<int:problem_id>/add/', CommentAddView.as_view(), name='comment-add'),
]