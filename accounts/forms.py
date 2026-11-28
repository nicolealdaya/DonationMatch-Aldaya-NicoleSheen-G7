from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Organization, Donation, Request

class UserRegistrationForm(UserCreationForm):
   organization_name = forms.CharField(
       max_length=150,
       required=False,
       label="Organization Name"
   )
   class Meta:
       model = User
       fields = [
           "full_name",
           "username",
           "email",
           "contact_number",
           "role",
           "organization_name",
       ]
   def clean_email(self):
       email = self.cleaned_data["email"].strip().lower()
       if User.objects.filter(email__iexact=email).exists():
           raise forms.ValidationError(
               "This email address is already registered."
           )
       return email
   def clean(self):
       cleaned_data = super().clean()
       role = cleaned_data.get("role")
       organization_name = cleaned_data.get("organization_name")
       if role == "organization" and not organization_name:
           self.add_error(
               "organization_name",
               "Organization name is required."
           )
       return cleaned_data
   def save(self, commit=True):
       user = super().save(commit=False)
       user.email = self.cleaned_data["email"]
       if commit:
           user.save()
           if user.role == "organization":
               Organization.objects.create(
                   user=user,
                   organization_name=self.cleaned_data[
                       "organization_name"
                   ]
               )
       return user

class ProfileUpdateForm(forms.ModelForm):
   class Meta:
       model = User
       fields = [
           "full_name",
           "email",
           "contact_number",
       ]
   def clean_email(self):
       email = self.cleaned_data["email"].strip().lower()
       if User.objects.filter(
           email__iexact=email
       ).exclude(pk=self.instance.pk).exists():
           raise forms.ValidationError(
               "This email address is already registered."
           )
       return email

class DonationForm(forms.ModelForm):
   class Meta:
       model = Donation
       fields = [
           "item_name",
           "category",
           "description",
           "quantity",
       ]
       widgets = {
           "description": forms.Textarea(attrs={"rows": 4}),
           "quantity": forms.NumberInput(attrs={"min": 1}),
       }
   def clean_quantity(self):
       quantity = self.cleaned_data["quantity"]
       if quantity < 1:
           raise forms.ValidationError(
               "Quantity must be at least 1."
           )
       return quantity

class RequestForm(forms.ModelForm):
   class Meta:
       model = Request
       fields = [
           "item_name",
           "category",
           "description",
           "quantity",
       ]
       widgets = {
           "description": forms.Textarea(attrs={"rows": 4}),
           "quantity": forms.NumberInput(attrs={"min": 1}),
       }
   def clean_quantity(self):
       quantity = self.cleaned_data["quantity"]
       if quantity < 1:
           raise forms.ValidationError(
               "Quantity must be at least 1."
           )
       return quantity