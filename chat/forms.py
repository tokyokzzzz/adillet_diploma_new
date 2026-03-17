from django import forms
from django.utils.translation import gettext_lazy as _
from .models import MentorReview

RATING_CHOICES = [(i, f"{i} ★") for i in range(1, 6)]


class MentorReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label=_("Rating"),
    )

    class Meta:
        model = MentorReview
        fields = ["rating", "text"]
        labels = {"text": _("Your review")}
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Share your experience with this mentor...",
                "class": "form-control",
            }),
        }


class MessageForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Write a message...", "class": "form-control"}),
        max_length=2000,
        label="",
    )
