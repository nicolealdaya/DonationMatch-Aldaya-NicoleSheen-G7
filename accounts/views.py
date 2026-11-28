from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import (
   UserRegistrationForm,
   ProfileUpdateForm,
   DonationForm,
   RequestForm,
)
from .models import Organization, Donation, Request

def register_view(request):
   if request.method == "POST":
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(
               request,
               "Your account has been created successfully! You can now log in."
           )
           return redirect("login")
   else:
       form = UserRegistrationForm()
   return render(
       request,
       "accounts/register.html",
       {"form": form}
   )

def login_view(request):
   if request.method == "POST":
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
           user = form.get_user()
           login(request, user)
           return redirect("dashboard")
   else:
       form = AuthenticationForm()
   return render(
       request,
       "accounts/login.html",
       {"form": form}
   )

@login_required
def dashboard_view(request):
   organization = None
   donations = None
   requests = None
   if request.user.role == "donor":
       donations = Donation.objects.filter(user=request.user)
   elif request.user.role == "organization":
       try:
           organization = request.user.organization
           requests = Request.objects.filter(
               organization=organization
           )
       except Organization.DoesNotExist:
           pass
   return render(
       request,
       "accounts/dashboard.html",
       {
           "organization": organization,
           "donations": donations,
           "requests": requests,
       }
   )

@login_required
def donor_dashboard(request):
   return redirect("dashboard")

@login_required
def organization_dashboard(request):
   return redirect("dashboard")

@login_required
def create_post_view(request):
   if request.user.role == "donor":
       form_class = DonationForm
       post_type = "Donation"
   elif request.user.role == "organization":
       form_class = RequestForm
       post_type = "Request"
   else:
       return redirect("login")
   if request.method == "POST":
       form = form_class(request.POST)
       if form.is_valid():
           post = form.save(commit=False)
           if request.user.role == "donor":
               post.user = request.user
           else:
               try:
                   post.organization = request.user.organization
               except Organization.DoesNotExist:
                   messages.error(
                       request,
                       "Your organization profile could not be found."
                   )
                   return redirect("dashboard")
           post.save()
           messages.success(
               request,
               f"Your {post_type.lower()} post has been created successfully."
           )
           return redirect("dashboard")
   else:
       form = form_class()
   return render(
       request,
       "accounts/create_post.html",
       {
           "form": form,
           "post_type": post_type,
       }
   )

@login_required
def profile_view(request):
   if request.method == "POST":
       form = ProfileUpdateForm(
           request.POST,
           instance=request.user
       )
       if form.is_valid():
           form.save()
           messages.success(
               request,
               "Your profile has been updated successfully."
           )
           return redirect("profile")
   else:
       form = ProfileUpdateForm(instance=request.user)
   return render(
       request,
       "accounts/profile.html",
       {"form": form}
   )

def logout_view(request):
   if request.method == "POST":
       logout(request)
       messages.success(
           request,
           "You have successfully logged out."
       )
   return redirect("login")