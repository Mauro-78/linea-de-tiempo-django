from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("lineatiempo.urls")),   # ← todo lo de la app
]
