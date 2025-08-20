from django.urls import path
from .views import UserListView, CreateSQLProblemView, EditSQLProblemView, DeleteSQLProblemView

urlpatterns = [
    path('users/', UserListView.as_view(), name='admin-user-list'),
    path('problems/create/', CreateSQLProblemView.as_view(), name='admin-create-problem'),
    path('problems/<int:id>/edit/', EditSQLProblemView.as_view(), name='admin-edit-problem'),
    path('problems/<int:id>/delete/', DeleteSQLProblemView.as_view(), name='admin-delete-problem'),
]