from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        if self.parent_message:
            return f"Reply from {self.sender} to {self.receiver} (parent {self.parent_message.id})"
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    def get_thread(self):
        """
        Recursively fetch this message and all its replies in a nested dict.
        """
        return {
            "id": self.id,
            "sender": self.sender.username,
            "receiver": self.receiver.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "replies": [reply.get_thread() for reply in self.replies.all()]
        }


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - Message {self.message.id}"
    

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"
