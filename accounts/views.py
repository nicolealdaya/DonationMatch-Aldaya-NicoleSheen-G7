from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileUpdateForm

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
       form = AuthenticationForm(
           request,
           data=request.POST
       )
       if form.is_valid():
           user = form.get_user()
           login(request, user)
           if user.role == "donor":
               return redirect("donor_dashboard")
           elif user.role == "organization":
               return redirect("organization_dashboard")
   else:
       form = AuthenticationForm()
   return render(
       request,
       "accounts/login.html",
       {"form": form}
   )

@login_required
def donor_dashboard(request):
   if request.user.role != "donor":
       return redirect("organization_dashboard")
   return render(
       request,
       "accounts/donor_dashboard.html"
   )

@login_required
def organization_dashboard(request):
   if request.user.role != "organization":
       return redirect("donor_dashboard")
   return render(
       request,
       "accounts/organization_dashboard.html"
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