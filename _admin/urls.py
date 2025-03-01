from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("members/", views.dashboard_member, name="dashboard_members"),
    path("projects/", views.dashboard_project, name="dashboard_projects"),
    path("projects/all/", views.all_projects, name="all_projects"),
    path("members/all/", views.all_members, name="all_members"),
    path("create-user/", views.create_user, name="create_user"),
    path("deactivate-user/", views.deactivate_user, name="deactivate_user"),
    path("activate-user/", views.activate_user, name="activate_user"),
    path("delete-user/", views.delete_user, name="delete_user"),
    path("settings/", views.settings, name="settings"),
    path("change-password/", views.change_password, name="change-password"),
]
