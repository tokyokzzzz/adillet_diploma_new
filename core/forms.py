from django import forms


COUNTRY_DIFFICULTY_CHOICES = [
    ("easy",      "Easy — less selective, lower requirements"),
    ("moderate",  "Moderate — average competition"),
    ("hard",      "Hard — selective, high requirements"),
    ("very_hard", "Very Hard — extremely selective (e.g. US, UK top unis)"),
]

UNIVERSITY_COMPETITIVENESS_CHOICES = [
    ("low",       "Low — regional or open-admission university"),
    ("medium",    "Medium — average national university"),
    ("high",      "High — well-ranked national university"),
    ("very_high", "Very High — top-ranked / Ivy League equivalent"),
]

SCORE_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CalculatorForm(forms.Form):
    gpa = forms.FloatField(
        label="GPA (0.0 – 4.0 scale)",
        min_value=0.0,
        max_value=4.0,
        widget=forms.NumberInput(attrs={"step": "0.01", "placeholder": "e.g. 3.5"}),
        help_text="Your cumulative GPA on a 4.0 scale.",
    )
    english_score = forms.FloatField(
        label="English Proficiency Score (IELTS 0–9)",
        min_value=0.0,
        max_value=9.0,
        widget=forms.NumberInput(attrs={"step": "0.5", "placeholder": "e.g. 6.5"}),
        help_text="IELTS band score. If you have TOEFL, divide by 12 to convert roughly.",
    )
    motivation = forms.ChoiceField(
        label="Motivation Strength (1 = weak, 10 = exceptional)",
        choices=SCORE_CHOICES,
        help_text="How strong is your statement of purpose / personal motivation?",
    )
    extracurricular = forms.ChoiceField(
        label="Extracurricular Strength (1 = none, 10 = outstanding)",
        choices=SCORE_CHOICES,
        help_text="Research, volunteering, competitions, internships, etc.",
    )
    country_difficulty = forms.ChoiceField(
        label="Target Country Difficulty",
        choices=COUNTRY_DIFFICULTY_CHOICES,
    )
    university_competitiveness = forms.ChoiceField(
        label="Target University Competitiveness",
        choices=UNIVERSITY_COMPETITIVENESS_CHOICES,
    )
