"""
URL configuration for final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({"message": "Welcome to the SQL Learning Platform API"})

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Root route now handled by group7_app
    path("", include("group7_app.urls")),

    # API routes
    path("api/auth/", include("users.urls")),
    path("api/messages/", include("messages.urls")),
    path("api/notifications/", include("notifications.urls")),
    path('api/comments/', include('comments.urls')),
    path("api/badges/", include("badges.urls")),
    path("api/admin/", include("admin_tools.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/", include("sql_app.urls")),
    path("api/llm/", include("llm.urls")),
    path("api/llm-analytics/", include("llm_analytics.urls")),

]
