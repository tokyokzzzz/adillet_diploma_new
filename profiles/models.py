from django.db import models
from django.conf import settings


class ApplicantProfile(models.Model):
    DEGREE_CHOICES = [
        ("bachelor", "Bachelor's"),
        ("master", "Master's"),
        ("phd", "PhD"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applicant_profile"
    )
    full_name = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=80, blank=True, help_text="Your current country")
    target_country = models.CharField(max_length=80, blank=True, help_text="Country you want to study in")
    target_degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, blank=True)
    intended_major = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(max_length=80, blank=True, help_text="e.g. English, German")
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"ApplicantProfile({self.user.username})"

    def is_complete(self):
        return all([self.full_name, self.country, self.target_country, self.intended_major])


class MentorProfile(models.Model):
    DEGREE_CHOICES = [
        ("bachelor", "Bachelor's"),
        ("master", "Master's"),
        ("phd", "PhD"),
        ("other", "Other"),
    ]

    YEAR_CHOICES = [
        ("1", "1st year"),
        ("2", "2nd year"),
        ("3", "3rd year"),
        ("4", "4th year"),
        ("5", "5th year"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentor_profile"
    )
    full_name = models.CharField(max_length=120, blank=True)
    current_country = models.CharField(max_length=80, blank=True)
    university_name = models.CharField(max_length=150, blank=True)
    degree_level = models.CharField(max_length=20, choices=DEGREE_CHOICES, blank=True)
    major = models.CharField(max_length=100, blank=True)
    year_of_study = models.CharField(max_length=10, choices=YEAR_CHOICES, blank=True)
    languages = models.CharField(max_length=200, blank=True, help_text="e.g. English, Russian, Korean")
    bio = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"MentorProfile({self.user.username})"

    def is_complete(self):
        return all([self.full_name, self.current_country, self.university_name, self.major])


class VerificationRequest(models.Model):
    STATUS_PENDING  = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING,  "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    mentor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_request",
    )
    university_name = models.CharField(max_length=150)
    student_id = models.CharField(
        max_length=100,
        help_text="Your student ID or enrollment number as it appears on official documents.",
    )
    note = models.TextField(
        max_length=1000,
        blank=True,
        help_text="Optional: add any details that may help the admin verify your enrollment.",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"VerificationRequest({self.mentor.username}, {self.status})"

    def is_pending(self):
        return self.status == self.STATUS_PENDING

    def is_approved(self):
        return self.status == self.STATUS_APPROVED

    def is_rejected(self):
        return self.status == self.STATUS_REJECTED
