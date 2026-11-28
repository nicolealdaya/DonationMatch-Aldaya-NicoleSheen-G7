from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from .forms import (
   UserRegistrationForm,
   ProfileUpdateForm,
   DonationForm,
   RequestForm,
)
from .models import Organization, Category, Donation, Request

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
   return render(request, "accounts/register.html", {"form": form})

def login_view(request):
   if request.method == "POST":
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
           user = form.get_user()
           login(request, user)
           if user.role == "donor":
               return redirect("donor_dashboard")
           return redirect("organization_dashboard")
   else:
       form = AuthenticationForm()
   return render(request, "accounts/login.html", {"form": form})

@login_required
def donor_dashboard(request):
   if request.user.role != "donor":
       return redirect("organization_dashboard")
   return render(request, "accounts/donor_dashboard.html")

@login_required
def organization_dashboard(request):
   if request.user.role != "organization":
       return redirect("donor_dashboard")
   return render(request, "accounts/organization_dashboard.html")

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
                   return redirect("organization_dashboard")
           post.save()
           messages.success(
               request,
               f"Your {post_type.lower()} post has been created successfully."
           )
           if request.user.role == "donor":
               return redirect("donor_dashboard")
           return redirect("organization_dashboard")
   else:
       form = form_class()
   return render(
       request,
       "accounts/create_post.html",
       {"form": form, "post_type": post_type}
   )

@login_required
def explore_view(request):
   search_query = request.GET.get("search", "").strip()
   category_id = request.GET.get("category", "")
   donations = Donation.objects.filter(
       status="Active"
   ).select_related("user", "category")
   requests = Request.objects.filter(
       status="Active"
   ).select_related("organization__user", "category")
   if search_query:
       donations = donations.filter(
           Q(item_name__icontains=search_query) |
           Q(description__icontains=search_query)
       )
       requests = requests.filter(
           Q(item_name__icontains=search_query) |
           Q(description__icontains=search_query)
       )
   if category_id:
       donations = donations.filter(category_id=category_id)
       requests = requests.filter(category_id=category_id)
   donations = donations.order_by("-date_posted")
   requests = requests.order_by("-date_posted")
   return render(
       request,
       "accounts/explore.html",
       {
           "donations": donations,
           "requests": requests,
           "categories": Category.objects.all(),
           "search_query": search_query,
           "selected_category": category_id,
       }
   )

@login_required
def my_posts_view(request):
   if request.user.role == "donor":
       donations = Donation.objects.filter(
           user=request.user
       ).select_related("category").order_by("-date_posted")
       requests = None
   elif request.user.role == "organization":
       donations = None
       requests = Request.objects.filter(
           organization__user=request.user
       ).select_related("category").order_by("-date_posted")
   else:
       return redirect("login")
   return render(
       request,
       "accounts/my_posts.html",
       {
           "donations": donations,
           "requests": requests,
       }
   )

@login_required
@require_POST
def edit_post_view(request, post_type, post_id):
   if post_type == "donation" and request.user.role == "donor":
       post = get_object_or_404(
           Donation,
           pk=post_id,
           user=request.user
       )
       form = DonationForm(request.POST, instance=post)
   elif post_type == "request" and request.user.role == "organization":
       post = get_object_or_404(
           Request,
           pk=post_id,
           organization__user=request.user
       )
       form = RequestForm(request.POST, instance=post)
   else:
       return redirect("my_posts")
   if form.is_valid():
       form.save()
       messages.success(request, "Your post has been updated successfully.")
   else:
       messages.error(request, form.errors.as_text())
   return redirect("my_posts")

@login_required
@require_POST
def delete_post_view(request, post_type, post_id):
   if post_type == "donation" and request.user.role == "donor":
       post = get_object_or_404(
           Donation,
           pk=post_id,
           user=request.user
       )
   elif post_type == "request" and request.user.role == "organization":
       post = get_object_or_404(
           Request,
           pk=post_id,
           organization__user=request.user
       )
   else:
       return redirect("my_posts")
   post.delete()
   messages.success(request, "Your post has been deleted successfully.")
   return redirect("my_posts")

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
   return render(request, "accounts/profile.html", {"form": form})

def logout_view(request):
   if request.method == "POST":
       logout(request)
       messages.success(request, "You have successfully logged out.")
   return redirect("login")