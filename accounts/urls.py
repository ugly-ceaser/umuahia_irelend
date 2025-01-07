from django.urls import path
from .views import (
    user_login,
    user_register,
    user_logout,
    verificaton_email_sent,
    verify_account,
)

app_name = "accounts"

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    path(
        "verification/email/sent/",
        verificaton_email_sent,
        name="verificaton_email_sent",
    ),
    path("verification/email/<str:token>/", verify_account, name="verify_account"),
    path("logout/", user_logout, name="logout"),
]
