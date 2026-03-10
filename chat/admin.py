from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "mentor", "status", "created_at", "updated_at")
    list_filter = ("status",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender", "timestamp", "text")
    list_filter = ("timestamp",)
