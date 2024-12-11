from django.urls import path
from .views import index

app_name = "_admin"

urlpatterns = [path("dashboard/", index, name="admin_dashboard")]
