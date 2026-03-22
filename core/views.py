from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from profiles.models import ApplicantProfile, MentorProfile, VerificationRequest, SavedMentor
from chat.models import MentorReview
from ml.recommender import get_mentor_recommendations



def home_view(request):
    return render(request, "home.html")


@login_required
def applicant_dashboard(request):
    if not request.user.is_applicant():
        return redirect("mentor_dashboard")
    profile, _ = ApplicantProfile.objects.get_or_create(user=request.user)

    recommended = []
    show_recommendations = False

    try:
        all_mentors = MentorProfile.objects.filter(
            is_verified=True
        ).exclude(university_name="").exclude(major="")

        if profile.target_country and profile.intended_major:
            recommended = get_mentor_recommendations(
                profile,
                list(all_mentors),
                top_n=3,
            )
            show_recommendations = True
    except Exception:
        pass

    return render(request, "applicant/dashboard.html", {
        "profile": profile,
        "recommended": recommended,
        "show_recommendations": show_recommendations,
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
        .filter(is_verified=True)
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

    # ML recommendations for logged-in applicants with a complete profile
    recommended = []
    show_recommendations = False

    if request.user.is_authenticated and hasattr(request.user, "role"):
        if request.user.role == "applicant":
            try:
                applicant_profile = ApplicantProfile.objects.get(user=request.user)
                if applicant_profile.target_country and applicant_profile.intended_major:
                    all_mentors = MentorProfile.objects.filter(
                        is_verified=True
                    ).exclude(university_name="").exclude(major="")
                    recommended = get_mentor_recommendations(
                        applicant_profile,
                        list(all_mentors),
                        top_n=5,
                    )
                    show_recommendations = True
            except ApplicantProfile.DoesNotExist:
                pass

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
        "recommended": recommended,
        "show_recommendations": show_recommendations,
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
