# urls.py (inside your app, e.g. llm_integration/urls.py)
from django.urls import path
from .views import get_hint_from_llm

urlpatterns = [
    path("hint/", get_hint_from_llm, name="get_hint_from_llm"),
]