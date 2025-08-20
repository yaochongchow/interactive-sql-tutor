from django.urls import path
from .views import generate_read_query

urlpatterns = [
    path('generate/', generate_read_query, name='generate_read_query'),
]