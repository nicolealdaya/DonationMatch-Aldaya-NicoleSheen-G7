from django.urls import path
from . import views
urlpatterns = [
   path("register/", views.register_view, name="register"),
   path("login/", views.login_view, name="login"),
   path("logout/", views.logout_view, name="logout"),
   path(
       "donor/dashboard/",
       views.donor_dashboard,
       name="donor_dashboard"
   ),
   path(
       "organization/dashboard/",
       views.organization_dashboard,
       name="organization_dashboard"
   ),
   path(
       "posts/create/",
       views.create_post_view,
       name="create_post"
   ),
   path(
       "profile/",
       views.profile_view,
       name="profile"
   ),
]