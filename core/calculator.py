"""
Acceptance Estimation Calculator
---------------------------------
A simple rule-based scoring model for estimating international university
admission likelihood. Designed for transparency and explainability.

Formula overview:
  1. Each input is normalized to a 0–100 scale.
  2. A weighted average produces the base score (weights sum to 1.0).
  3. Country difficulty and university competitiveness apply flat penalties.
  4. The final score is clamped to [0, 100] and mapped to a qualitative label.

Weights:
  GPA                   35%
  English proficiency   30%
  Motivation            20%
  Extracurricular       15%

Penalties (subtracted from base score):
  Country difficulty:
    Easy        0 pts
    Moderate   -5 pts
    Hard      -12 pts
    Very Hard  -20 pts

  University competitiveness:
    Low          0 pts
    Medium       -5 pts
    High        -12 pts
    Very High   -20 pts
"""

# ---------------------------------------------------------------------------
# Weights (must sum to 1.0)
# ---------------------------------------------------------------------------
WEIGHTS = {
    "gpa": 0.35,
    "english": 0.30,
    "motivation": 0.20,
    "extracurricular": 0.15,
}

# ---------------------------------------------------------------------------
# Difficulty penalties (in percentage points, applied after weighted average)
# ---------------------------------------------------------------------------
COUNTRY_PENALTY = {
    "easy": 0,
    "moderate": -5,
    "hard": -12,
    "very_hard": -20,
}

UNIVERSITY_PENALTY = {
    "low": 0,
    "medium": -5,
    "high": -12,
    "very_high": -20,
}

# ---------------------------------------------------------------------------
# Outcome labels
# ---------------------------------------------------------------------------
def get_label(score):
    """Return a qualitative chance label based on the final numeric score."""
    if score >= 76:
        return "Strong Chance"
    elif score >= 56:
        return "Good Chance"
    elif score >= 36:
        return "Moderate Chance"
    else:
        return "Low Chance"


def get_label_color(label):
    """Return a Bootstrap color class for the label badge."""
    return {
        "Strong Chance": "success",
        "Good Chance": "primary",
        "Moderate Chance": "warning",
        "Low Chance": "danger",
    }.get(label, "secondary")


# ---------------------------------------------------------------------------
# Main calculation function
# ---------------------------------------------------------------------------
def estimate(gpa, english_score, motivation, extracurricular,
             country_difficulty, university_competitiveness):
    """
    Calculate an estimated acceptance probability.

    Parameters
    ----------
    gpa : float
        Grade Point Average on a 4.0 scale (0.0 – 4.0).
    english_score : float
        English proficiency score on IELTS scale (0.0 – 9.0).
    motivation : int
        Self-assessed motivation strength (1 – 10).
    extracurricular : int
        Self-assessed extracurricular strength (1 – 10).
    country_difficulty : str
        One of: "easy", "moderate", "hard", "very_hard".
    university_competitiveness : str
        One of: "low", "medium", "high", "very_high".

    Returns
    -------
    dict with keys: score (float), label (str), color (str), breakdown (dict)
    """

    # Step 1: Normalize each input to 0–100
    gpa_norm          = (gpa / 4.0) * 100
    english_norm      = (english_score / 9.0) * 100
    motivation_norm   = ((motivation - 1) / 9) * 100
    extra_norm        = ((extracurricular - 1) / 9) * 100

    # Step 2: Weighted average → base score (0–100)
    base_score = (
        gpa_norm        * WEIGHTS["gpa"]
        + english_norm  * WEIGHTS["english"]
        + motivation_norm * WEIGHTS["motivation"]
        + extra_norm    * WEIGHTS["extracurricular"]
    )

    # Step 3: Apply difficulty penalties
    country_pen    = COUNTRY_PENALTY.get(country_difficulty, 0)
    university_pen = UNIVERSITY_PENALTY.get(university_competitiveness, 0)

    final_score = base_score + country_pen + university_pen

    # Step 4: Clamp to valid range
    final_score = max(0.0, min(100.0, final_score))
    final_score = round(final_score, 1)

    label = get_label(final_score)
    color = get_label_color(label)

    # Breakdown for the results card (for transparency)
    breakdown = {
        "gpa_contribution":          round(gpa_norm * WEIGHTS["gpa"], 1),
        "english_contribution":      round(english_norm * WEIGHTS["english"], 1),
        "motivation_contribution":   round(motivation_norm * WEIGHTS["motivation"], 1),
        "extra_contribution":        round(extra_norm * WEIGHTS["extracurricular"], 1),
        "base_score":                round(base_score, 1),
        "country_penalty":           country_pen,
        "university_penalty":        university_pen,
    }

    return {
        "score": final_score,
        "label": label,
        "color": color,
        "breakdown": breakdown,
    }
