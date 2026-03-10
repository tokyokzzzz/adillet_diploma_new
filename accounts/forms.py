from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[
            (User.ROLE_APPLICANT, "Applicant — I want to study abroad"),
            (User.ROLE_MENTOR, "Mentor — I'm already studying abroad"),
        ]
    )

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")
