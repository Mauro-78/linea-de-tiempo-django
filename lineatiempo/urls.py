from django.urls import path
from . import views

urlpatterns = [
    path("", views.timeline_view, name="timeline"),
    path("api/eventos/", views.eventos_api, name="eventos_api"),
]
