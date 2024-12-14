from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
import uuid

now = timezone.now()
naive_datetime = datetime.datetime(
    year=now.year,
    month=now.month,
    day=now.day,
    hour=now.hour,
    minute=now.minute,
    second=now.second,
)
aware_datetime = timezone.make_aware(
    naive_datetime, timezone=timezone.get_current_timezone()
)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    phone_number = models.CharField(max_length=20, default="")
    verification_token = models.CharField(max_length=64, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def get_username(self):
        return self.email

    def __str__(self):
        return self.email
