from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from users.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .utils import send_message
from umuahia_ireland.settings import APP_NAME, APP_URL
from django.template.loader import render_to_string
from .decorators import admin_required
from django.db import transaction


# Create your views here.
@admin_required
def dashboard_member(request):
    users = CustomUser.objects.all()
    total_users = CustomUser.objects.count()

    context = {"users": users, "total_users": total_users}

    return render(request, "_admin/dashboard.html", context)

@admin_required
def dashboard_project(request):
    users = CustomUser.objects.all()
    total_users = CustomUser.objects.count()

    context = {"users": users, "total_users": total_users}

    return render(request, "_admin/dashboard-projects.html", context)


@admin_required
def all_members(request):
    return render(request, "_admin/members.html")

@admin_required
def all_projects(request):
    return render(request, "_admin/projects.html")


@admin_required
def create_user(request):
    if request.method == "POST":
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        email = request.POST.get("email")
        position = request.POST.get("position")

        isAdmin = True if position == "admin" else False

        if CustomUser.objects.filter(email=email).exists():
            # messages.error(request, "Email already exists")
            return HttpResponse("Email already exists", status=400)

        with transaction.atomic():
            new_user = CustomUser.objects.create(
                firstName=firstName,
                lastName=lastName,
                email=email,
                is_active=True,
                is_staff=isAdmin,
                is_superuser=isAdmin,
            )
            new_user.save()
        # messages.success(
        #     request,
        #     f"User {new_user.firstName} {new_user.lastName} created successfully",
        # )
        return redirect(reverse("_admin:dashoard"))
    else:
        return HttpResponse("Invalid request", status=400)


@admin_required
def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
        return redirect(reverse("_admin:dashboard"))
    else:
        return HttpResponse("User is already deactivated")


@admin_required
def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        return redirect(reverse("_admin:dashboard"))
    else:
        return HttpResponse("User is already active")


@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.delete()
        return redirect(reverse("_admin:dashboard"))
    else:
        return render(request, "_admin/user/delete.html", {"user": user})


@admin_required
def settings(request):
    return render(request, "_admin/settings.html")


@admin_required
def change_password(request):
    if request.method == "POST":
        currentPassword = request.POST.get("current_password")
        newPassword = request.POST.get("newPassword")
        confirmPassword = request.POST.get("confirmPassword")

        hashed_password = make_password(newPassword)

        user = CustomUser.objects.get(id=request.user.id)

        if not user.check_password(currentPassword):
            messages.error(request, "Current password is incorrect!")
            return render(request, "_admin/settings.html")

        if not newPassword == confirmPassword:
            messages.error(request, "Passwords do not match!")
            return render(request, "_admin/settings.html")

        if newPassword == currentPassword:
            messages.error(request, "The new password cannot be your current password!")
            return render(request, "_admin/settings.html")

        user.password = hashed_password
        user.save()

        # Send welcome email
        subject = f"Admin Password Changed"
        context = {
            "APP_NAME": APP_NAME,
            "APP_URL": APP_URL,
        }
        body = render_to_string("email/admin/password-changed.html", context)
        send_message(user, subject, "", body)

    return render(request, "_admin/settings.html")
