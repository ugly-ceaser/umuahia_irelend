from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("profi;e/", views.dashboard, name="dashboard"),
    path("minuites/", views.minuites, name="minuites"),
    path("update-profile/", views.update_profile, name="update_profile"),
    path("settings/", views.settings, name="settings"),
]
