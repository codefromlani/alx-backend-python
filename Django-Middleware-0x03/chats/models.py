import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, password=None,
                    phone_number=None, role="guest", **extra_fields):
        """Create and save a regular User."""
        if not email:
            raise ValueError("The Email field must be set")
        if not first_name or not last_name:
            raise ValueError("First name and last name must be set")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name="Admin", last_name="User",
                         password=None, **extra_fields):
        """Create and save a SuperUser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if password is None:
            raise ValueError("Superuser must have a password.")

        return self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role="admin",
            **extra_fields
        )

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)

    ROLE_CHOICES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.strip().title()
        if self.last_name:
            self.last_name = self.last_name.strip().title()
        if self.email:
            self.email = self.email.strip().lower()
        if self.phone_number:
            self.phone_number = self.phone_number.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.message_body:
            # assign stripped text back (previous code called strip but didn't assign)
            self.message_body = self.message_body.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        snippet = (self.message_body[:50] + "...") if len(self.message_body) > 50 else self.message_body
        return f"Message {self.message_id} by {self.sender}: {snippet}"

    class Meta:
        ordering = ["-sent_at"]
