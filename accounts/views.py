from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import RegisterForm
User = get_user_model()

# REGISTER
def register_view(request):
   if request.user.is_authenticated:
       return redirect('dashboard')
   if request.method == 'POST':
       form = RegisterForm(request.POST)
       if form.is_valid():
           user = form.save()
           messages.success(request, 'Account created successfully! You can now log in.')
           return redirect('login')
   else:
       form = RegisterForm()
   return render(request, 'accounts/register.html', {'form': form})

# LOGIN
def login_view(request):
   if request.user.is_authenticated:
       return redirect('dashboard')
   if request.method == 'POST':
       form = AuthenticationForm(request, data=request.POST)
       if form.is_valid():
           user = form.get_user()
           login(request, user)
           messages.success(request, 'Welcome to DonationMatch!')
           if user.is_superuser or user.is_staff:
               return redirect('admin_dashboard')
           return redirect('dashboard')
       messages.error(request, 'Invalid username or password.')
   else:
       form = AuthenticationForm()
   return render(request, 'accounts/login.html', {'form': form})

# MEMBER DASHBOARD
@login_required
def dashboard_view(request):
   if request.user.is_staff or request.user.is_superuser:
       return redirect('admin_dashboard')
   return render(request, 'accounts/dashboard.html')

# ADMIN DASHBOARD
@login_required
def admin_dashboard_view(request):
   if not (request.user.is_staff or request.user.is_superuser):
       messages.error(request, 'You are not allowed to access the admin dashboard.')
       return redirect('dashboard')
   total_users = User.objects.count()
   total_donors = User.objects.filter(role='donor').count()
   total_organizations = User.objects.filter(role='organization').count()
   context = {
       'total_users': total_users,
       'total_donors': total_donors,
       'total_organizations': total_organizations,
   }
   return render(request, 'accounts/admin_dashboard.html', context)

# PROFILE
@login_required
def profile_view(request):
   if request.method == 'POST':
       full_name = request.POST.get('full_name', '').strip()
       email = request.POST.get('email', '').strip()
       contact_number = request.POST.get('contact_number', '').strip()
       if not full_name or not email:
           messages.error(request, 'Full name and email are required.')
       elif User.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists():
           messages.error(request, 'This email is already registered.')
       else:
           request.user.full_name = full_name
           request.user.email = email
           request.user.contact_number = contact_number
           request.user.save()
           messages.success(request, 'Profile updated successfully!')
           return redirect('profile')
   return render(request, 'accounts/profile.html')

# LOGOUT
@login_required
def logout_view(request):
   if request.method == 'POST':
       logout(request)
       messages.success(request, 'You have logged out successfully.')
       return redirect('login')
   return redirect('dashboard')