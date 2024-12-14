from django.shortcuts import render
from umuahia_ireland.config import APP_NAME


# Create your views here.
def index(request):
    return render(request, "index.html")
