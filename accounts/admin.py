from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
   fieldsets = UserAdmin.fieldsets + (
       ('Additional Information', {
           'fields': ('full_name', 'role', 'contact_number')
       }),
   )
   add_fieldsets = UserAdmin.add_fieldsets + (
       ('Additional Information', {
           'fields': ('full_name', 'email', 'role', 'contact_number')
       }),
   )
   list_display = (
       'username',
       'full_name',
       'email',
       'role',
       'is_staff'
   )