from django.utils import timezone
from umuahia_ireland.settings import DEFAULT_EMAIL
from django.core.mail import send_mail


def send_verification_email(user, subject, message, token, html_message):
    user.verification_token = token
    user.token_created_at = timezone.now()
    user.save()

    send_mail(
        subject,
        message,
        DEFAULT_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
