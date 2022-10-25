from django.urls import path

from .views import SignUpView, SignInView, SignOutView, ProfileView, ProfileUpdateView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", SignInView.as_view(), name="login"),
    path("logout/", SignOutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="my_profile"),
    path("author/<str:username>/", ProfileView.as_view(), name="other_profile"),
    path("edit-profile/", ProfileUpdateView.as_view(), name="edit_profile"),
]
