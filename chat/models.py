from django.db import models
from django.conf import settings


class Conversation(models.Model):
    STATUS_PENDING  = "pending"
    STATUS_ACTIVE   = "active"
    STATUS_DECLINED = "declined"

    STATUS_CHOICES = [
        (STATUS_PENDING,  "Pending"),
        (STATUS_ACTIVE,   "Active"),
        (STATUS_DECLINED, "Declined"),
    ]

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applicant_conversations",
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mentor_conversations",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("applicant", "mentor")
        ordering = ["-updated_at"]

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_active(self):
        return self.status == self.STATUS_ACTIVE

    def is_declined(self):
        return self.status == self.STATUS_DECLINED

    def other_participant(self, user):
        return self.mentor if user == self.applicant else self.applicant

    def __str__(self):
        return f"{self.applicant.username} ↔ {self.mentor.username} [{self.status}]"


class MentorReview(models.Model):
    conversation = models.OneToOneField(
        "Conversation", on_delete=models.CASCADE, related_name="review"
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="given_reviews"
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_reviews"
    )
    rating = models.PositiveSmallIntegerField()  # 1–5
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.applicant.username} for {self.mentor.username} ({self.rating}★)"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender.username}: {self.text[:40]}"
