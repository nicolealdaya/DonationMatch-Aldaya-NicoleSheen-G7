from django.contrib.auth.models import AbstractUser
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