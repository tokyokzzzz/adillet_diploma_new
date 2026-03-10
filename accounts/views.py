from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignupForm
from .models import User


def signup_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect_by_role(user)
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


def redirect_by_role(user):
    if user.is_admin_role() or user.is_staff:
        return redirect("/admin/")
    elif user.is_mentor():
        return redirect("mentor_dashboard")
    else:
        return redirect("applicant_dashboard")
