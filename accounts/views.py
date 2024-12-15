from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from django.contrib import messages
from umuahia_ireland.settings import APP_NAME, APP_URL, FRONTEND_URL
from django.template.loader import render_to_string
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .utils import send_verification_email
from django.utils.crypto import get_random_string
from django.db import transaction


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
            phone_number = request.POST.get("phone_number")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirmPassword = request.POST.get("confirmPassword")

            print(
                f"""
                    User Data:
                    {phone_number}
                    {email}
                    {password}
                    {confirmPassword}
                """
            )

            # Hash the password
            hashed_password = make_password(password)
            print(f"Hashed password: {hashed_password}")

            print("Checking one1")
            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                print("Email already exists")
                messages.error(request, message="Email already exists!")

            print("Checking two")
            # Check if phone number already exists
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                print("Phone number already exists")
                messages.error(
                    request,
                    message="Phone number is already linked to a different account!",
                )

            print("Checking three")
            # Check if passwords match
            if password != confirmPassword:
                print("Password mismatch")
                messages.error(request, message="Passwords do not match!")

            print("Checking four")
            with transaction.atomic():
                # Create a new user
                new_user = CustomUser.objects.create(
                    email=email,
                    phone_number=phone_number,
                    password=hashed_password,
                )
                print(f"New User: {new_user}")
                new_user.save()

                # Send welcome email
                subject = f"🎉 Welcome to {APP_NAME} {new_user.first_name} {new_user.last_name} {new_user.email}!"
                token = get_random_string(64)
                verification_link = f"{FRONTEND_URL}/auth/verify-email/{token}/"
                context = {
                    "APP_NAME": APP_NAME,
                    "APP_URL": APP_URL,
                    "VERIFICATION_URL": verification_link,
                }
                body = render_to_string("email/welcome.html", context)
                send_verification_email(new_user, subject, "", token, body)

            return redirect(reverse("accounts:verificaton_email_sent"))

        except Exception as e:
            messages.error(request, message="An error occurred!")
    return render(request, "registration/register.html")


def verificaton_email_sent(request):
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect(reverse("dashboard:dashboard"))

    if request.method == "POST":
        try:
            data = request.POST
            email = data.get("email")

            user = get_object_or_404(CustomUser, email=email)

            # Clear the older token
            user.verification_token = None
            user.token_created_at = None
            user.save()

            # Send welcome email
            subject = f"🎉 Welcome to {APP_NAME} {user.first_name} {user.last_name} {user.email}!"
            token = get_random_string(64)
            verification_link = f"{FRONTEND_URL}/auth/verify-email/{token}/"
            context = {
                "APP_NAME": APP_NAME,
                "APP_URL": APP_URL,
                "VERIFICATION_URL": verification_link,
            }
            body = render_to_string("email/welcome.html", context)
            send_verification_email(user, subject, "", token, body)

        except Http404:
            messages.error(request, message="Account not found")
        except Exception as e:
            messages.error(request, message="An error occurred!")

    # Render login page with messages in case of any failure
    return render(request, "registration/verification_email_sent.html")


# Verify Account View
def verify_account(request, token):
    try:
        user = get_object_or_404(CustomUser, verification_token=token)
        print(f"Found user: {user}")
        if user:
            user.verification_token = None
            user.token_created_at = None
            user.user.is_active = True
            user.user.is_verified = True
            user.save()
            return render(
                request,
                "verification_success.html",
                {"message": "Your account has been successfully verified."},
            )
    except Exception as e:
        return render(
            request,
            "registration/verification_failed.html",
            {"error": "Invalid or expired token."},
        )


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
