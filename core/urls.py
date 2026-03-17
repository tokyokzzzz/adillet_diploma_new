from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("dashboard/applicant/", views.applicant_dashboard, name="applicant_dashboard"),
    path("dashboard/mentor/", views.mentor_dashboard, name="mentor_dashboard"),
    path("mentors/", views.mentor_list, name="mentor_list"),
    path("mentors/<int:pk>/", views.mentor_detail, name="mentor_detail"),
]
