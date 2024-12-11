from django.core.mail import send_mail


def send_message(subject, message, html_message, sender, reciepient):
    send_mail(
        subject,
        message,
        sender,
        [reciepient],
        html_message=html_message,
        fail_silently=False,
    )
