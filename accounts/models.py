from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

class User(AbstractUser):
   ROLE_CHOICES = [
       ("donor", "Donor"),
       ("organization", "Organization"),
   ]
   full_name = models.CharField(max_length=100)
   email = models.EmailField(max_length=150, unique=True)
   contact_number = models.CharField(max_length=20)
   role = models.CharField(max_length=20, choices=ROLE_CHOICES)
   def __str__(self):
       return self.username

class Organization(models.Model):
   user = models.OneToOneField(
       User,
       on_delete=models.CASCADE,
       related_name="organization"
   )
   organization_name = models.CharField(max_length=150)
   def __str__(self):
       return self.organization_name

class Category(models.Model):
   name = models.CharField(max_length=100, unique=True)
   class Meta:
       ordering = ["name"]
   def __str__(self):
       return self.name

class Donation(models.Model):
   STATUS_CHOICES = [
       ("Active", "Active"),
       ("Inactive", "Inactive"),
   ]
   user = models.ForeignKey(
       User,
       on_delete=models.CASCADE,
       related_name="donations"
   )
   category = models.ForeignKey(
       Category,
       on_delete=models.PROTECT,
       related_name="donations"
   )
   item_name = models.CharField(max_length=150)
   description = models.TextField()
   quantity = models.PositiveIntegerField(
       validators=[MinValueValidator(1)]
   )
   status = models.CharField(
       max_length=10,
       choices=STATUS_CHOICES,
       default="Active"
   )
   date_posted = models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return self.item_name

class Request(models.Model):
   STATUS_CHOICES = [
       ("Active", "Active"),
       ("Inactive", "Inactive"),
   ]
   organization = models.ForeignKey(
       Organization,
       on_delete=models.CASCADE,
       related_name="requests"
   )
   category = models.ForeignKey(
       Category,
       on_delete=models.PROTECT,
       related_name="requests"
   )
   item_name = models.CharField(max_length=150)
   description = models.TextField()
   quantity = models.PositiveIntegerField(
       validators=[MinValueValidator(1)]
   )
   status = models.CharField(
       max_length=10,
       choices=STATUS_CHOICES,
       default="Active"
   )
   date_posted = models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return self.item_name