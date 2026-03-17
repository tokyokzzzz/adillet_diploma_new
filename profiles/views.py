from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import Http404
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from .models import ApplicantProfile, MentorProfile, VerificationRequest, SavedMentor
from .forms import ApplicantProfileForm, MentorProfileForm, VerificationRequestForm


@login_required
def edit_applicant_profile(request):
    profile, _ = ApplicantProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ApplicantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect("applicant_dashboard")
    else:
        form = ApplicantProfileForm(instance=profile)

    return render(request, "profiles/edit_applicant.html", {"form": form})


@login_required
def edit_mentor_profile(request):
    profile, _ = MentorProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MentorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _("Profile updated successfully."))
            return redirect("mentor_dashboard")
    else:
        form = MentorProfileForm(instance=profile)

    return render(request, "profiles/edit_mentor.html", {"form": form})


@login_required
def submit_verification(request):
    if not request.user.is_mentor():
        raise Http404

    # Get existing request if any
    existing = VerificationRequest.objects.filter(mentor=request.user).first()

    # If approved, nothing more to do
    if existing and existing.is_approved():
        return render(request, "profiles/verification_request.html", {
            "existing": existing,
            "form": None,
        })

    # If pending, just show status — no resubmission allowed while under review
    if existing and existing.is_pending():
        return render(request, "profiles/verification_request.html", {
            "existing": existing,
            "form": None,
        })

    # No request yet, or previous was rejected → allow submission / resubmission
    if request.method == "POST":
        form = VerificationRequestForm(request.POST, instance=existing)
        if form.is_valid():
            ver_req = form.save(commit=False)
            ver_req.mentor = request.user
            ver_req.status = VerificationRequest.STATUS_PENDING
            ver_req.reviewed_at = None
            ver_req.save()
            messages.success(request, _("Verification request submitted. We will review it shortly."))
            return redirect("submit_verification")
    else:
        form = VerificationRequestForm(instance=existing)

    return render(request, "profiles/verification_request.html", {
        "existing": existing,
        "form": form,
    })


@login_required
def saved_mentors(request):
    if not request.user.is_applicant():
        raise Http404
    saves = (
        SavedMentor.objects
        .filter(applicant=request.user)
        .select_related("mentor__mentor_profile")
        .annotate(avg_rating=Avg("mentor__received_reviews__rating"))
    )
    return render(request, "profiles/saved_mentors.html", {"saves": saves})


@login_required
@require_POST
def toggle_save_mentor(request, mentor_pk):
    if not request.user.is_applicant():
        raise Http404
    mentor_profile = get_object_or_404(MentorProfile, pk=mentor_pk)
    mentor_user = mentor_profile.user
    existing = SavedMentor.objects.filter(applicant=request.user, mentor=mentor_user).first()
    if existing:
        existing.delete()
    else:
        SavedMentor.objects.create(applicant=request.user, mentor=mentor_user)
    # Redirect back to where the request came from
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "saved_mentors"
    return redirect(next_url)
