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
       "posts/mine/",
       views.my_posts_view,
       name="my_posts"
   ),
   path(
       "posts/<str:post_type>/<int:post_id>/edit/",
       views.edit_post_view,
       name="edit_post"
   ),
   path(
       "posts/<str:post_type>/<int:post_id>/delete/",
       views.delete_post_view,
       name="delete_post"
   ),
   path(
       "explore/",
       views.explore_view,
       name="explore"
   ),
   path(
       "profile/",
       views.profile_view,
       name="profile"
   ),
]