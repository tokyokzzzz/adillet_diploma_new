from django import forms
from .models import ApplicantProfile, MentorProfile, VerificationRequest


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        fields = [
            "full_name",
            "country",
            "target_country",
            "target_degree",
            "intended_major",
            "preferred_language",
            "bio",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = [
            "full_name",
            "current_country",
            "university_name",
            "degree_level",
            "major",
            "year_of_study",
            "languages",
            "bio",
            "availability_status",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class VerificationRequestForm(forms.ModelForm):
    class Meta:
        model = VerificationRequest
        fields = ["university_name", "student_id", "note"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 4}),
        }
