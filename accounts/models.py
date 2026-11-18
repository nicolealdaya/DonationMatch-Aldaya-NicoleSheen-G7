from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
   ROLE_CHOICES = [
       ('donor', 'Donor'),
       ('organization', 'Organization'),
   ]
   full_name = models.CharField(max_length=150)
   email = models.EmailField(unique=True)
   contact_number = models.CharField(max_length=20, blank=True)
   role = models.CharField(
       max_length=20,
       choices=ROLE_CHOICES,
       default='donor'
   )
   def __str__(self):
       return self.username