from django.urls import path
from . import views

urlpatterns = [
    path("applicant/edit/", views.edit_applicant_profile, name="edit_applicant_profile"),
    path("mentor/edit/", views.edit_mentor_profile, name="edit_mentor_profile"),
    path("mentor/verify/", views.submit_verification, name="submit_verification"),
    path("saved/", views.saved_mentors, name="saved_mentors"),
    path("save/<int:mentor_pk>/", views.toggle_save_mentor, name="toggle_save_mentor"),
]
