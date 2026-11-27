import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def create_default_categories(apps, schema_editor):
   Category = apps.get_model("accounts", "Category")
   database = schema_editor.connection.alias
   categories = [
       "Clothes",
       "Food",
       "School Supplies",
       "Books",
       "Furniture",
       "Hygiene Items",
   ]
   for name in categories:
       Category.objects.using(database).get_or_create(name=name)

class Migration(migrations.Migration):
   dependencies = [
       ("accounts", "0001_initial"),
   ]
   operations = [
       migrations.CreateModel(
           name="Category",
           fields=[
               ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
               ("name", models.CharField(max_length=100, unique=True)),
           ],
           options={
               "ordering": ["name"],
           },
       ),
       migrations.CreateModel(
           name="Donation",
           fields=[
               ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
               ("item_name", models.CharField(max_length=150)),
               ("description", models.TextField()),
               ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
               ("status", models.CharField(choices=[("Active", "Active"), ("Inactive", "Inactive")], default="Active", max_length=10)),
               ("date_posted", models.DateTimeField(auto_now_add=True)),
               ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="donations", to="accounts.category")),
               ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="donations", to=settings.AUTH_USER_MODEL)),
           ],
       ),
       migrations.CreateModel(
           name="Request",
           fields=[
               ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
               ("item_name", models.CharField(max_length=150)),
               ("description", models.TextField()),
               ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
               ("status", models.CharField(choices=[("Active", "Active"), ("Inactive", "Inactive")], default="Active", max_length=10)),
               ("date_posted", models.DateTimeField(auto_now_add=True)),
               ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="requests", to="accounts.category")),
               ("organization", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="requests", to="accounts.organization")),
           ],
       ),
       migrations.RunPython(
           create_default_categories,
           migrations.RunPython.noop
       ),
   ]