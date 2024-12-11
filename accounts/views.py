from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from django.contrib import messages
from umuahia_ireland.settings import APP_NAME, APP_URL, EMAIL_HOST_USER
from django.template.loader import render_to_string
from umuahia_ireland.utils import send_message
from django.http import Http404
from django.contrib.auth.decorators import login_required


# Function based handler views
def user_register(request):
    """
    Handles user registration. This function retrieves user data from POST request,
    checks if the email already exists, ensures passwords match, and creates a new user.
    If successful, logs in the user and sends a welcome email.

    Parameters:
    request (HttpRequest): The HTTP request object containing POST data.

    Returns:
    HttpResponse: Redirects to the registration page on failure or the dashboard on success.
    """

    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect(reverse("dashboard:dashboard"))

    if request.method == "POST":
        try:
            # Retrieve data from POST request
            firstName = request.POST.get("firstName")
            lastName = request.POST.get("lastName")
            email = request.POST.get("email")
            password = request.POST.get("password")
            cmfpassword = request.POST.get("cmfpassword")

            # Hash the password
            hashed_password = make_password(password)

            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, message="Email already exists!")

            # Check if passwords match
            if password != cmfpassword:
                messages.error(request, message="Passwords do not match!")

            # Create a new user
            new_user = CustomUser.objects.create(
                first_name=firstName,
                last_name=lastName,
                email=email,
                password=hashed_password,
            )
            new_user.save()
            login(request, new_user)  # Log the user in

            # Send welcome email
            subject = (
                f"🎉 Welcome to {APP_NAME} {new_user.first_name} {new_user.last_name}!"
            )
            context = {"APP_NAME": APP_NAME, "APP_URL": APP_URL}
            body = render_to_string("email/welcome.html", context)
            send_message(subject, "", body, EMAIL_HOST_USER, email)

            return redirect(reverse("dashboard:dashboard"))

        except Exception as e:
            messages.error(request, message="An error occurred!")
    return render(request, "registration/register.html")


from django.contrib.auth.decorators import login_required


def user_login(request):
    """
    Handles user login. This function retrieves the email and password from the POST request,
    checks if the user exists and the password is correct, and logs in the user if successful.

    Parameters:
    request (HttpRequest): The HTTP request object containing POST data.

    Returns:
    HttpResponse: Renders the login page on failure or redirects to the dashboard on success.
    """
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect(reverse("dashboard:dashboard"))

    if request.method == "POST":
        try:
            # Retrieve data from POST request
            email = request.POST.get("email")
            password = request.POST.get("password")

            # Get the user by email
            user = get_object_or_404(CustomUser, email=email)
            if user is not None and user.check_password(password):
                login(request, user)  # Log the user in
                return redirect(reverse("dashboard:dashboard"))
            else:
                messages.error(request, message="Invalid email or password!")
        except Http404:
            messages.error(request, message="Invalid email or password!")
        except Exception as e:
            messages.error(request, message="An error occurred!")

    # Render login page with messages in case of any failure
    return render(request, "registration/login.html")


@login_required
def user_logout(request):
    """
    Handles user logout. Logs the user out and redirects to the home page.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    HttpResponse: Redirects to the home page after logging out.
    """
    logout(request)  # Log the user out
    return redirect(reverse("app:home_page"))
