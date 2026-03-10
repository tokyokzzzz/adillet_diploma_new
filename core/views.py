from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from profiles.models import ApplicantProfile, MentorProfile, VerificationRequest
from .forms import CalculatorForm
from .calculator import estimate


def home_view(request):
    return render(request, "home.html")


@login_required
def applicant_dashboard(request):
    if not request.user.is_applicant():
        return redirect("mentor_dashboard")
    profile, _ = ApplicantProfile.objects.get_or_create(user=request.user)
    return render(request, "applicant/dashboard.html", {"profile": profile})


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
    }
    return render(request, "mentors/list.html", context)


def mentor_detail(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    if not mentor.is_complete():
        raise Http404
    return render(request, "mentors/detail.html", {"mentor": mentor})


@login_required
def calculator_view(request):
    result = None
    form = CalculatorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        result = estimate(
            gpa=form.cleaned_data["gpa"],
            english_score=form.cleaned_data["english_score"],
            motivation=int(form.cleaned_data["motivation"]),
            extracurricular=int(form.cleaned_data["extracurricular"]),
            country_difficulty=form.cleaned_data["country_difficulty"],
            university_competitiveness=form.cleaned_data["university_competitiveness"],
        )

    return render(request, "core/calculator.html", {"form": form, "result": result})
