from django.contrib import admin
from django.utils import timezone
from .models import ApplicantProfile, MentorProfile, VerificationRequest, SavedMentor


@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "country", "target_country", "intended_major")
    search_fields = ("user__username", "full_name")


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "current_country", "university_name", "is_verified")
    list_filter = ("is_verified",)
    search_fields = ("user__username", "full_name", "university_name")


# ---------------------------------------------------------------------------
# Custom admin actions for verification
# ---------------------------------------------------------------------------

@admin.action(description="Approve selected requests and mark mentor as verified")
def approve_requests(modeladmin, request, queryset):
    for req in queryset.filter(status=VerificationRequest.STATUS_PENDING):
        req.status = VerificationRequest.STATUS_APPROVED
        req.reviewed_at = timezone.now()
        req.save()
        try:
            profile = req.mentor.mentor_profile
            profile.is_verified = True
            profile.save()
        except MentorProfile.DoesNotExist:
            pass


@admin.action(description="Reject selected requests")
def reject_requests(modeladmin, request, queryset):
    for req in queryset.filter(status=VerificationRequest.STATUS_PENDING):
        req.status = VerificationRequest.STATUS_REJECTED
        req.reviewed_at = timezone.now()
        req.save()
        try:
            profile = req.mentor.mentor_profile
            profile.is_verified = False
            profile.save()
        except MentorProfile.DoesNotExist:
            pass


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ("mentor", "university_name", "student_id", "status", "submitted_at", "reviewed_at")
    list_filter = ("status",)
    search_fields = ("mentor__username", "university_name", "student_id")
    readonly_fields = ("submitted_at", "reviewed_at")
    actions = [approve_requests, reject_requests]
    ordering = ("-submitted_at",)


@admin.register(SavedMentor)
class SavedMentorAdmin(admin.ModelAdmin):
    list_display = ("applicant", "mentor", "created_at")
    search_fields = ("applicant__username", "mentor__username")
