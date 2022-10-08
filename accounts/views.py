from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm

# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class SignInView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class SignOutView(LogoutView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
