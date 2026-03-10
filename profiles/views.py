from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import ApplicantProfile, MentorProfile, VerificationRequest
from .forms import ApplicantProfileForm, MentorProfileForm, VerificationRequestForm


@login_required
def edit_applicant_profile(request):
    profile, _ = ApplicantProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ApplicantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
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
            messages.success(request, "Profile updated successfully.")
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
            messages.success(request, "Verification request submitted. We will review it shortly.")
            return redirect("submit_verification")
    else:
        form = VerificationRequestForm(instance=existing)

    return render(request, "profiles/verification_request.html", {
        "existing": existing,
        "form": form,
    })
