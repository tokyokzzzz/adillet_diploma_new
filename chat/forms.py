from django import forms


class MessageForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Write a message...", "class": "form-control"}),
        max_length=2000,
        label="",
    )
