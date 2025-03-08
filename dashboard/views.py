from django.shortcuts import render, redirect
from .decorators import validation_required
from django.urls import reverse


@validation_required
def dashboard(request):
    return render(request, "_user/profile.html")


@validation_required
def minuites(request):
    return render(request, "_user/minuites.html")


@validation_required
def settings(request):
    return render(request, "_user/settins.html")


@validation_required
def update_profile(request):
    if request.method == "POST":
        # Handle form submission
        first_name = request.POST.get("fullName").split()[0]
        last_name = request.POST.get("fullName").split()[-1]
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        about = request.POST.get("about")

        # Save changes to the user profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone
        user.location = location
        user.about = about
        user.save()

        return redirect(reverse("user:dashboard"))

    return render(request, "_user/update-profile.html")
