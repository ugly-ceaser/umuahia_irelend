from django.shortcuts import render
from .decorators import validation_required


@validation_required
def dashboard(request):
    return render(request, "dashboard/index.html")
