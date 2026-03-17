from django.contrib import admin
from .models import Conversation, Message, MentorReview


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("applicant", "mentor", "status", "created_at", "updated_at")
    list_filter = ("status",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation", "sender", "timestamp", "text")
    list_filter = ("timestamp",)


@admin.register(MentorReview)
class MentorReviewAdmin(admin.ModelAdmin):
    list_display = ("applicant", "mentor", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("applicant__username", "mentor__username")
    readonly_fields = ("created_at",)
