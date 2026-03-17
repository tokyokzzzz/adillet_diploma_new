from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[
            (User.ROLE_APPLICANT, _("Applicant — I want to study abroad")),
            (User.ROLE_MENTOR, _("Mentor — I'm already studying abroad")),
        ]
    )

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")
