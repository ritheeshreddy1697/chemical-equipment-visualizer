from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "Backend is running",
        "project": "Chemical Equipment Parameter Visualizer",
        "backend": "Django + Django REST Framework"
    })

urlpatterns = [
    path("", home),                  # 👈 root URL
    path("admin/", admin.site.urls),
    path("api/", include("equipment.urls")),
]