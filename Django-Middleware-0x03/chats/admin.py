from django.contrib import admin
from .models import User, Conversation, Message

# Register your models
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("role", "is_staff", "is_superuser")

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")
    filter_horizontal = ("participants",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "conversation", "sender", "sent_at")
    search_fields = ("message_body", "sender__email")
