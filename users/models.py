from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

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


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, phone_number, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        if not phone_number:
            raise ValueError("User must have a phone number")

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new superuser profile"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, default="")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    verification_token = models.CharField(max_length=64, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=aware_datetime)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Add 'first_name', 'last_name', or other required fields here

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f"User: {self.email}"
