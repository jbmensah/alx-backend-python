from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Extend Django’s built-in User to add profile fields.
    """
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    A conversation between two or more users.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional for group chats"
    )
    is_group = models.BooleanField(
        default=False,
        help_text="Toggle on for group conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.is_group and self.name:
            return self.name
        # for 1:1 chats, show both usernames
        users = self.participants.all()
        return " & ".join(user.username for user in users)


class Message(models.Model):
    """
    A single message in a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} @ {self.created_at:%Y-%m-%d %H:%M}"
