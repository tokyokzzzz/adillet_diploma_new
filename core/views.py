from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from profiles.models import ApplicantProfile, MentorProfile, VerificationRequest, SavedMentor
from chat.models import MentorReview


def match_mentors(profile):
    """
    Score and rank mentors against an applicant profile.
    Returns up to 5 MentorProfile objects (with match_score attribute), score > 0.

    Scoring:
      +2  target_country    == mentor current_country  (case-insensitive)
      +2  target_degree     == mentor degree_level
      +2  intended_major  found in mentor major        (case-insensitive)
      +1  preferred_language found in mentor languages (case-insensitive)
      +1  mentor is verified (tie-breaker bonus)
    """
    candidates = (
        MentorProfile.objects
        .exclude(full_name="")
        .exclude(current_country="")
        .exclude(university_name="")
        .exclude(major="")
        .select_related("user")
        .annotate(avg_rating=Avg("user__received_reviews__rating"))
    )

    scored = []
    for mentor in candidates:
        score = 0
        if profile.target_country and mentor.current_country.lower() == profile.target_country.lower():
            score += 2
        if profile.target_degree and mentor.degree_level == profile.target_degree:
            score += 2
        if profile.intended_major and mentor.major and profile.intended_major.lower() in mentor.major.lower():
            score += 2
        if profile.preferred_language and mentor.languages and profile.preferred_language.lower() in mentor.languages.lower():
            score += 1
        if mentor.is_verified:
            score += 1
        if score > 0:
            mentor.match_score = score
            scored.append(mentor)

    scored.sort(key=lambda m: m.match_score, reverse=True)
    return scored[:5]


def home_view(request):
    return render(request, "home.html")


@login_required
def applicant_dashboard(request):
    if not request.user.is_applicant():
        return redirect("mentor_dashboard")
    profile, _ = ApplicantProfile.objects.get_or_create(user=request.user)
    recommended = match_mentors(profile)
    return render(request, "applicant/dashboard.html", {
        "profile": profile,
        "recommended": recommended,
    })


@login_required
def mentor_dashboard(request):
    if not request.user.is_mentor():
        return redirect("applicant_dashboard")
    profile, _ = MentorProfile.objects.get_or_create(user=request.user)
    ver_request = VerificationRequest.objects.filter(mentor=request.user).first()
    return render(request, "mentor/dashboard.html", {
        "profile": profile,
        "ver_request": ver_request,
    })


def mentor_list(request):
    # Only mentors with complete profiles are shown
    mentors = (
        MentorProfile.objects
        .exclude(full_name="")
        .exclude(current_country="")
        .exclude(university_name="")
        .exclude(major="")
        .select_related("user")
        .annotate(avg_rating=Avg("user__received_reviews__rating"),
                  review_count=Count("user__received_reviews"))
        .order_by("-is_verified", "full_name")
    )

    country = request.GET.get("country", "").strip()
    university = request.GET.get("university", "").strip()
    major = request.GET.get("major", "").strip()
    degree = request.GET.get("degree", "").strip()
    language = request.GET.get("language", "").strip()

    if country:
        mentors = mentors.filter(current_country__icontains=country)
    if university:
        mentors = mentors.filter(university_name__icontains=university)
    if major:
        mentors = mentors.filter(major__icontains=major)
    if degree:
        mentors = mentors.filter(degree_level=degree)
    if language:
        mentors = mentors.filter(languages__icontains=language)

    # Distinct countries for the filter dropdown
    countries = (
        MentorProfile.objects
        .exclude(current_country="")
        .values_list("current_country", flat=True)
        .distinct()
        .order_by("current_country")
    )

    saved_ids = set()
    if request.user.is_authenticated and request.user.is_applicant():
        saved_ids = set(
            SavedMentor.objects
            .filter(applicant=request.user)
            .values_list("mentor_id", flat=True)
        )

    context = {
        "mentors": mentors,
        "countries": countries,
        "degree_choices": MentorProfile.DEGREE_CHOICES,
        "filters": {
            "country": country,
            "university": university,
            "major": major,
            "degree": degree,
            "language": language,
        },
        "saved_ids": saved_ids,
    }
    return render(request, "mentors/list.html", context)


def mentor_detail(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    if not mentor.is_complete():
        raise Http404
    reviews = MentorReview.objects.filter(mentor=mentor.user).select_related("applicant__applicant_profile")
    avg_rating = reviews.aggregate(avg=Avg("rating"))["avg"]
    is_saved = (
        request.user.is_authenticated
        and request.user.is_applicant()
        and SavedMentor.objects.filter(applicant=request.user, mentor=mentor.user).exists()
    )
    return render(request, "mentors/detail.html", {
        "mentor": mentor,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "review_count": reviews.count(),
        "is_saved": is_saved,
    })
