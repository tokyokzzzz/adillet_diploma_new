from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_APPLICANT = "applicant"
    ROLE_MENTOR = "mentor"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_APPLICANT, "Applicant"),
        (ROLE_MENTOR, "Mentor"),
        (ROLE_ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_APPLICANT)

    def is_applicant(self):
        return self.role == self.ROLE_APPLICANT

    def is_mentor(self):
        return self.role == self.ROLE_MENTOR

    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        return f"{self.username} ({self.role})"
