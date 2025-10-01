from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # Message is new, no history to save
        return
    
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    
    if old_message.content != instance.content:
        # Save old content to history
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content,
            edited_by=old_message.sender  
        )
        # Mark message as edited
        instance.edited = True

@receiver(post_delete, sender=User)
def delete_user_related(sender, instance, **kwargs):
    MessageHistory.objects.filter(edited_by=instance).delete()

    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
