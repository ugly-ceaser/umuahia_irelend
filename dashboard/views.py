from django.shortcuts import render
from .decorators import validation_required


@validation_required
def dashboard(request):
    return render(request, "user/profile.html")

@validation_required
def minuites(request):
    return render(request, "user/minuites.html")

@validation_required
def settings(request):
    return render(request, "user/settins.html")

@validation_required
def update_profile(request):
    return render(request, "user/update_profile.html")
